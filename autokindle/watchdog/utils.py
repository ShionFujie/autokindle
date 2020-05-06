from watchdog.observers import Observer
from autokindle.constants import paths
from autokindle.watchdog.observer_runner import ObserverRunner


def start_watching(epub_handler, kindle_handler):
    observer = Observer()
    observer.schedule(
        path=paths.BUCKET,
        event_handler=epub_handler
    )
    observer.schedule(
        path=paths.VOLUMES,
        event_handler=kindle_handler
    )
    ObserverRunner().runObserver(observer)
