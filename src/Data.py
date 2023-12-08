"""
  Data.py
  DMOR Project

  Created by Weihang Ren on 12/07/23.
"""

import math
import pandas as pd
from Customer import Customer
from Truck import Truck
from datetime import timedelta


class Data:
    def __init__(self, file):
        self.customers = []
        self.customerID = {}
        self.read(file)

        self.trucks = []
        self.depot1 = [0, 0]  # 0
        self.depot2 = [-50, 50]  # -1
        self.depot3 = [50, -50]  # -2

        self.cost = 0
        self.truck_rent = 200
        self.gas_price = 3

        self.report = ""
        # time precisioin tolerance
        self._time_tol = 0

    def read(self, file):
        df = pd.read_csv(file)
        for i, row in df.iterrows():
            customer = Customer(i, row)
            self.customers.append(customer)
            self.customerID[customer._name] = customer._id

    def read_solution(self, solution_file, part):
        """
        Calculate the total cost
        """
        self.reset()
        self.sol = pd.read_csv(solution_file).fillna(0)
        self.report += f"\nPart {part}:\n"
        self.verify_basic()
        if part > 1:
            self.verify_time()
        self.report += f"Total cost = {self.cost}\n"

    def verify_basic(self):
        """
        Verify all customers demands are satisfied
        Verify all trucks are within capacity
        Verify total trucks number (<=20)
        """
        for i, row in self.sol.groupby("truck"):
            truck = Truck(i, row)
            self.trucks.append(truck)
            if truck.__str__() != "":
                self.report += truck.__str__()
        self.adjust_start_time()

        if len(self.trucks) > 20:
            self.report += f"Too many trucks: {len(self.trucks)} {[t._name for t in self.trucks]}\n"

        for truck in self.trucks:
            self.calc_distance(truck)
            self.cost += self.truck_rent
            self.cost += truck._distance * self.gas_price
            for i, cname in enumerate(truck._stops):
                if cname in self.customerID.keys():
                    self.customers[self.customerID[cname]].serve(
                        truck._offloads[i], truck._name
                    )

        for c in self.customers:
            if not c.check_served():
                self.report += f"Customer {c._name}'s demand not satisfied (unsatisfied={c._demand - c._served})\n"

            if not c.check_split():
                self.report += (
                    f"Customer {c._name}'s demand not splittable: {c._visited_trucks}\n"
                )

    def verify_time(self):
        """
        Verify all customers are timely served
        Verify trucks are able to make the tour constrained by time
        """
        for truck in self.trucks:
            for i, start in enumerate(truck._starts):
                c = self.customers[self.customerID[truck._stops[i + 1]]]
                if start > c._latest_start:
                    self.report += f"Truck {truck._name} served customer {c._name} too late: {start.strftime("%H:%M")}\n"
                if i > 0:
                    last_c = self.customers[self.customerID[truck._stops[i]]]
                    if start < (
                        truck._starts[i - 1]
                        + last_c._service_time
                        + timedelta(
                            minutes=self.distance_between(c._name, last_c._name) - self._time_tol
                        )
                    ):
                        self.report += f"Truck {truck._name} can't make it to customer {c._name} on assumed time {start.strftime("%H:%M")}\n"

    def reset(self):
        for c in self.customers:
            c.reset()
        self.trucks = []
        self.cost = 0

    def adjust_start_time(self):
        for t in self.trucks:
            for i, start in enumerate(t._starts):
                cid = self.customerID[t._stops[i+1]]
                c_start = self.customers[cid]._service_start
                if start < c_start:
                    t._starts[i] = c_start
                    # print(f"Truck {t._name} arrives at {self.customers[cid]._name} at {start} but starts at {c_start}")

    def calc_distance(self, truck):
        d = 0
        for i, cid in enumerate(truck._stops):
            if i > 0:
                d += self.distance_between(cid, last)
                last = cid
            else:
                last = cid
        truck.set_distance(d)
        # self.report += f"Truck {truck._name} traveled {truck._distance} miles result in ${truck._distance * self.gas_price + self.truck_rent}\n"

    def distance_between(self, cname1, cname2):
        x1, y1 = self.get_coord(cname1)
        x2, y2 = self.get_coord(cname2)
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def get_coord(self, cname):
        if cname in self.customerID.keys():
            c = self.customers[self.customerID[cname]]
            return c._x, c._y
        elif cname == "0":
            return self.depot1
        elif cname == "-1":
            return self.depot2
        elif cname == "-2":
            return self.depot3
        else:
            print(cname)

    def write(self, name: str):
        with open("solution/output/" + name + ".txt", "w") as file:
            file.write(self.report)

    def __str__(self):
        return self.report
