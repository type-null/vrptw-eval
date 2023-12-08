"""
  Customer.py
  DMOR Project

  Created by Weihang Ren on 12/07/23.
"""

from utils import *
from datetime import datetime, timedelta


class Customer:
    def __init__(self, cid, row):
        self._id = cid
        self._name = str(row["Customer ID"])
        self._x = float(row["X"])
        self._y = float(row["Y"])
        self._demand = float(row["Demand (pounds)"])
        time = datetime.strptime(row["Service-time"], "%H:%M").time()
        self._service_time = timedelta(hours=time.hour, minutes=time.minute)
        self._service_start = dateit(row["Time-window(start; h:m)"])
        self._service_end = dateit(row["Time-window(end; h:m)"])
        self._latest_start = self._service_end - self._service_time
        self._splitable = True if row["Can this demand be split"] == "Y" else False
        self._served = 0.0
        self._visited_trucks = []

    def serve(self, load, tname):
        self._served += load
        self._visited_trucks.append(tname)

    def check_served(self):
        return near_zero(self._served - self._demand)

    def check_split(self):
        """
        Return False if not splitable and more than 1 truck visited
        """
        if not self._splitable:
            return len(self._visited_trucks) < 2
        return True

    def reset(self):
        self._served = 0
        self._visited_trucks = []

    def __str__(self):
        return (
            f"Customer(name={self._name}, "
            f"demand={self._demand}, "
            f"served={self._served}, "
            f"trucks={self._visited_trucks})"
        )
