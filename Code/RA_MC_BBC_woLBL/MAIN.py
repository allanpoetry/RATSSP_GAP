from gurobipy import *
import time, copy
from SGAP.Solution_methods.RA_BD.SP import SP
from SGAP.Solution_methods.RA_BD.subtour_check import subtour_check


# 20 Contact gates
K_E = [1, 2, 3, 4]
K_D = [5, 6, 7, 8, 9, 10, 11, 12, 13]
K_C = [14, 15, 16, 17, 18, 19, 20]
r = [21]
K = K_E + K_D + K_C
K_all = K + r



# S1
F = [1, 2, 3, 4, 5, 6, 7, 8, 9]
F_size  = [1, 1, 1, 2, 2, 1, 1, 1, 1]
F_E = []
F_D = [4, 5]
F_C = [1, 2, 3, 6, 7, 8, 9]
occupy_time  = [86, 64, 68, 67, 62, 68, 84, 111, 64]
scenario_weight = 0.02
OMEGA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
scenario_arrival_time = [[1450, 1460, 1438, 1437, 1450, 1453, 1457, 1445, 1463], [1445, 1436, 1455, 1436, 1468, 1457, 1436, 1452, 1496], [1449, 1486, 1428, 1438, 1470, 1447, 1515, 1454, 1462], [1434, 1433, 1450, 1441, 1451, 1460, 1442, 1448, 1519], [1442, 1493, 1445, 1431, 1436, 1475, 1456, 1472, 1481], [1439, 1446, 1425, 1458, 1467, 1451, 1490, 1487, 1495], [1438, 1440, 1444, 1450, 1451, 1458, 1450, 1479, 1486], [1432, 1439, 1442, 1457, 1443, 1461, 1476, 1468, 1495], [1412, 1445, 1446, 1473, 1444, 1442, 1463, 1462, 1487], [1418, 1435, 1439, 1458, 1460, 1453, 1464, 1470, 1470], [1461, 1435, 1465, 1438, 1449, 1476, 1474, 1475, 1463], [1439, 1458, 1430, 1493, 1439, 1461, 1460, 1469, 1467], [1452, 1424, 1428, 1442, 1450, 1459, 1513, 1460, 1472], [1423, 1440, 1500, 1460, 1493, 1443, 1449, 1451, 1473], [1436, 1479, 1427, 1458, 1454, 1436, 1473, 1460, 1473], [1424, 1449, 1441, 1444, 1492, 1483, 1492, 1473, 1460], [1440, 1445, 1430, 1463, 1450, 1438, 1451, 1473, 1453], [1434, 1434, 1456, 1429, 1446, 1492, 1440, 1481, 1475], [1440, 1434, 1427, 1451, 1440, 1512, 1459, 1490, 1475], [1446, 1417, 1454, 1489, 1459, 1447, 1457, 1462, 1463], [1425, 1453, 1478, 1451, 1425, 1478, 1450, 1485, 1473], [1451, 1456, 1435, 1450, 1492, 1477, 1459, 1477, 1481], [1462, 1424, 1467, 1449, 1435, 1460, 1447, 1468, 1486], [1446, 1488, 1454, 1447, 1458, 1480, 1451, 1484, 1471], [1484, 1427, 1433, 1447, 1441, 1464, 1472, 1486, 1502], [1426, 1440, 1421, 1466, 1455, 1460, 1460, 1495, 1452], [1438, 1469, 1425, 1483, 1449, 1493, 1447, 1470, 1463], [1426, 1476, 1442, 1461, 1439, 1481, 1450, 1500, 1475], [1440, 1425, 1460, 1450, 1457, 1459, 1471, 1444, 1461], [1473, 1403, 1446, 1437, 1444, 1471, 1455, 1476, 1461], [1418, 1452, 1425, 1443, 1458, 1442, 1430, 1472, 1475], [1440, 1435, 1429, 1473, 1435, 1466, 1449, 1463, 1506], [1412, 1445, 1436, 1444, 1464, 1476, 1456, 1485, 1514], [1435, 1431, 1450, 1429, 1442, 1441, 1450, 1447, 1475], [1458, 1477, 1477, 1478, 1444, 1468, 1447, 1461, 1468], [1440, 1446, 1466, 1482, 1436, 1453, 1462, 1463, 1471], [1439, 1448, 1407, 1478, 1436, 1479, 1515, 1459, 1485], [1427, 1433, 1438, 1450, 1455, 1450, 1446, 1488, 1510], [1420, 1442, 1483, 1427, 1499, 1443, 1459, 1469, 1478], [1414, 1495, 1433, 1472, 1468, 1456, 1453, 1476, 1462], [1448, 1446, 1437, 1441, 1449, 1428, 1453, 1449, 1474], [1437, 1464, 1439, 1448, 1455, 1458, 1461, 1501, 1478], [1438, 1432, 1435, 1428, 1450, 1437, 1451, 1481, 1475], [1443, 1436, 1468, 1418, 1449, 1450, 1486, 1488, 1475], [1443, 1489, 1454, 1445, 1451, 1476, 1491, 1441, 1472], [1433, 1418, 1480, 1450, 1457, 1467, 1511, 1463, 1507], [1486, 1437, 1440, 1459, 1449, 1456, 1481, 1482, 1459], [1456, 1453, 1455, 1469, 1446, 1468, 1440, 1511, 1463], [1456, 1438, 1442, 1471, 1459, 1447, 1457, 1479, 1481], [1451, 1445, 1491, 1472, 1445, 1458, 1452, 1458, 1480]]



