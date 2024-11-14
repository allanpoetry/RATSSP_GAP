from gurobipy import *
import copy, random, time


# 8 Contact gates
K_E = [1, 2]
K_D = [3, 4, 5, 6, 7]
K_C = [8]
r = [9]
K = K_E + K_D + K_C
K_all = K + r


# 1
F = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
F_size = [2, 2, 2, 2, 2, 2, 3, 1, 1, 2, 2, 1, 3, 3, 2, 3, 2, 2, 1, 2]
F_E = [8, 9, 12, 19]
F_D = [1, 2, 3, 4, 5, 6, 10, 11, 15, 17, 18, 20]
F_C = [7, 13, 14, 16]
occupy_time = [50, 60, 53, 51, 42, 50, 49, 60, 53, 53, 54, 51, 48, 44, 41, 40, 53, 36, 35, 37]
scenario_weight = 0.02
OMEGA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
scenario_arrival_time = [[187, 198, 201, 269, 299, 305, 311, 311, 313, 317, 318, 324, 325, 350, 360, 377, 381, 402, 427, 436], [230, 251, 220, 334, 314, 345, 351, 376, 378, 350, 377, 389, 335, 407, 426, 414, 447, 465, 490, 481], [231, 241, 239, 275, 359, 370, 378, 323, 335, 358, 340, 344, 356, 411, 424, 441, 442, 444, 487, 494], [245, 233, 223, 319, 336, 348, 355, 366, 350, 337, 355, 369, 385, 371, 374, 438, 443, 456, 489, 481], [215, 243, 210, 325, 364, 325, 345, 369, 375, 374, 383, 390, 388, 360, 386, 417, 403, 442, 480, 460], [245, 219, 249, 286, 349, 342, 348, 358, 366, 334, 359, 358, 362, 409, 386, 412, 424, 429, 438, 454], [243, 235, 265, 302, 312, 365, 369, 368, 345, 384, 381, 366, 326, 400, 387, 437, 447, 451, 460, 449], [198, 203, 265, 334, 346, 344, 344, 364, 346, 383, 378, 337, 372, 393, 415, 439, 441, 430, 466, 487], [224, 230, 268, 320, 354, 372, 365, 368, 354, 337, 372, 342, 375, 385, 405, 410, 403, 465, 460, 472], [243, 257, 234, 321, 334, 338, 377, 371, 370, 324, 384, 390, 352, 389, 396, 434, 412, 467, 460, 481], [210, 231, 242, 328, 358, 302, 347, 378, 361, 329, 365, 353, 391, 413, 423, 385, 427, 433, 492, 475], [211, 218, 265, 335, 366, 359, 371, 342, 358, 370, 373, 339, 364, 408, 379, 390, 436, 429, 492, 482], [253, 255, 265, 301, 344, 358, 338, 348, 346, 357, 316, 388, 356, 413, 426, 437, 400, 440, 482, 500], [249, 248, 262, 322, 351, 354, 377, 339, 322, 367, 334, 345, 381, 385, 359, 434, 427, 424, 488, 481], [236, 222, 197, 295, 296, 333, 360, 349, 335, 343, 358, 383, 387, 353, 423, 419, 420, 458, 488, 476], [251, 262, 251, 325, 302, 367, 349, 345, 372, 380, 367, 377, 373, 401, 399, 381, 444, 468, 456, 460], [244, 224, 259, 311, 362, 361, 345, 326, 348, 351, 350, 369, 371, 398, 426, 419, 435, 434, 460, 464], [236, 232, 237, 325, 307, 318, 375, 369, 329, 335, 338, 366, 384, 362, 381, 381, 426, 463, 478, 474], [236, 199, 257, 309, 304, 355, 356, 365, 316, 342, 366, 359, 379, 405, 411, 410, 447, 449, 456, 452], [228, 252, 257, 302, 350, 350, 339, 323, 320, 363, 374, 354, 360, 408, 394, 424, 400, 444, 430, 454], [238, 239, 254, 325, 327, 323, 344, 358, 368, 373, 374, 334, 335, 414, 427, 430, 438, 430, 468, 495], [230, 256, 264, 307, 366, 350, 329, 345, 360, 345, 356, 344, 348, 393, 367, 441, 446, 467, 476, 487], [250, 251, 263, 333, 342, 317, 359, 351, 362, 374, 348, 355, 384, 406, 427, 434, 446, 465, 488, 492], [248, 242, 261, 331, 299, 362, 333, 351, 371, 377, 375, 382, 376, 373, 422, 391, 430, 453, 486, 474], [235, 239, 238, 320, 313, 346, 334, 378, 378, 378, 373, 385, 376, 362, 417, 435, 435, 437, 440, 462], [242, 244, 247, 322, 353, 354, 368, 325, 372, 337, 352, 361, 368, 370, 406, 378, 389, 459, 477, 497], [212, 263, 266, 323, 366, 360, 317, 319, 361, 341, 382, 381, 367, 388, 407, 383, 403, 462, 464, 443], [247, 207, 237, 290, 346, 326, 369, 375, 362, 375, 336, 322, 341, 402, 386, 406, 436, 464, 469, 482], [222, 241, 221, 306, 331, 330, 319, 343, 328, 361, 381, 321, 386, 383, 406, 419, 405, 455, 478, 477], [223, 206, 265, 306, 355, 342, 328, 366, 370, 380, 376, 389, 388, 404, 422, 415, 448, 461, 466, 501], [197, 227, 257, 326, 348, 342, 358, 357, 373, 366, 376, 383, 376, 412, 403, 402, 410, 468, 493, 471], [248, 257, 241, 280, 345, 371, 369, 378, 342, 341, 376, 341, 337, 399, 417, 443, 398, 448, 486, 501], [228, 218, 251, 288, 329, 317, 369, 373, 363, 350, 384, 376, 380, 415, 425, 388, 432, 435, 488, 476], [233, 230, 237, 308, 329, 326, 378, 375, 374, 363, 379, 375, 389, 385, 387, 434, 426, 439, 467, 502], [249, 256, 243, 304, 311, 331, 360, 338, 335, 350, 336, 370, 386, 415, 417, 419, 436, 437, 492, 498], [222, 248, 256, 313, 308, 316, 368, 341, 367, 349, 380, 373, 338, 405, 392, 442, 438, 442, 485, 462], [186, 231, 243, 289, 337, 346, 368, 355, 351, 368, 352, 390, 370, 415, 417, 401, 442, 449, 433, 499], [238, 253, 266, 321, 360, 318, 364, 323, 360, 380, 323, 390, 389, 407, 373, 435, 428, 461, 448, 498], [199, 246, 244, 314, 342, 349, 365, 368, 349, 365, 385, 345, 341, 415, 378, 414, 439, 458, 442, 472], [225, 248, 249, 331, 341, 318, 327, 356, 376, 343, 381, 383, 365, 404, 402, 405, 408, 458, 488, 451], [231, 221, 220, 335, 366, 343, 372, 373, 369, 358, 333, 360, 369, 405, 417, 427, 395, 418, 489, 481], [233, 248, 230, 295, 339, 346, 360, 370, 356, 380, 373, 374, 390, 417, 406, 396, 407, 424, 477, 453], [212, 233, 230, 313, 325, 362, 357, 359, 324, 328, 371, 381, 350, 411, 398, 432, 446, 447, 466, 499], [181, 256, 261, 322, 354, 340, 378, 329, 375, 382, 382, 347, 345, 402, 417, 404, 381, 464, 452, 454], [236, 246, 252, 297, 354, 328, 371, 359, 322, 370, 379, 347, 342, 411, 427, 440, 446, 459, 457, 476], [223, 239, 245, 276, 326, 359, 337, 366, 374, 376, 385, 380, 317, 413, 379, 428, 381, 464, 459, 489], [224, 211, 258, 281, 340, 365, 376, 334, 374, 340, 384, 379, 339, 354, 419, 379, 440, 460, 447, 492], [241, 251, 263, 289, 360, 340, 330, 350, 378, 345, 374, 325, 391, 416, 382, 400, 433, 468, 452, 500], [189, 261, 246, 329, 307, 334, 339, 325, 361, 341, 381, 382, 368, 391, 414, 404, 423, 462, 456, 466], [194, 246, 237, 334, 329, 335, 366, 372, 348, 323, 363, 368, 391, 381, 388, 438, 424, 468, 461, 480]]




