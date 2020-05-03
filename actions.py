
def Connected():
    return dict(type='CONNECTED')


def Disconnected():
    return dict(type='DISCONNECTED')


def NewFile(path):
    return dict(type='NEW_FILE', path=path)

def FailedTransfer(path):
    return dict(type='TRANSFER_FAILED', path=path)