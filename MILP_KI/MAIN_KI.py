import copy
from gurobipy import *
from JO_ALP_TATFP.ORIGINAL_PROBLEM.SMG import SMG


from ZOW.TY.MILP_VIs_KI.KI import KI
from ZOW.TY.MILP_VIs_KI.solution_evaluation import SE




# Distance information
distance_matrix = [[1000000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 31.3, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 90.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 92.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 75.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 80.1, 1000000.0, 79.2, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 85.3, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 49.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 96.5, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 84.5, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 27.1, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 24.2, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 37.3, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 87.1, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 54.4, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 42.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 73.9, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 73.9, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 42.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 46.4, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 46.4, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 42.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 51.2, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 51.2, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 42.0, 1000000.0, 1000000.0, 1000000.0, 67.3, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 67.3, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 42.0, 1000000.0, 9.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 9.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 44.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 33.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 12.2, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 42.0, 35.6, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 35.6, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 22.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 0.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0]]


# 10 fix, 26 paths
Path_list = [[1, 11, 15, 27, 30, 31],
            [2, 11, 15, 27, 30, 31],
            [3, 11, 15, 27, 30, 31],
            [4, 12, 17, 25, 27, 30, 31],
            [5, 12, 17, 25, 27, 30, 31],
            [6, 13, 14, 19, 25, 27, 30, 31],
            [7, 13, 14, 19, 25, 27, 30, 31],
            [8, 21, 26, 28, 30, 31],
            [9, 23, 26, 28, 30, 31],
            [10, 28, 30, 31]]
d = 31




F = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
F_size = [2, 3, 2, 2, 2, 2, 1, 1, 3, 1, 2, 2, 3, 2, 2]
F_speed = [0.062, 0.069, 0.062, 0.062, 0.062, 0.062, 0.066, 0.066, 0.069, 0.066, 0.062, 0.062, 0.069, 0.062, 0.062]
F_weight = [3, 3, 2, 2, 3, 3, 1, 3, 3, 2, 1, 1, 3, 2, 2]
F_path = [7, 6, 4, 8, 9, 1, 2, 10, 6, 10, 1, 4, 4, 3, 7]
separation_matrix = [[0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0], [3, 0, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3], [0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0], [0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0], [0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0], [0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0], [5, 7, 5, 5, 5, 5, 0, 0, 7, 0, 5, 5, 7, 5, 5], [5, 7, 5, 5, 5, 5, 0, 0, 7, 0, 5, 5, 7, 5, 5], [3, 0, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3], [5, 7, 5, 5, 5, 5, 0, 0, 7, 0, 5, 5, 7, 5, 5], [0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0], [0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0], [3, 0, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3], [0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0], [0, 5, 0, 0, 0, 0, 3, 3, 5, 3, 0, 0, 5, 0, 0]]
scenario_weight = 0.05
OMEGA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
scenario_arrival_time = [[1916, 2150, 2156, 2403, 2741, 2816, 2847, 2971, 3074, 3176, 3238, 3375, 3379, 3446, 3501], [1998, 2137, 2504, 2400, 2599, 2886, 3159, 3166, 2722, 3350, 3179, 3492, 3201, 3223, 3285], [2211, 2088, 2413, 2653, 2541, 3024, 2983, 2794, 3001, 3284, 2986, 3150, 3435, 3477, 3216], [1635, 2276, 1818, 2492, 2544, 2723, 2792, 3141, 3282, 3163, 3356, 3017, 3363, 3558, 3549], [1971, 1795, 1973, 2180, 2760, 3135, 2936, 2936, 3006, 2977, 3464, 3405, 3312, 3794, 3362], [1806, 1812, 2199, 2664, 2727, 2570, 2630, 2905, 3046, 3136, 3543, 3285, 3224, 3287, 3734], [1945, 2270, 2004, 2505, 2924, 2939, 3135, 2810, 3351, 2992, 3367, 3091, 3190, 3091, 3798], [2188, 2016, 2181, 2570, 2599, 2903, 2717, 2677, 2760, 3183, 3485, 3075, 3472, 3154, 3684], [2104, 2463, 2126, 2256, 2584, 3136, 2741, 3013, 2955, 3284, 3448, 3058, 3715, 3447, 3468], [2256, 2403, 2513, 2307, 2862, 2641, 2789, 3051, 2828, 3347, 3181, 3195, 3539, 3737, 3336], [2139, 1996, 2056, 2735, 2944, 2463, 3150, 2828, 3218, 3507, 3584, 3650, 3633, 3583, 3317], [2102, 2252, 2194, 2697, 2704, 2892, 3093, 3043, 3083, 3266, 3462, 3039, 3137, 3091, 3163], [1837, 2098, 2129, 2501, 2387, 2897, 2733, 3159, 3360, 2841, 3517, 3065, 3144, 3112, 3419], [2268, 2028, 2314, 2276, 2494, 2761, 2870, 2870, 3032, 2897, 3344, 3486, 3449, 3627, 3164], [2140, 2196, 2146, 2146, 2511, 3073, 3055, 3261, 2978, 3036, 3073, 3695, 3246, 3416, 3463], [2000, 1794, 2133, 2370, 2680, 2678, 2607, 3040, 2886, 3434, 2943, 3412, 3087, 3375, 3664], [2178, 2426, 2139, 2270, 2855, 2894, 2818, 3213, 3321, 3462, 2915, 3239, 3447, 3447, 3710], [2178, 2089, 2462, 2343, 2519, 2519, 3195, 2855, 3098, 3196, 3072, 3129, 3193, 3463, 3694], [1563, 2110, 2372, 2500, 2391, 2934, 2870, 2680, 2938, 3416, 3179, 3433, 3064, 3658, 3308], [1881, 2196, 1952, 2482, 2688, 2697, 2719, 2880, 3098, 2849, 3359, 3601, 3361, 3109, 3262]]





