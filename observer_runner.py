import time

class ObserverRunner:
    def runObserver(self, observer):
        observer.start()
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
            print("observer stopped")
        return onInterrupted