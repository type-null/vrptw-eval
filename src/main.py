"""
  main.py
  DMOR Project

  Created by Weihang Ren on 12/07/23.
"""

from Data import Data

d = Data("Data.csv")

team = 1

d.read_solution(f"solution/team{team}-part1.csv", part=1)
d.read_solution(f"solution/team{team}-part2.csv", part=2)
# d.read_solution(f"solution/team{team}-part3.csv", part=3)

d.write(f"Team{team}")

# print(d.distance_between("28", "4"))
