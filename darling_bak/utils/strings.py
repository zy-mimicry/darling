#! /usr/bin/env python
# coding=utf-8

def get_string_between_spaces(re_name, string):
    import re
    class NotFindPatternString(Exception):pass
    pattern = '({re_name}.*?)\s+(.*?)\s+.*'.format(re_name = re_name)
    g = re.search(pattern, string, re.I)
    try: # If not match, g is None
        return string[g.span(2)[0] : g.span(2)[1]]
    except AttributeError:
        raise NotFindPatternString("Pattern passed, can't found.")
