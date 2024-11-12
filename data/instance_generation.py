
import copy, random




Aircraft_number = 10
F = [i for i in range(1, Aircraft_number + 1)]
print('I = ' + str(F))


F_ad = copy.deepcopy(F)
random.shuffle(F_ad)


Heavy_ratio = 0.3
Heavy_number = round(Aircraft_number * Heavy_ratio)
Fh = [1 for i in range(1, Heavy_number + 1)]
Large_ratio = 0.7
Large_number = round(Aircraft_number * Large_ratio)
Fm = [2 for i in range(1, Large_number + 1)]
F_size = copy.deepcopy(Fh + Fm)
random.shuffle(F_size)
print('I_size = ' + str(F_size))



H_max, H_min = 0.0833, 0.0694
L_max, L_min = 0.0750, 0.0694
F_speed_max = []
F_speed_min = []
for i_size in F_size:
    if i_size == 1:
        F_speed_max.append(H_max)
        F_speed_min.append(H_min)
    elif i_size == 2:
        F_speed_max.append(L_max)
        F_speed_min.append(L_min)
print('I_speed_max = ' + str(F_speed_max))
print('I_speed_min = ' + str(F_speed_min))


F_weight = []
for i in F:
    weight = random.randint(1, 3)
    F_weight.append(weight)
print('I_weight = ' + str(F_weight))


F_path = []
for i in F:
    approach_fix = random.randint(1, 3)
    F_path.append(approach_fix)
print('I_path = ' + str(F_path))



separation_matrix = []
for i in F_size:
    ssm = []
    for j in F_size:
        if i != j:
            if i == 1 and j == 1:
                ssm.append(4)
            elif i == 1 and j == 2:
                ssm.append(5)
            else:
                ssm.append(3)
        else:
            ssm.append(0)
    separation_matrix.append(ssm)
print('separation_matrix = ' + str(separation_matrix))





#Aircraft
nominal_lt_time = []
aircraft_counter = 0
while aircraft_counter < Aircraft_number:
    lt_time = random.randint(1800, 3600)
    nominal_lt_time.append(lt_time)
    aircraft_counter += 1
nominal_lt_time.sort()
#print(nominal_lt_time)





scenario_number = 100
scenario_weight = 1 / scenario_number
print('scenario_weight = ' + str(scenario_weight))


OMEGA = []
scenario_counter = 1
while scenario_counter < scenario_number + 1:
    OMEGA.append(scenario_counter)
    scenario_counter += 1
print('OMEGA = ' + str(OMEGA))


scenario_arrival_time = []
scenario_arrival_time.append(nominal_lt_time)


scenario_counter = 1
while scenario_counter < scenario_number:
    sat = []
    aircraft_counter = 0
    while aircraft_counter < len(nominal_lt_time):
        lt = nominal_lt_time[aircraft_counter]
        deviation = random.triangular(-360, 0, 360)
        sat.append(lt + round(deviation))
        aircraft_counter += 1

    scenario_arrival_time.append(sat)
    scenario_counter += 1
print('scenario_arrival_time = ' + str(scenario_arrival_time))











