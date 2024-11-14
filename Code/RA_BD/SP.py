import copy
from gurobipy import *

def SP(F, F_E, F_D, F_C, arrival_time, occupy_time, C_E, C_D, C_C, M, b, Binary_Yij, test_Pi, test_Sigma, test_Tau):

    Pi_list, Sigma_list, Tau_list = copy.deepcopy(test_Pi), copy.deepcopy(test_Sigma), copy.deepcopy(test_Tau)

    # 3 BUILD THE MODEL
    model = Model('dual_SP')
    model.setParam('OutputFlag', 0)

    pi = {}
    sigma = {}
    tau = {}

    for i in F:
        name = 'pi_' + str(i)
        pi[i] = model.addVar(vtype=GRB.CONTINUOUS, name=name)
        name = 'sigma_' + str(i)
        sigma[i] = model.addVar(lb=-GRB.INFINITY, ub=0, vtype=GRB.CONTINUOUS, name=name)

    for i in F:
        for j in F:
            if i != j:
                name = 'tau_' + str(i) + '_' + str(j)
                tau[i, j] = model.addVar(lb=-GRB.INFINITY, ub=0, vtype=GRB.CONTINUOUS, name=name)

    # 15a
    obj = LinExpr(0)
    for i in F:
        obj.addTerms(arrival_time[i - 1], pi[i])
        obj.addTerms(arrival_time[i - 1], sigma[i])
    for i in F:
        for j in F:
            if i != j:
                obj.addTerms((M * (1 - Binary_Yij[i][j])) - occupy_time[i - 1] - b, tau[i, j])
    model.setObjective(obj, GRB.MAXIMIZE)
    model.params.InfUnbdInfo = 1

    # 15b
    for i in F:
        expr1, expr2 = LinExpr(0), LinExpr(0)
        for j in F:
            if i != j:
                expr1.addTerms(1, tau[i, j])
                expr2.addTerms(1, tau[j, i])
        model.addConstr(pi[i] + sigma[i] + expr1 - expr2 <= 0)

    # 15c
    for i in F:
        if i in F_E:
            model.addConstr(- sigma[i] <= C_E)
        elif i in F_D:
            model.addConstr(- sigma[i] <= C_D)
        elif i in F_C:
            model.addConstr(- sigma[i] <= C_C)


    # solve the model
    model.optimize()

    for key in pi.keys():
        Pi_list[key] += pi[key].x
    for key in sigma.keys():
        Sigma_list[key] += sigma[key].x
    for key in tau.keys():
        Tau_list[key[0]][key[1]] += tau[key].x


    objective_value = model.Objval
    return_result = [objective_value, Pi_list, Sigma_list, Tau_list]


    return return_result

