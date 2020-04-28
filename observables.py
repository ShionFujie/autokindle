import os
import subprocess
import rx
from rx import operators
from constants import paths


def new_files(epub_handler):
    return rx.create(_push_new_files(epub_handler)).pipe(
        operators.flat_map(_mapToConvertedFile)
    )


def connection_statuses(kindle_handler):
    return rx.create(_push_connection_statuses(kindle_handler))


def _push_new_files(watchdog_handler):
    def _(observer, scheduler):
        def on_created(event):
            observer.on_next(event.src_path)
        watchdog_handler.on_created = on_created
    return _


def _push_connection_statuses(watchdog_handler):
    def _(observer, scheduler):
        def on_created(_):
            observer.on_next(dict(type='CONNECTED'))

        def on_deleted(_):
            observer.on_next(dict(type='DISCONNECTED'))
        watchdog_handler.on_created = on_created
        watchdog_handler.on_deleted = on_deleted
    return _


def _mapToConvertedFile(src_path):
    def change_extension_to_mobi(path):
        return f"{os.path.splitext(path)[0]}.mobi"

    def push_converted_files(observer, scheduler):
        subprocess.run([paths.KINDLEGEN, src_path], cwd=paths.BUCKET)
        subprocess.run(['rm', src_path])
        observer.on_next(dict(type='NEW_FILE', path=change_extension_to_mobi(src_path)))
        observer.on_completed()
    return rx.create(push_converted_files)
