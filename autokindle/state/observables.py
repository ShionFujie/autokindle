import os
import subprocess
import rx
from rx.subject import Subject, ReplaySubject
from rx import operators
from autokindle.logging import getLogger
from autokindle.state import actions
from autokindle.constants import paths


def events(file_handler, connection_handler, store):
    return rx.concat(
        _initialize(),
        rx.merge(
            _new_files(file_handler),
            _connection_statuses(connection_handler),
            _failed_transfers(store),
        )
    )


def _initialize():
    def convert_if_necessary(path):
        return _convert_to_mobi(path) if path.endswith(".epub") else path

    def _(emitter, _):
        is_connected = os.path.isdir(paths.KINDLE_DOCUMENTS)
        file_paths = [convert_if_necessary(os.path.join(paths.BUCKET, path))
                      for path in os.listdir(paths.BUCKET) if path.endswith((".pdf", ".mobi", ".epub"))]
        emitter.on_next(actions.Initialize(is_connected, file_paths))
        emitter.on_completed()
    return rx.create(_)


def _new_files(epub_handler):
    subject = Subject()

    def on_created(event):
        subject.on_next(event.src_path)
    epub_handler.on_created = on_created
    return subject.pipe(
        operators.flat_map(_convert_file_if_necessary)
    )


def _connection_statuses(kindle_handler):
    subject = Subject()

    def on_created(_):
        subject.on_next(actions.Connected())

    def on_deleted(_):
        subject.on_next(actions.Disconnected())
    kindle_handler.on_created = on_created
    kindle_handler.on_deleted = on_deleted
    return subject


def _failed_transfers(store):
    processing_files = ReplaySubject()

    def transfer_files():
        state = store.getState()
        if (state.processing):
            processing_files.on_next(state.processing)
    store.subscribe(transfer_files)
    return processing_files.pipe(
        operators.map(lambda paths: rx.from_iterable(paths)),
        operators.merge_all(),
        operators.flat_map(_transfer_file)
    )


def _convert_file_if_necessary(src_path):
    def get_extension(path):
        return os.path.splitext(path)[1]

    def push_converted_files(observer, scheduler):
        observer.on_next(actions.NewFile(path=_convert_to_mobi(src_path)))
        observer.on_completed()
    ext = get_extension(src_path)
    if ext == ".epub":
        return rx.create(push_converted_files)
    else:
        return rx.of(actions.NewFile(src_path))


def _convert_to_mobi(src_path):
    def change_extension_to_mobi(path):
        return f"{os.path.splitext(path)[0]}.mobi"
    subprocess.run([paths.KINDLEGEN, src_path],
                   cwd=paths.BUCKET, stdout=subprocess.DEVNULL)
    subprocess.run(['rm', src_path])
    return change_extension_to_mobi(src_path)


def _transfer_file(path):
    result = subprocess.run(
        [f"mv '{path}' {paths.KINDLE_DOCUMENTS}"], shell=True, stderr=subprocess.DEVNULL)
    if (result.returncode == 0):
        return rx.empty()
    else:
        return rx.of(actions.FailedTransfer(path))
