import datetime
import inspect
import os.path
import sys
from functools import wraps
from typing import Any, Union


def get_script_dir(follow_symlinks: bool = True) -> str:
    """return path of the executed script"""
    if getattr(sys, 'frozen', False):
        path = os.path.abspath(sys.executable)
    else:
        if '__main__' in sys.modules and hasattr(sys.modules['__main__'], '__file__'):
            path = sys.modules['__main__'].__file__
        else:
            path = inspect.getabsfile(get_script_dir)

    if follow_symlinks:
        path = os.path.realpath(path)

    return os.path.dirname(path)


def compare(a: Any, b: Any) -> int:
    """compare to values, return -1 if a is smaller than b, 1 if a is greater than b, 0 is both are equal"""
    return bool(a > b) - bool(a < b)


def minmax(*arr: Any) -> (Any, Any):
    """return the min and max value of an array (or arbitrary amount of arguments)"""
    if len(arr) == 1:
        if isinstance(arr[0], list):
            arr = arr[0]
        else:
            return arr[0], arr[0]

    arr = set(arr)
    smallest = min(arr)
    biggest = max(arr)
    if smallest == biggest:
        arr.remove(smallest)
        biggest = max(arr)

    return smallest, biggest


def human_readable_time_from_delta(delta: datetime.timedelta) -> str:
    time_str = ""
    if delta.days > 0:
        time_str += "%d day%s, " % (delta.days, "s" if delta.days > 1 else "")

    if delta.seconds > 3600:
        time_str += "%02d:" % (delta.seconds // 3600)
    else:
        time_str += "00:"

    if delta.seconds % 3600 > 60:
        time_str += "%02d:" % (delta.seconds % 3600 // 60)
    else:
        time_str += "00:"

    return time_str + "%02d" % (delta.seconds % 60)


def cache(func):
    saved = {}

    @wraps(func)
    def newfunc(*args):
        if args in saved:
            return saved[args]

        result = func(*args)
        saved[args] = result
        return result

    return newfunc