CPU_time_limit = 3600

# 1 Data input
Lambda = 1
Alpha = 0.9



# 1 Data input

#print(len(scenario_time_list[0]))
det = len(F) + 1        # dummy_ending_task
Fs = [0] + F
Fe = F + [det]
N = [0] + F + [det]




C_apron = 2000
C_E = 40
C_D = 30
C_C = 20


b = 10



max_at= 0
for sat in scenario_arrival_time:
    for at in sat:
        if at > max_at:
            max_at = at
M = (max_at + sum(occupy_time) + b * len(F)) + 0.00001
print(M)







Binary_Ykij = []
k_counter = 0
while k_counter < len(K):
    sub_binary_Yij = []
    i_counter = 0
    while i_counter < len(N):
        sub_sy = []
        j_counter = 0
        while j_counter < len(N):
            sub_sy.append(0)
            j_counter += 1
        i_counter += 1
        sub_binary_Yij.append(sub_sy)
    k_counter += 1
    Binary_Ykij.append(copy.deepcopy(sub_binary_Yij))


test_Pi = []
test_Sigma = []
test_Tau = []

i_counter = 0
while i_counter < len(N):
    test_Pi.append(0)
    test_Sigma.append(0)
    i_counter += 1

i_counter = 0
while i_counter < len(N):
    sub_list = []
    j_counter = 0
    while j_counter < len(N):
        sub_list.append(0)
        j_counter += 1
    test_Tau.append(copy.deepcopy(sub_list))
    i_counter += 1
#print(test_Sum_Psi)


# Benders optimality cuts list
Subtour_elimination_cuts = []
Optimality_cuts_info = []



founded_cuts = []











UB = 1000000000
LB = 0
GAP = UB - LB

iteration_counter = 1

start_time = time.time()
CPU_time = time.time() - start_time




# 3 BUILD THE MODEL
model = Model('MP')
model.Params.timelimit = CPU_time_limit
#model.setParam('OutputFlag', 0)
model.Params.MIPGap = 0.0000001


model._Optimality_cuts_counter = 0




# Decision variables
x = {}
y = {}
theta = {}

upsilon = {}

for k in K_all:
    for i in F:
        name = 'x_' + str(k) + '_' + str(i)
        x[k, i] = model.addVar(vtype=GRB.BINARY, name=name)

for k in K:
    for i in Fs:
        for j in Fe:
            if i != j:
                name = 'y_' + str(k) + '_' + str(i) + '_' + str(j)
                y[k, i, j] = model.addVar(vtype=GRB.BINARY, name=name)