det = len(F) + 1        # dummy_ending_task
Fs = [0] + F
Fe = F + [det]
N = [0] + F + [det]

rw_separation_matrix = SMG(F, F_size)

M = 10000









weighted_arrival_time = [0] * len(F)
for at in scenario_arrival_time:
    aircraft_counter = 0
    while aircraft_counter < len(at):
        weighted_arrival_time[aircraft_counter] += scenario_weight * at[aircraft_counter]
        aircraft_counter += 1


# Enhancements

# 2 Knapsack inequality
weighted_sequence = KI(N, Fs, Fe, F, F_weight, F_path, F_speed, weighted_arrival_time, Path_list, d, M, rw_separation_matrix, distance_matrix, separation_matrix)
second_stage_obj_list = []
for omega in OMEGA:
    arrival_time = copy.deepcopy(scenario_arrival_time[omega - 1])
    SE_result = SE(weighted_sequence, arrival_time, F, F_weight, F_path, F_speed, Path_list, d, M, rw_separation_matrix, distance_matrix, separation_matrix)
    second_stage_obj_list.append(copy.deepcopy(SE_result))
UB = scenario_weight * sum(second_stage_obj_list)








# 3 BUILD THE MODEL
model = Model('JAT')


y = {}
z = {}
t = {}
D = {}

# Define decision variables
for i in Fs:
    for j in Fe:
        if i != j:
            name = 'y_' + str(i) + '_' + str(j)
            y[i, j] = model.addVar(vtype=GRB.BINARY, name=name)

for i in F:
    for j in F:
        if i != j:
            i_path, j_path = copy.deepcopy(Path_list[F_path[i - 1] - 1]), copy.deepcopy(Path_list[F_path[j - 1] - 1])
            ij_N_list = list(set(i_path).intersection(set(j_path)))
            for u in ij_N_list:
                if u != d:
                    for omega in OMEGA:
                        name = 'z_' + str(omega) + '_' + str(i) + '_' + str(j) + '_' + str(u)
                        z[omega, i, j, u] = model.addVar(vtype=GRB.BINARY, name=name)
                
for i in F:
    for u in Path_list[F_path[i - 1] - 1]:
        for omega in OMEGA:
            name = 't_' + str(omega) + '_' + str(i) + '_' + str(u)
            t[omega, i, u] = model.addVar(vtype=GRB.CONTINUOUS, name=name)

for omega in OMEGA:
    for i in F:
        name = 'D_' + str(omega) + '_' + str(i)
        D[omega, i] = model.addVar(vtype=GRB.CONTINUOUS, name=name)


# Objective function
obj = LinExpr(0)
for omega in OMEGA:
    for i in F:
        obj.addTerms(scenario_weight * F_weight[i - 1], D[omega, i])
model.setObjective(obj, GRB.MINIMIZE)


# Constraints
# First stage
# 2.2
expr = LinExpr(0)
for j in Fe:
    expr.addTerms(1, y[Fs[0], j])
model.addConstr(expr == 1)

