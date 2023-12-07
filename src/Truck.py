"""
  Truck.py
  DMOR Project

  Created by Weihang Ren on 12/07/23.
"""

from utils import *


class Truck:
    def __init__(self, idx, row):
        self._id = idx
        self._name = str(int(row["truck"].tolist()[0]))
        self._capacity = 20000
        self._distance = 0
        self._stops = [str(int(i)) for i in row["stop"].tolist()]
        self._offloads = row["offload"].tolist()
        self._starts = [dateit(i) for i in row["start"].tolist() if i != 0]
        self._desc = f"Truck {self._name}:\n"
        self._total_load = sum(self._offloads)
        # sanity checks
        self.check_capacity()
        self.check_depot()
        self.check_no_repeat_customer()

    def check_capacity(self):
        if self._total_load > self._capacity:
            self._desc += f"Overloaded: {self._total_load}\n"

    def check_depot(self):
        if self._stops[0] == self._stops[-1]:
            self._depot = self._stops[0]
        else:
            self._desc += (
                f"Didn't return to depot: {self._stops[0]}-{self._stops[-1]}\n"
            )

    def check_no_repeat_customer(self):
        dup = set()
        seen = set()
        for c in self._stops[1:-1]:
            if c in seen:
                dup.add(c)
            seen.add(c)
        if len(dup) > 0:
            self._desc += f"Visited {dup} more than once!\n"

    def set_distance(self, distance):
        self._distance = distance

    def __str__(self):
        if self._desc == f"Truck {self._name}:\n":
            return ""
        else:
            return self._desc