for k in K:
    for omega in OMEGA:
        name = 'theta_' + str(k) + '_' + str(omega)
        theta[k, omega] = model.addVar(vtype=GRB.CONTINUOUS, name=name)

for omega in OMEGA:
    name = 'upsilon_' + str(omega)
    upsilon[omega] = model.addVar(vtype=GRB.CONTINUOUS, name=name)

name = 'eta'
eta = model.addVar(lb=-float('inf'), ub=float('inf'), vtype=GRB.CONTINUOUS, name=name)

# 18a
obj = LinExpr(0)
for k in r:
    for i in F:
        obj.addTerms((1 + Lambda) * C_apron, x[k, i])
for k in K:
    for omega in OMEGA:
        obj.addTerms(scenario_weight, theta[k, omega])
obj.addTerms(Lambda, eta)
for omega in OMEGA:
    obj.addTerms(scenario_weight * (Lambda / (1 - Alpha)), upsilon[omega])
model.setObjective(obj, GRB.MINIMIZE)
model.Params.lazyConstraints = 1

# First-stage problem
# 1b
for i in F:
    expr = LinExpr(0)
    for k in K_all:
        expr.addTerms(1, x[k, i])
    model.addConstr(expr == 1)
# 1c
for k in K_D + K_C:
    for i in F_E:
        model.addConstr(x[k, i] <= 0)
# 1d
for k in K_C:
    for i in F_D:
        model.addConstr(x[k, i] <= 0)
# 1e
for k in K:
    for i in F:
        expr = LinExpr(0)
        for j in Fe:
            if i != j:
                expr.addTerms(1, y[k, i, j])
        model.addConstr(expr == x[k, i])
# 1f
for k in K:
    expr = LinExpr(0)
    for j in Fe:
        expr.addTerms(1, y[k, Fs[0], j])
    model.addConstr(expr == 1)
# 1g
for k in K:
    expr = LinExpr(0)
    for i in Fs:
        expr.addTerms(1, y[k, i, Fe[-1]])
    model.addConstr(expr == 1)
# 1h
for k in K:
    for i in F:
        expr1, expr2 = LinExpr(0), LinExpr(0)
        for j in Fs:
            if i != j:
                expr1.addTerms(1, y[k, j, i])
        for j in Fe:
            if i != j:
                expr2.addTerms(1, y[k, i, j])
        model.addConstr(expr1 == expr2)

# 18b
for omega in OMEGA:
    expr = LinExpr(0)
    for k in K:
        expr.addTerms(1, theta[k, omega])
    model.addConstr(upsilon[omega] >= expr - eta)



