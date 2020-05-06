from autokindle.state import State

def reducer(state=State(), action=None):
    if action is None:
        return state
    if action['type'] == 'CONNECTED':
        return State(is_connected=True, paths=[], processing=state.paths)
    elif action['type'] == 'DISCONNECTED':
        return state.copy(is_connected=False)
    elif action['type'] == 'NEW_FILE':
        if (state.is_connected):
            return state.copy(processing=[action['path']])
        else:
            return state.copy(paths=[*state.paths, action['path']])
    elif action['type'] == 'TRANSFER_FAILED':
        if (state.is_connected):
            return state.copy(processing=[action['path']])
        else:
            return state.copy(paths=[*state.paths, action['path']])
        return
    else:
        return state