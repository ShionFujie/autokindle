class Store:
    def __init__(self, reducer):
        self.reducer = reducer
        self.state = None
        self.listeners = []
        self.dispatch(None)

    def getState(self):
        return self.state

    def dispatch(self, action):
        params = {'action': action}
        if self.state is not None:
            params['state'] = self.state
        self.state = self.reducer(**params)
        for listener in self.listeners:
            listener()

    def subscribe(self, listener):
        def unsubscribe():
            self.listeners.remove(listener)
        self.listeners.append(listener)
        return unsubscribe


# def counter(state=0, action=None):
#     if action == 'INCREMENT':
#         return state + 1
#     elif action == 'DECREMENT':
#         return state - 1
#     else:
#         return state

# store = Store(counter)

# def onCount():
#     print(store.getState())

# store.subscribe(onCount)

# onCount()
# store.dispatch('INCREMENT')
# store.dispatch('INCREMENT')
# store.dispatch('DECREMENT')