# 定义Callback函数
def mycallback(model, where):
    if where == GRB.Callback.MIPSOL:
        # 获取当前节点的变量取值
        x_val = model.cbGetSolution(x)
        y_val = model.cbGetSolution(y)

        Xki_list = []
        k_counter = 0
        while k_counter < len(K):
            k_list = []
            for key in x_val.keys():
                if key[0] == k_counter + 1:
                    if round(x_val[key], 6) >= 0.9:
                        k_list.append(key[1])
            k_counter += 1
            Xki_list.append(k_list)

        Ykij_list = []
        for k in K:
            sub_yij_list = []
            for key in y_val.keys():
                if key[0] == k:
                    if y_val[key] > 0.9:
                        sub_yij_list.append([key[1], key[2]])
            Ykij_list.append(copy.deepcopy(sub_yij_list))

        test_Binary_Ykij = copy.deepcopy(Binary_Ykij)
        # Update Y
        for key in y_val.keys():
            for k in K:
                if key[0] == k:
                    if key[1] != Fs[0]:
                        if key[2] != Fe[-1]:
                            if round(y_val[key]) > 0.9:
                                test_Binary_Ykij[key[0] - 1][key[1]][key[2]] += 1


        '''print(Xgi_list)
        print(Ygij_list)
        print('\n')'''

        subtour_counter_list = []
        for Yij in Ykij_list:
            subtour_list = subtour_check(Yij, N)
            if len(subtour_list) > 0:
                subtour_counter_list.append(1)
            else:
                subtour_counter_list.append(0)
            for sl in subtour_list:
                for k in K:
                    expr = LinExpr(0)
                    for arc in sl:
                        expr.addTerms(1, y[k, arc[0], arc[1]])
                    model.cbLazy(expr <= len(sl) - 1)


        gate_counter = 0
        while gate_counter < len(subtour_counter_list):

            if subtour_counter_list[gate_counter] == 0:

                sub_F = copy.deepcopy(Xki_list[gate_counter])
                test_Binary_Yij = copy.deepcopy(test_Binary_Ykij[gate_counter])

                if sub_F not in founded_cuts:
                    founded_cuts.append(copy.deepcopy(test_Binary_Yij))

                    E_counter, D_counter, C_counter = 0, 0, 0
                    for aircraft in sub_F:
                        if aircraft in F_E:
                            E_counter = 1
                            break
                    if E_counter == 0:
                        for aircraft in sub_F:
                            if aircraft in F_D:
                                D_counter = 1
                                break
                    if E_counter == 0 and D_counter == 0:
                        C_counter = 1

                    if E_counter == 1:
                        gate_info_list = copy.deepcopy(K_E)
                    elif D_counter == 1:
                        gate_info_list = copy.deepcopy(K_E + K_D)
                    elif C_counter == 1:
                        gate_info_list = K

                    for omega in OMEGA:
                        arrival_time = copy.deepcopy(scenario_arrival_time[omega - 1])
                        SP_result = SP(sub_F, F_E, F_D, F_C, arrival_time, occupy_time, C_E, C_D, C_C, M, b,
                                       test_Binary_Yij, test_Pi, test_Sigma, test_Tau)
                        optimality_cut = copy.deepcopy(SP_result[1:])

                        for k in gate_info_list:
                            pi_info = copy.deepcopy(optimality_cut[0])
                            sigma_info = copy.deepcopy(optimality_cut[1])
                            tau_info = copy.deepcopy(optimality_cut[2])

                            para = 0
                            for i in sub_F:
                                para += scenario_arrival_time[omega - 1][i - 1] * pi_info[i]
                                para += scenario_arrival_time[omega - 1][i - 1] * sigma_info[i]
                                for j in sub_F:
                                    if i != j:
                                        para += (M - occupy_time[i - 1] - b) * tau_info[i][j]

                            expr = LinExpr(0)
                            for i in sub_F:
                                for j in sub_F:
                                    if i != j:
                                        expr.addTerms(tau_info[i][j], y[k, i, j])

                            model._Optimality_cuts_counter += 1
                            model.cbLazy(theta[k, omega] >= para - M * expr)
                
            gate_counter += 1



# 3.5 solve the model
model.optimize(mycallback)


# 打印结果
# print("\n\n-----optimal value-----")
# print(model.Objval)
objective_value = model.Objval


print('\n')
# 需要返回的内容
# optimlaity gap
mip_gap = model.MIPGap
print(mip_gap)

# 计算时间
CPU_time = time.time() - start_time
print(CPU_time)

# Objective value
print(objective_value)


# Solution
Xk_list = []
k_counter = 0
while k_counter < len(K_all):
    k_list = []
    for key in x.keys():
        if key[0] == k_counter + 1:
            if round(x[key].x, 6) >= 0.9:
                k_list.append(key[1])
    k_counter += 1
    Xk_list.append(k_list)
print("Xk_list = " + str(Xk_list))

Ykij_list = []
for k in K:
    sub_yij_list = []
    for key in y.keys():
        if key[0] == k:
            if y[key].x > 0.9:
                sub_yij_list.append([key[1], key[2]])
    Ykij_list.append(copy.deepcopy(sub_yij_list))
print("Ykij_list = " + str(Ykij_list))


#print(upper_bound_list)
#print(lower_bound_list)









