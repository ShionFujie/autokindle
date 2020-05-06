class State:
    def __init__(self, paths=[], is_connected=False, processing=[]):
        self.paths = paths
        self.is_connected = is_connected
        self.processing = processing

    def is_idle(self):
        return not self.paths and not self.is_connected

    def needs_sync(self):
        return self.paths and not self.is_connected

    def awaits_files(self):
        return not self.paths and self.is_connected

    def is_syncing(self):
        return self.paths and self.is_connected

    def copy(self, processing=[], **updates):
        return State(**{**self.__dict__, **updates, 'processing': processing})
