"""
  utils.py
  DMOR Project

  Created by Weihang Ren on 12/07/23.
"""

from datetime import datetime


def near_zero(num):
    return abs(num) < 1e-6


def dateit(s):
    if not isinstance(s, str):
        time = min2time(s)
    else:
        time = datetime.strptime(s, "%H:%M").time()
    return datetime(2000, 1, 1, hour=time.hour, minute=time.minute, second=time.second)


def min2time(f):
    hour, remainder = divmod(f * 60, 3600)
    min, sec = divmod(remainder, 60)
    return datetime(2000, 1, 1, hour=int(hour), minute=int(min), second=int(sec))
