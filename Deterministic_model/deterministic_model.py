import copy
from gurobipy import *
from JO_ALP_TATFP.ORIGINAL_PROBLEM.SMG import SMG

# Distance information
distance_matrix = [[1000000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0],
                   [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 31.3, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0],
                   [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 90.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 92.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 75.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 80.1, 1000000.0, 79.2, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 85.3, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 49.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 96.5, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 84.5, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 27.1, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 24.2, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 27.1, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 87.1, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 54.4, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 73.9, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 46.4, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 51.2, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 67.3, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 9.6, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 44.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 33.6, 1000000.0, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 12.2, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 35.6, 1000000.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 22.0, 1000000.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 0.0], [1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0, 1000000.0]]


# 10 fix, 26 paths
Path_list = [[1, 11, 15, 22, 24, 25],
            [2, 11, 15, 22, 24, 25],
            [3, 11, 15, 22, 24, 25],
            [4, 12, 16, 20, 22, 24, 25],
            [5, 12, 16, 20, 22, 24, 31],
            [6, 13, 14, 19, 25, 27, 30, 31],
            [7, 13, 14, 19, 25, 27, 30, 31],
            [8, 21, 26, 28, 30, 31],
            [9, 23, 26, 28, 30, 31],
            [10, 28, 30, 31]]
d = 31


# Data
F = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
F_size = [1, 2, 2, 2, 2, 3, 1, 2, 3, 2]
F_speed = [0.066, 0.062, 0.062, 0.062, 0.062, 0.069, 0.066, 0.062, 0.069, 0.062]
F_weight = [2, 2, 1, 3, 3, 3, 3, 1, 3, 1]
F_path = [7, 7, 7, 9, 8, 1, 1, 2, 6, 5]
separation_matrix = [[0, 5, 5, 5, 5, 7, 0, 5, 7, 5], [3, 0, 0, 0, 0, 5, 3, 0, 5, 0], [3, 0, 0, 0, 0, 5, 3, 0, 5, 0], [3, 0, 0, 0, 0, 5, 3, 0, 5, 0], [3, 0, 0, 0, 0, 5, 3, 0, 5, 0], [3, 3, 3, 3, 3, 0, 3, 3, 0, 3], [0, 5, 5, 5, 5, 7, 0, 5, 7, 5], [3, 0, 0, 0, 0, 5, 3, 0, 5, 0], [3, 3, 3, 3, 3, 0, 3, 3, 0, 3], [3, 0, 0, 0, 0, 5, 3, 0, 5, 0]]
scenario_weight = 1.0
OMEGA = [1]
arrival_time = [1876, 2006, 2097, 2105, 2240, 2287, 2467, 2661, 2855, 2958]


det = len(F) + 1        # dummy_ending_task
Fs = [0] + F
Fe = F + [det]
N = [0] + F + [det]

rw_separation_matrix = SMG(F, F_size)

M = 10000


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
                    name = 'z_'  + str(i) + '_' + str(j) + '_' + str(u)
                    z[i, j, u] = model.addVar(vtype=GRB.BINARY, name=name)
                
for i in F:
    for u in Path_list[F_path[i - 1] - 1]:
            name = 't_' + str(i) + '_' + str(u)
            t[i, u] = model.addVar(vtype=GRB.CONTINUOUS, name=name)

for i in F:
    name = 'D_' + str(i)
    D[i] = model.addVar(vtype=GRB.CONTINUOUS, name=name)


# Objective function
obj = LinExpr(0)
for i in F:
    obj.addTerms(F_weight[i - 1], D[i])
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
for i in F:
    for j in F:
        if i != j:
            model.addConstr(t[j, d] >= t[i, d] + rw_separation_matrix[i - 1][j - 1] - M * (1 - y[i, j]))

# 2.7
for i in F:
    for j in F:
        if i != j:
            i_path, j_path = copy.deepcopy(Path_list[F_path[i - 1] - 1]), copy.deepcopy(Path_list[F_path[j - 1] - 1])
            ij_N_list = list(set(i_path).intersection(set(j_path)))
            print(ij_N_list)
            for u in ij_N_list:
                if u != d:
                    model.addConstr(z[i, j, u] + z[j, i, u] == 1)


# 2.8
for i in F:
    oi = Path_list[F_path[i - 1] - 1][0]
    model.addConstr(t[i, oi] >= arrival_time[i -1])

# 2.9
for i in F:
    path = Path_list[F_path[i - 1] - 1]

    u_counter = 0
    while u_counter < len(path) - 1:
        u, v = path[u_counter], path[u_counter + 1]
        traversing_time = distance_matrix[u][v] / F_speed[i - 1]
        model.addConstr(t[i, u] + traversing_time == t[i, v])
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
                    model.addConstr(t[j, u] >= t[i, u] + separation_time - M * (1 - z[i, j, u]))

for i in F:
    oi = copy.deepcopy(Path_list[F_path[i - 1] - 1][0])
    model.addConstr(D[i] >= t[i, oi] - arrival_time[i - 1])


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


print('\n')
for key in y.keys():
    if y[key].x > 0:
        print(y[key].VarName + ' = ', y[key].x)
print('\n')
'''for key in t.keys():
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