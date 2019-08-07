import datetime as dt

epoch = dt.datetime.utcfromtimestamp(0)


def unixtime(dt):
    return (dt - epoch).total_seconds()
