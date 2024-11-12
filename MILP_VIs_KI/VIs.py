
import copy
from ZOW.TY.MILP_VIs_KI.SP import SP

def VIs(scenario_weight, OMEGA, scenario_arrival_time, F, F_weight, F_path, F_speed, Path_list, d, M,
                                   rw_separation_matrix, distance_matrix, separation_matrix):

    Cij_list = []

    for i in F:

        sub_Cij_list = []

        for j in F:
            if i != j:

                sub_F = [i, j]
                Yij_list_2 = [[i, j]]

                second_stage_obj_list = []

                for omega in OMEGA:
                    arrival_time = scenario_arrival_time[omega - 1]

                    SP_result = SP(Yij_list_2, arrival_time, sub_F, F_weight, F_path, F_speed, Path_list, d, M,
                                   rw_separation_matrix, distance_matrix, separation_matrix)

                    second_stage_obj_list.append(copy.deepcopy(SP_result))

                sub_Cij_list.append(copy.deepcopy(scenario_weight * sum(second_stage_obj_list)))

            else:
                sub_Cij_list.append(0)

        Cij_list.append(sub_Cij_list)

    return Cij_list





