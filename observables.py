import os
import subprocess
import rx
from rx.subject import Subject
from rx import operators

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
        subject.on_next(dict(type='CONNECTED'))
    def on_deleted(_):
        subject.on_next(dict(type='DISCONNECTED'))
    kindle_handler.on_created = on_created
    kindle_handler.on_deleted = on_deleted
    return subject


def _mapToConvertedFile(src_path):
    def change_extension_to_mobi(path):
        return f"{os.path.splitext(path)[0]}.mobi"

    def push_converted_files(observer, scheduler):
        subprocess.run([paths.KINDLEGEN, src_path], cwd=paths.BUCKET)
        subprocess.run(['rm', src_path])
        observer.on_next(dict(type='NEW_FILE', path=change_extension_to_mobi(src_path)))
        observer.on_completed()
    return rx.create(push_converted_files)