# 2.3
expr = LinExpr(0)
for i in Fs:
    expr.addTerms(1, y[i, Fe[-1]])
model.addConstr(expr == 1)

# 2.4
for i in F:
    expr1, expr2 = LinExpr(0), LinExpr(0)
    for j in Fs:
        if i != j:
            expr1.addTerms(1, y[j, i])
    for j in Fe:
        if i != j:
            expr2.addTerms(1, y[i, j])
    model.addConstr(expr1 == expr2)

# 2.5
for i in F:
    expr = LinExpr(0)
    for j in Fe:
        if i != j:
            expr.addTerms(1, y[i, j])
    model.addConstr(expr == 1)


# Second stage
# 2.6
for omega in OMEGA:
    for i in F:
        for j in F:
            if i != j:
                model.addConstr(t[omega, j, d] >= t[omega, i, d] + rw_separation_matrix[i - 1][j - 1] - M * (1 - y[i, j]))

# 2.7
for i in F:
    for j in F:
        if i != j:
            i_path, j_path = copy.deepcopy(Path_list[F_path[i - 1] - 1]), copy.deepcopy(Path_list[F_path[j - 1] - 1])
            ij_N_list = list(set(i_path).intersection(set(j_path)))
            for u in ij_N_list:
                if u != d:
                    for omega in OMEGA:
                        model.addConstr(z[omega, i, j, u] + z[omega, j, i, u] == 1)


# 2.8
for i in F:
    oi = Path_list[F_path[i - 1] - 1][0]
    for omega in OMEGA:
            model.addConstr(t[omega, i, oi] >= scenario_arrival_time[omega - 1][i -1])

# 2.9
for i in F:
    path = Path_list[F_path[i - 1] - 1]

    u_counter = 0
    while u_counter < len(path) - 1:
        u, v = path[u_counter], path[u_counter + 1]
        traversing_time = distance_matrix[u][v] / F_speed[i - 1]
        for omega in OMEGA:
            model.addConstr(t[omega, i, u] + traversing_time == t[omega, i, v])

        u_counter += 1


# 2.10
for i in F:
    for j in F:
        if i != j:

            separation_distance = separation_matrix[i - 1][j - 1]
            separation_time = separation_distance / F_speed[j - 1]

            i_path, j_path = copy.deepcopy(Path_list[F_path[i - 1] - 1]), copy.deepcopy(Path_list[F_path[j - 1] - 1])
            ij_N_list = list(set(i_path).intersection(set(j_path)))
            for u in ij_N_list:
                if u != d:
                    for omega in OMEGA:

                        model.addConstr(t[omega, j, u] >= t[omega, i, u] + separation_time - M * (1 - z[omega, i, j, u]))


for omega in OMEGA:
    for i in F:
        oi = copy.deepcopy(Path_list[F_path[i - 1] - 1][0])
        model.addConstr(D[omega, i] >= t[omega, i, oi] - scenario_arrival_time[omega - 1][i - 1])










# Knapsack inequality
expr = LinExpr(0)
for omega in OMEGA:
    for i in F:
        expr.addTerms(scenario_weight * F_weight[i - 1], D[omega, i])
model.addConstr(expr <= UB)













# 3.5 solve the model
model.optimize()

# 打印结果
# print("\n\n-----optimal value-----")
# print(model.Objval)
info = model.status
objective_value = model.Objval
lower_bound = model.getAttr("ObjBoundC")
print(objective_value)
print(info)


'''print('\n')
for key in y.keys():
    if y[key].x > 0:
        print(y[key].VarName + ' = ', y[key].x)
print('\n')
for key in t.keys():
    if t[key].x > 0:
        print(t[key].VarName + ' = ', t[key].x)
print('\n')
for key in z.keys():
    if z[key].x > 0:
        print(z[key].VarName + ' = ', z[key].x)
print('\n')
for key in D.keys():
    if D[key].x > 0:
        print(D[key].VarName + ' = ', D[key].x)
print('\n')'''


Yij_list = []
for key in y.keys():
    if y[key].x > 0.9:
        Yij_list.append([key[0], key[1]])
#print(Yij_list)

aircraft_sequence = []
origin_node = N[0]
destination_node = N[-1]
current_node = origin_node
while current_node != destination_node:
    for arc in Yij_list:
        if arc[0] == current_node:
            aircraft_sequence.append(copy.deepcopy(arc))
            current_node = copy.deepcopy(arc[1])
            break
print(aircraft_sequence)
print(model.Runtime)
