import time
from autokindle.logging import getLogger


class ObserverRunner:
    logger = getLogger(__name__, 'ObserverRunner')

    def runObserver(self, observer):
        observer.start()
        self.logger.info('Observer started')
        self._run_until_interrupted(self._OnInterruptedListener(observer))
        observer.join()

    def _run_until_interrupted(self, onInterrupted):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            onInterrupted()

    def _OnInterruptedListener(self, observer):
        def onInterrupted():
            observer.stop()
            self.logger.info("Observer stopped")
        return onInterrupted
