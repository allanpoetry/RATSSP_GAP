import copy
from gurobipy import *

def KI(N, Fs, Fe, F, F_weight, F_path, F_speed, arrival_time, Path_list, d, M, rw_separation_matrix, distance_matrix, separation_matrix):

    # 3 BUILD THE MODEL
    model = Model('JAT')
    model.setParam('OutputFlag', 0)

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
                i_path, j_path = copy.deepcopy(Path_list[F_path[i - 1] - 1]), copy.deepcopy(
                    Path_list[F_path[j - 1] - 1])
                ij_N_list = list(set(i_path).intersection(set(j_path)))
                for u in ij_N_list:
                    if u != d:
                        name = 'z_' + str(i) + '_' + str(j) + '_' + str(u)
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
                i_path, j_path = copy.deepcopy(Path_list[F_path[i - 1] - 1]), copy.deepcopy(
                    Path_list[F_path[j - 1] - 1])
                ij_N_list = list(set(i_path).intersection(set(j_path)))
                for u in ij_N_list:
                    if u != d:
                        model.addConstr(z[i, j, u] + z[j, i, u] == 1)

    # 2.8
    for i in F:
        oi = Path_list[F_path[i - 1] - 1][0]
        model.addConstr(t[i, oi] >= arrival_time[i - 1])

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

                i_path, j_path = copy.deepcopy(Path_list[F_path[i - 1] - 1]), copy.deepcopy(
                    Path_list[F_path[j - 1] - 1])
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
    #objective_value = model.Objval

    Yij_list = []
    for key in y.keys():
        if y[key].x > 0.9:
            Yij_list.append([key[0], key[1]])

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


    aircraft_sequence = copy.deepcopy(aircraft_sequence[1:-1])

    return aircraft_sequence