CPU_time_limit = 1800

# 1 Data input
Lambda = 1
Alpha = 0.9


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


start_time = time.time()


# 3 BUILD THE MODEL
model = Model('RA_TSSP')
model.Params.timelimit = CPU_time_limit
#model.setParam('OutputFlag', 0)


# Decision variables
x = {}
y = {}


t = {}
d = {}

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
    for i in F:
        name = 't_' + str(omega) + '_' + str(i)
        t[omega, i] = model.addVar(vtype=GRB.CONTINUOUS, name=name)
        name = 'd_' + str(omega) + '_' + str(i)
        d[omega, i] = model.addVar(vtype=GRB.CONTINUOUS, name=name)

for omega in OMEGA:
    name = 'upsilon_' + str(omega)
    upsilon[omega] = model.addVar(vtype=GRB.CONTINUOUS, name=name)

name = 'eta'
eta = model.addVar(lb=-float('inf'), ub=float('inf'), vtype=GRB.CONTINUOUS, name=name)

# 11a
obj = LinExpr(0)
for k in r:
    for i in F:
        obj.addTerms((1 + Lambda) * C_apron, x[k, i])
for omega in OMEGA:
    for i in F:
        if i in F_E:
            obj.addTerms(scenario_weight * C_E, d[omega, i])
        elif i in F_D:
            obj.addTerms(scenario_weight * C_D, d[omega, i])
        elif i in F_C:
            obj.addTerms(scenario_weight * C_C, d[omega, i])
