import os
import subprocess
import rx
from rx.subject import Subject
from rx import operators
import actions

from constants import paths


def new_files(epub_handler):
    subject = Subject()

    def on_created(event):
        subject.on_next(event.src_path)
    epub_handler.on_created = on_created
    return subject.pipe(
        operators.flat_map(_mapToConvertedFile)
    )


def connection_statuses(kindle_handler):
    subject = Subject()

    def on_created(_):
        subject.on_next(actions.Connected())

    def on_deleted(_):
        subject.on_next(actions.Disconnected())
    kindle_handler.on_created = on_created
    kindle_handler.on_deleted = on_deleted
    return subject


def failed_transfers(store):
    proccessing_files = Subject()

    def transfer_files():
        state = store.getState()
        if (state.processing):
            proccessing_files.on_next(state.processing)
    store.subscribe(transfer_files)
    return proccessing_files.pipe(
        operators.map(lambda paths: rx.from_iterable(paths)),
        operators.merge_all(),
        operators.flat_map(_transfer_file),
    )


def _mapToConvertedFile(src_path):
    def change_extension_to_mobi(path):
        return f"{os.path.splitext(path)[0]}.mobi"

    def push_converted_files(observer, scheduler):
        subprocess.run([paths.KINDLEGEN, src_path],
                       cwd=paths.BUCKET, stdout=subprocess.DEVNULL)
        subprocess.run(['rm', src_path])
        observer.on_next(actions.NewFile(
            path=change_extension_to_mobi(src_path)))
        observer.on_completed()
    return rx.create(push_converted_files)


def _transfer_file(path):
    result = subprocess.run(
        [f"mv '{path}' {paths.KINDLE_DOCUMENTS}"], shell=True, stderr=subprocess.DEVNULL)
    if (result.returncode == 0):
        return rx.empty()
    else:
        return rx.of(actions.FailedTransfer(path))
