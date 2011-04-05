from types import UnicodeType


def convertStringToId(s, maxlen=None):
    """
    Converts a string into a Zope-safe ID.

    thx to Joel BURTON  <joel@joelburton.com> joelburton.com

    This removes all non-identifier safe characters. It replaces
    most with underscores, while trying to make the ID match a
    sensible choice (eg "Bill's House" -> "bills_house", not "bill_s_house").
    The output is always lowercase, and any leading underscores are
    removed (as they would be illegal in Zope.

    s = string to convert
    maxlen = maximum length of ID

    returns string.
    """

    if type(s) == UnicodeType:
        s = s.encode('latin-1')

    tt = '______________________________________________._0123456789_______abcdefghijklmnopqrstuvwxy_______abcdefghijklmnopqrstuvwxyz_____________________________________________________________________________________________________________________________________'

    s=s.lower()

    # translate most things to underscore. remove punctuation below w/o translating
    s = s.translate(tt, '!@#$%^&*()-=+,\'"')

    # remove leading and trailing underscores
    s = s.strip("_")

    # remove ALL double-underscores
    while s.find("__") > -1:
        s = s.replace('__', '_')

    # trim to maxlength
    if maxlen and len(s) > maxlen:
        s = s[:maxlen]

    return s