obj.addTerms(Lambda, eta)
for omega in OMEGA:
    obj.addTerms(scenario_weight * (Lambda / (1 - Alpha)), upsilon[omega])

model.setObjective(obj, GRB.MINIMIZE)
model.params.InfUnbdInfo = 1



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



# Second-stage problem
# 11b
for i in F:
    for omega in OMEGA:
        model.addConstr(t[omega, i] >= scenario_arrival_time[omega - 1][i - 1])
# 11c
for i in F:
    for omega in OMEGA:
        model.addConstr(d[omega, i] >= t[omega, i] - scenario_arrival_time[omega-1][i - 1])
# 11d
for k in K:
    for i in F:
        for j in F:
            if i != j:
                for omega in OMEGA:
                    model.addConstr(t[omega, i] + occupy_time[i - 1] + b - t[omega, j] <= M * (1 - y[k, i, j]))
# 11e
for omega in OMEGA:
    expr = LinExpr(0)
    for i in F:
        if i in F_E:
            expr.addTerms(C_E, d[omega, i])
        elif i in F_D:
            expr.addTerms(C_D, d[omega, i])
        elif i in F_C:
            expr.addTerms(C_C, d[omega, i])
    model.addConstr(expr - eta <= upsilon[omega])




# 定义Callback函数
def mycallback(model, where):

    if where == GRB.Callback.MIP:
        cur_obj = model.cbGet(GRB.Callback.MIP_OBJBST)
        cur_bd = model.cbGet(GRB.Callback.MIP_OBJBND)

        if model._obj != cur_obj or model._bd != cur_bd:
            model._obj = cur_obj
            model._bd = cur_bd
            model._data.append([time.time() - model._start, cur_obj, cur_bd])




model._obj = None
model._bd = None
model._data = []
model._start = time.time()


# 3.5 solve the model
model.optimize(mycallback)



# 打印结果
# print("\n\n-----optimal value-----")
# print(model.Objval)
objective_value = model.Objval
#print(objective_value)
#info = model.status
consumed_time = time.time() - start_time

'''
for key in x.keys():
    if x[key].x > 0:
        print(x[key].VarName + ' = ', x[key].x)
print('\n')
for key in y.keys():
    if y[key].x > 0:
        print(y[key].VarName + ' = ', y[key].x)
print('\n')
for key in t.keys():
    if t[key].x > 0:
        print(t[key].VarName + ' = ', t[key].x)
print('\n')
for key in d.keys():
    if d[key].x > 0:
        print(d[key].VarName + ' = ', d[key].x)
'''

mip_gap = model.MIPGap


print('\n')
print(mip_gap)
print(consumed_time)
print(objective_value)

# X
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
print(Xk_list)


# Update Y
Ykij_list = []
for k in K:
    sub_yij_list = []
    for key in y.keys():
        if key[0] == k:
            if y[key].x > 0.9:
                sub_yij_list.append([key[1], key[2]])
    Ykij_list.append(copy.deepcopy(sub_yij_list))
print(Ykij_list)

'''Yij_list = []
for key in y.keys():
    if y[key].x > 0.9:
        if key[1] != 0 and key[2] != det:
            Yij_list.append([key[1], key[2]])
print(Yij_list)
'''
print(model._data)
