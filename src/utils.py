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
    hour = int(f // 60)
    min = int(f % 60)
    return datetime(2000, 1, 1, hour=hour, minute=min, second=0)
