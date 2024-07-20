from pathlib import PurePosixPath, PureWindowsPath

def match_file_type(path, included_patterns=None, excluded_patterns=None, case_sensitive=True):
    """
    Matches from a set of paths based on acceptable patterns and
    ignorable patterns.
    :param path:
        path name that will be filtered based on matching and
        ignored patterns.
    :param included_patterns:
        Allow filenames matching wildcard patterns specified in this list.
        If no pattern list is specified, ["*"] is used as the default pattern,
        which matches all files.
    :param excluded_patterns:
        Ignores filenames matching wildcard patterns specified in this list.
        If no pattern list is specified, no files are ignored.
    :param case_sensitive:
        ``True`` if matching should be case-sensitive; ``False`` otherwise.
    :returns:
        ``True`` if any of the paths matches; ``False`` otherwise.
    """
    included = ["*"] if included_patterns is None else included_patterns
    excluded = [] if excluded_patterns is None else excluded_patterns

    if _match_path(path, set(included), set(excluded), case_sensitive):
        return True
    else:
        return False

def _match_path(path, included_patterns, excluded_patterns, case_sensitive):
    if case_sensitive:
        path = PurePosixPath(path)
    else:
        included_patterns = {pattern.lower() for pattern in included_patterns}
        excluded_patterns = {pattern.lower() for pattern in excluded_patterns}
        path = PureWindowsPath(path)

    common_patterns = included_patterns & excluded_patterns
    if common_patterns:
        raise ValueError("conflicting patterns `{}` included and excluded".format(common_patterns))
    return any(path.match(p) for p in included_patterns) and not any(path.match(p) for p in excluded_patterns)