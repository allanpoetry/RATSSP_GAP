from gurobipy import *
import copy, random, time


def MP(K_all, K, K_D, K_C, r, F, Fs, Fe, F_E, F_D, C_apron, OMEGA, scenario_weight, scenario_arrival_time, occupy_time, M, b, Lambda, Alpha, Optimality_cuts_info, Subtour_elimination_cuts, Binary_Yij, CPU_time):


    test_Binary_Yij = copy.deepcopy(Binary_Yij)


    # 3 BUILD THE MODEL
    model = Model('MP')
    model.Params.timelimit = 3650 - CPU_time
    model.setParam('OutputFlag', 0)
    model.Params.MIPGap = 0.0000001

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


    for omega in OMEGA:
        name = 'theta_'  + str(omega)
        theta[omega] = model.addVar(vtype=GRB.CONTINUOUS, name=name)


    for omega in OMEGA:
        name = 'upsilon_' + str(omega)
        upsilon[omega] = model.addVar(vtype=GRB.CONTINUOUS, name=name)

    name = 'eta'
    eta = model.addVar(lb=-float('inf'), ub=float('inf'), vtype=GRB.CONTINUOUS, name=name)


    obj = LinExpr(0)
    for k in r:
        for i in F:
            obj.addTerms((1 + Lambda) * C_apron, x[k, i])
    for omega in OMEGA:
        obj.addTerms(scenario_weight, theta[omega])
    # CVaR
    obj.addTerms(Lambda, eta)
    for omega in OMEGA:
        obj.addTerms(scenario_weight * (Lambda / (1 - Alpha)), upsilon[omega])
    model.setObjective(obj, GRB.MINIMIZE)


    # First stage decisions
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

    # 12b
    for omega in OMEGA:
        model.addConstr(theta[omega] - eta <= upsilon[omega])

    # 13: DFJ subtour elimination cuts
    for subtour in Subtour_elimination_cuts:
        for k in K:
            expr = LinExpr(0)
            for arc in subtour:
                expr.addTerms(1, y[k, arc[0], arc[1]])
            model.addConstr(expr <= len(subtour) - 1)


    # 17: Benders optimality cuts
    for cut_info in Optimality_cuts_info:

        for omega in OMEGA:
            pi_info = copy.deepcopy(cut_info[omega - 1][0])
            sigma_info = copy.deepcopy(cut_info[omega - 1][1])
            tau_info = copy.deepcopy(cut_info[omega - 1][2])

            para = 0
            for i in F:
                para += scenario_arrival_time[omega - 1][i - 1] * pi_info[i]
                para += scenario_arrival_time[omega - 1][i - 1] * sigma_info[i]
                for j in F:
                    if i != j:
                        para += (M - occupy_time[i - 1] - b) * tau_info[i][j]

            expr = LinExpr(0)
            for k in K:
                for i in F:
                    for j in F:
                        if i != j:
                            expr.addTerms(tau_info[i][j], y[k, i, j])

            model.addConstr(theta[omega] >= para - M * expr)




    # solve the model
    model.optimize()

    # 打印结果
    # print("\n\n-----optimal value-----")
    # print(model.Objval)
    objective_value = model.Objval
    # print(objective_value)
    # info = model.status

    '''
    for key in x.keys():
        if x[key].x > 0:
            print(x[key].VarName + ' = ', x[key].x)
    print('\n')
    for key in y.keys():
        if y[key].x > 0:
            print(y[key].VarName + ' = ', y[key].x)
    print('\n')
    '''

    Xk_list = []
    k_counter = 0
    while k_counter < len(K):
        k_list = []
        for key in x.keys():
            if key[0] == k_counter + 1:
                if round(x[key].x, 6) >= 0.9:
                    k_list.append(key[1])
        k_counter += 1
        Xk_list.append(k_list)

    # Update Y
    for key in y.keys():
        test_Binary_Yij[key[1]][key[2]] += round(y[key].x)

    Ykij_list = []
    for k in K:
        sub_yij_list = []
        for key in y.keys():
            if key[0] == k:
                if y[key].x > 0.9:
                    sub_yij_list.append([key[1], key[2]])
        Ykij_list.append(copy.deepcopy(sub_yij_list))

    apron_list = []
    for key in x.keys():
        if x[key].x > 0.9:
            if key[0] in r:
                apron_list.append([key[0], key[1]])
    first_stage_obj = C_apron * len(apron_list)


    return_list = [objective_value, first_stage_obj, Ykij_list, test_Binary_Yij, Xk_list]

    return return_list
