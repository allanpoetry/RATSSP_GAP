
from gurobipy import *
import copy
from gurobipy import *

def Subproblem(Yij_list_2, arrival_time, F, F_weight, F_path, F_speed, Path_list, d, M, rw_separation_matrix, distance_matrix, separation_matrix):

    # 3 BUILD THE MODEL
    model = Model('SP')
    model.setParam('OutputFlag', 0)

    z = {}
    t = {}
    D = {}

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

    # Second stage
    # 2.6

    for arc in Yij_list_2:
        i, j = copy.deepcopy(arc[0]), copy.deepcopy(arc[1])
        model.addConstr(t[j, d] >= t[i, d] + rw_separation_matrix[i - 1][j - 1])

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

    objective_value = model.Objval

    return objective_value


