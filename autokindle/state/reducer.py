from autokindle.state import State

def reducer(state=State(), action=None):
    type =  action['type'] if action else None

    if type == 'INITIALIZE':
        return State(is_connected=action['is_connected'])
    elif type == 'CONNECTED':
        return State(is_connected=True, paths=[], processing=state.paths)
    elif type == 'DISCONNECTED':
        return state.copy(is_connected=False)
    elif type == 'NEW_FILE':
        if (state.is_connected):
            return state.copy(processing=[action['path']])
        else:
            return state.copy(paths=[*state.paths, action['path']])
    elif type == 'TRANSFER_FAILED':
        if (state.is_connected):
            return state.copy(processing=[action['path']])
        else:
            return state.copy(paths=[*state.paths, action['path']])
        return
    else:
        return state