
import time, copy
from SGAP.Solution_methods.RA_BD.MP import MP
from SGAP.Solution_methods.RA_BD.SP import SP
from SGAP.Solution_methods.RA_BD.subtour_check import subtour_check
from SGAP.Solution_methods.RA_BD.CAP import CAP


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








Binary_Yij = []
i_counter = 0
while i_counter < len(N):
    sub_sy = []
    j_counter = 0
    while j_counter < len(N):
        sub_sy.append(0)
        j_counter += 1
    i_counter += 1
    Binary_Yij.append(sub_sy)


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






UB = 1000000000
LB = 0
GAP = UB - LB

iteration_counter = 1

start_time = time.time()
CPU_time = time.time() - start_time

best_Xgi_list = []
best_Ygij_list = []




while GAP > 0.0000001:

    print(iteration_counter, CPU_time)

    # Solve MP
    MP_result = MP(K_all, K, K_D, K_C, r, F, Fs, Fe, F_E, F_D, C_apron, OMEGA, scenario_weight, scenario_arrival_time, occupy_time, M, b, Lambda, Alpha, Optimality_cuts_info, Subtour_elimination_cuts, Binary_Yij, CPU_time)

    # Solve SPs
    test_LB = copy.deepcopy(MP_result[0])
    print(test_LB)
    if LB < test_LB:
        LB = test_LB

    first_stage_obj = copy.deepcopy(MP_result[1])
    Ygij_list = copy.deepcopy(MP_result[2])
    test_Binary_Yij = copy.deepcopy(MP_result[3])
    Xgi_list = copy.deepcopy(MP_result[4])

    print(test_LB)
    print(first_stage_obj)
    print(Ygij_list)
    print(Xgi_list)
    print(test_Binary_Yij)

    subtour_counter = 0
    for Yij in Ygij_list:
        subtour_list = subtour_check(Yij, N)
        if len(subtour_list) > 0:
            subtour_counter = 1
        for sl in subtour_list:
            Subtour_elimination_cuts.append(sl)

    # 如果没有子路径，计算SP
    if subtour_counter == 0:

        second_stage_obj_list = []
        Zeta_optimality_cut_info = []

        for omega in OMEGA:
            arrival_time = copy.deepcopy(scenario_arrival_time[omega - 1])
            SP_result = SP(F, F_E, F_D, F_C, arrival_time, occupy_time, C_E, C_D, C_C, M, b, test_Binary_Yij, test_Pi, test_Sigma,  test_Tau)

            second_stage_obj_list.append(copy.deepcopy(SP_result[0]))
            Zeta_optimality_cut_info.append(copy.deepcopy(SP_result[1:]))

        if Zeta_optimality_cut_info not in Optimality_cuts_info:
            Optimality_cuts_info.append(copy.deepcopy(Zeta_optimality_cut_info))

        second_stage_obj = scenario_weight * sum(second_stage_obj_list)

        print(second_stage_obj_list)

        CVaR_value = CAP(scenario_weight, OMEGA, second_stage_obj_list, Lambda, Alpha)

        test_UB = (1 + Lambda) * first_stage_obj + second_stage_obj + CVaR_value
        if test_UB < UB:
            UB = test_UB
            best_Xgi_list = copy.deepcopy(Xgi_list)
            best_Ygij_list = copy.deepcopy(Ygij_list)


    GAP = UB - LB
    print(UB, LB, GAP)
    print(len(Optimality_cuts_info), len(Subtour_elimination_cuts))

    iteration_counter += 1

    print('\n')
    CPU_time = time.time() - start_time

    if CPU_time > CPU_time_limit:
        break









print('\n')
# 需要返回的内容
# optimlaity gap
if abs(UB - LB) >= 0.0001:
    mip_gap = (UB - LB) / UB
elif abs(UB - LB) < 0.0001:
    mip_gap = 0
print(mip_gap)

# 计算时间
CPU_time = time.time() - start_time
print(CPU_time)

# Objective value
print(UB)


# Solution
print("Xk_list = " + str(best_Xgi_list))
print("Ykij_list = " + str(best_Ygij_list))


#print(upper_bound_list)
#print(lower_bound_list)




