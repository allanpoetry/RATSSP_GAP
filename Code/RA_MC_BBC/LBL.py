import copy


#(F, Fheavy, Flarge, Fsmall, OMEGA, scenario_arrival_time, scenario_weight, occupy_time, b, C_heavy, C_large, C_small):


def LBL(I, IE, ID, IC, OMEGA, scenario_arrival_time, occupy_time, b, CD_E, CD_D, CD_C):

    OMEGA_Cij_list = []
    for omega in OMEGA:
        Cij_list = []
        for i in I:
            sub_Cij_list = []
            for j in I:
                if i != j:
                    Cij = 0
                    arrival_time = copy.deepcopy(scenario_arrival_time[omega - 1])
                    if (arrival_time[i - 1] + occupy_time[i - 1] + b) > arrival_time[j - 1]:
                        delay_time = (arrival_time[i - 1] + occupy_time[i - 1] + b) - arrival_time[j - 1]
                    else:
                        delay_time = 0
                    if j in IE:
                        Cij += CD_E * delay_time
                    elif j in ID:
                        Cij += CD_D * delay_time
                    elif j in IC:
                        Cij += CD_C * delay_time
                    sub_Cij_list.append(Cij)
                else:
                    sub_Cij_list.append(0)

            Cij_list.append(sub_Cij_list)

        OMEGA_Cij_list.append(Cij_list)

    return OMEGA_Cij_list



