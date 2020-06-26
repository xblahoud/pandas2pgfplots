"""Utilities for nested dicts and translation into pgfplots syntax."""

import collections


def tikzify_dict(args, padding=0):
    """Translates Python dict of args into string to be passed to TikZ code.

    For a pair `k` : `v` we will get `k=v,%\n`, these values are TikZified
    (see further) and merged into a single string.

    TikZification means that we substiture True for "true", False for "false",
    and None for "none".

    Returns a string with TikZ options
    """
    res = ""
    pad = " " * padding
    for k, v in args.items():
        res += pad
        if v is False:
            res += f"{k}=false"
        elif v is True:
            res += f"{k}=true"
        elif v is None:
            res += f"{k}=none"
        elif isinstance(v, collections.Mapping):
            res += f"{k}={{\n{tikzify_dict(v, padding + 2)}{pad}}}"
        else:
            res += f"{k}={v}"
        res += ",\n"
    return res


def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.items():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source
