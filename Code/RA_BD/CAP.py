
from gurobipy import *

def CAP(scenario_weight, OMEGA, second_stage_obj_list, Lambda, Alpha):

    # 3 BUILD THE MODEL
    model = Model('CAP')
    model.setParam('OutputFlag', 0)

    # Decision variables
    Delta = {}

    for omega in OMEGA:
        name = 'Delta_' + str(omega)
        Delta[omega] = model.addVar(vtype=GRB.CONTINUOUS, name=name)

    name = 'Beta'
    Beta = model.addVar(lb=-float('inf'), ub=float('inf'), vtype=GRB.CONTINUOUS, name=name)


    # 16a
    obj = LinExpr(0)
    obj.addTerms(Lambda, Beta)
    for omega in OMEGA:
        obj.addTerms(scenario_weight * (Lambda / (1 - Alpha)), Delta[omega])
    model.setObjective(obj, GRB.MINIMIZE)

    # Constraints
    # 16b
    for omega in OMEGA:
        model.addConstr(second_stage_obj_list[omega - 1] - Beta <= Delta[omega])

    # 3.5 solve the model
    model.optimize()

    # 打印结果
    # print("\n\n-----optimal value-----")
    # print(model.Objval)
    objective_value = model.Objval


    return objective_value


