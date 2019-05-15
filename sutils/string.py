def to_bytes(x):
    if isinstance(x, str):
        return x.encode('utf-8', 'replace')
    return x


def to_string(x):
    if isinstance(x, bytes):
        return x.decode('utf-8')
    return x
