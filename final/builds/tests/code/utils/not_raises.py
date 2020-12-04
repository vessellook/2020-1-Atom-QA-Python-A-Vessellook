from contextlib import contextmanager


# https://gist.github.com/oisinmulvihill/45c14271fad7794a4a52516ecb784e69
@contextmanager
def not_raises(cls: type, msg_expected: str = None, msg_unexpected: str = None):
    """Convert Error test into Failed test. Use it if you expect some error"""
    try:
        yield
    except cls as error:
        msg = error.msg if hasattr(error, 'msg') else ''
        msg += (' | ' + msg_expected) if msg_expected is not None else ''
        raise AssertionError(msg) from error

    except Exception as error:
        msg = error.msg if hasattr(error, 'msg') else ''  # pylint: disable=no-mumber
        msg += msg_unexpected if msg_unexpected is not None else ''
        raise AssertionError(msg) from error