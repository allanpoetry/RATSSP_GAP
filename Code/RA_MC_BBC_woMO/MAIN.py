from gurobipy import *
import time, copy
from SGAP.Solution_methods.RA_BD.SP import SP
from SGAP.Solution_methods.RA_BD.subtour_check import subtour_check
from SGAP.Solution_methods.RA_MC_BBC.LBL import LBL



# 20 Contact gates
K_E = [1, 2, 3, 4]
K_D = [5, 6, 7, 8, 9, 10, 11, 12, 13]
K_C = [14, 15, 16, 17, 18, 19, 20]
r = [21]
K = K_E + K_D + K_C
K_all = K + r





# S10
F = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
F_size  = [1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2]
F_E = []
F_D = [4, 9, 12, 13, 14, 17, 25, 26, 30]
F_C = [1, 2, 3, 5, 6, 7, 8, 10, 11, 15, 16, 18, 19, 20, 21, 22, 23, 24, 27, 28, 29]
occupy_time  = [79, 66, 95, 113, 85, 117, 104, 109, 70, 109, 60, 64, 86, 109, 82, 106, 88, 88, 113, 87, 98, 101, 118, 90, 92, 102, 113, 108, 90, 111]
scenario_weight = 0.02
OMEGA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
scenario_arrival_time = [[2774, 2790, 2778, 2802, 2768, 2809, 2790, 2793, 2808, 2792, 2779, 2802, 2800, 2825, 2846, 2838, 2826, 2850, 2826, 2851, 2892, 2855, 2859, 2846, 2827, 2848, 2859, 2853, 2878, 2859], [2734, 2778, 2795, 2790, 2771, 2783, 2808, 2796, 2811, 2803, 2820, 2811, 2828, 2825, 2833, 2817, 2844, 2831, 2846, 2890, 2861, 2852, 2873, 2861, 2890, 2851, 2876, 2873, 2857, 2874], [2764, 2760, 2781, 2766, 2828, 2803, 2800, 2797, 2842, 2841, 2800, 2837, 2806, 2839, 2829, 2815, 2812, 2816, 2842, 2854, 2854, 2857, 2887, 2847, 2867, 2871, 2845, 2838, 2866, 2865], [2778, 2770, 2776, 2800, 2776, 2797, 2792, 2802, 2795, 2813, 2824, 2806, 2797, 2825, 2843, 2811, 2821, 2824, 2863, 2827, 2868, 2850, 2846, 2836, 2860, 2845, 2881, 2868, 2875, 2879], [2762, 2766, 2762, 2798, 2776, 2787, 2849, 2789, 2791, 2810, 2815, 2815, 2810, 2832, 2832, 2864, 2827, 2821, 2819, 2869, 2837, 2840, 2829, 2837, 2892, 2854, 2844, 2865, 2881, 2871], [2742, 2777, 2757, 2787, 2768, 2780, 2808, 2788, 2793, 2815, 2837, 2786, 2811, 2830, 2829, 2828, 2835, 2846, 2835, 2840, 2821, 2882, 2823, 2852, 2856, 2859, 2883, 2866, 2865, 2910], [2743, 2778, 2767, 2774, 2778, 2781, 2803, 2790, 2806, 2811, 2800, 2812, 2861, 2813, 2828, 2838, 2861, 2824, 2837, 2890, 2826, 2832, 2875, 2866, 2852, 2853, 2874, 2859, 2867, 2890], [2758, 2764, 2800, 2803, 2782, 2780, 2796, 2823, 2815, 2836, 2805, 2831, 2819, 2830, 2820, 2820, 2820, 2837, 2865, 2840, 2880, 2887, 2852, 2852, 2880, 2893, 2849, 2868, 2872, 2875], [2798, 2743, 2755, 2783, 2844, 2784, 2854, 2790, 2844, 2862, 2839, 2809, 2839, 2870, 2861, 2866, 2835, 2854, 2837, 2845, 2859, 2899, 2864, 2856, 2860, 2854, 2893, 2868, 2851, 2925], [2763, 2795, 2795, 2799, 2790, 2770, 2830, 2810, 2807, 2807, 2807, 2812, 2814, 2867, 2856, 2853, 2839, 2821, 2859, 2871, 2866, 2880, 2854, 2849, 2848, 2860, 2875, 2884, 2872, 2923], [2758, 2768, 2767, 2762, 2808, 2806, 2785, 2828, 2834, 2787, 2840, 2818, 2847, 2813, 2831, 2835, 2844, 2828, 2836, 2867, 2870, 2839, 2839, 2855, 2867, 2861, 2846, 2874, 2853, 2894], [2768, 2776, 2769, 2761, 2797, 2780, 2854, 2819, 2810, 2802, 2833, 2805, 2811, 2841, 2843, 2866, 2837, 2847, 2843, 2843, 2892, 2839, 2853, 2856, 2836, 2873, 2864, 2847, 2875, 2877], [2767, 2780, 2813, 2786, 2777, 2768, 2805, 2808, 2796, 2801, 2789, 2825, 2797, 2805, 2828, 2835, 2816, 2841, 2858, 2829, 2900, 2862, 2855, 2880, 2858, 2860, 2856, 2868, 2847, 2895], [2779, 2764, 2787, 2762, 2777, 2845, 2819, 2822, 2807, 2838, 2862, 2805, 2841, 2837, 2820, 2836, 2835, 2872, 2833, 2850, 2859, 2855, 2839, 2828, 2860, 2858, 2842, 2856, 2919, 2873], [2797, 2775, 2786, 2783, 2808, 2790, 2797, 2798, 2810, 2806, 2819, 2829, 2837, 2821, 2832, 2822, 2847, 2840, 2850, 2859, 2845, 2851, 2865, 2820, 2832, 2845, 2871, 2867, 2836, 2870], [2816, 2755, 2775, 2791, 2793, 2839, 2800, 2775, 2811, 2797, 2852, 2853, 2810, 2829, 2831, 2835, 2842, 2846, 2894, 2869, 2847, 2842, 2847, 2830, 2850, 2873, 2872, 2853, 2878, 2877], [2776, 2780, 2756, 2774, 2802, 2795, 2800, 2824, 2813, 2787, 2783, 2803, 2799, 2829, 2837, 2826, 2816, 2840, 2802, 2840, 2848, 2863, 2849, 2876, 2847, 2844, 2870, 2854, 2888, 2861], [2749, 2770, 2764, 2771, 2794, 2806, 2789, 2782, 2791, 2795, 2864, 2820, 2816, 2837, 2835, 2828, 2838, 2839, 2882, 2850, 2843, 2878, 2852, 2849, 2824, 2850, 2893, 2855, 2880, 2880], [2752, 2769, 2774, 2747, 2799, 2785, 2781, 2811, 2799, 2853, 2782, 2821, 2830, 2818, 2836, 2835, 2815, 2838, 2866, 2849, 2851, 2844, 2879, 2858, 2894, 2881, 2880, 2853, 2894, 2882], [2742, 2787, 2769, 2758, 2797, 2778, 2784, 2814, 2805, 2811, 2833, 2811, 2791, 2802, 2833, 2835, 2809, 2815, 2842, 2850, 2839, 2860, 2857, 2836, 2871, 2912, 2895, 2870, 2860, 2865], [2820, 2748, 2750, 2792, 2767, 2790, 2835, 2822, 2803, 2802, 2850, 2834, 2839, 2817, 2849, 2822, 2810, 2837, 2857, 2840, 2839, 2845, 2836, 2855, 2848, 2863, 2845, 2852, 2885, 2853], [2750, 2759, 2783, 2765, 2765, 2795, 2796, 2819, 2798, 2821, 2850, 2823, 2789, 2847, 2843, 2824, 2829, 2845, 2855, 2813, 2857, 2852, 2862, 2875, 2867, 2866, 2853, 2868, 2882, 2862], [2748, 2772, 2835, 2772, 2794, 2809, 2836, 2781, 2795, 2799, 2790, 2819, 2805, 2824, 2841, 2871, 2804, 2840, 2885, 2844, 2850, 2857, 2834, 2855, 2876, 2848, 2871, 2873, 2884, 2875], [2758, 2777, 2786, 2779, 2799, 2816, 2794, 2799, 2786, 2816, 2810, 2787, 2820, 2856, 2857, 2827, 2825, 2879, 2825, 2840, 2861, 2863, 2845, 2859, 2901, 2850, 2873, 2859, 2876, 2874], [2763, 2772, 2801, 2775, 2776, 2776, 2801, 2813, 2799, 2802, 2796, 2824, 2832, 2842, 2822, 2824, 2803, 2858, 2846, 2844, 2860, 2856, 2897, 2845, 2853, 2825, 2861, 2870, 2875, 2897], [2761, 2786, 2775, 2759, 2780, 2756, 2799, 2801, 2804, 2798, 2819, 2840, 2820, 2841, 2860, 2837, 2834, 2838, 2822, 2851, 2850, 2852, 2852, 2864, 2842, 2860, 2841, 2867, 2887, 2875], [2757, 2773, 2770, 2801, 2802, 2790, 2798, 2792, 2784, 2801, 2835, 2817, 2808, 2832, 2812, 2821, 2840, 2798, 2856, 2855, 2839, 2828, 2852, 2845, 2853, 2843, 2866, 2870, 2843, 2862], [2742, 2746, 2780, 2780, 2769, 2778, 2815, 2786, 2813, 2801, 2803, 2788, 2810, 2837, 2826, 2862, 2837, 2851, 2833, 2852, 2860, 2859, 2840, 2844, 2858, 2874, 2850, 2876, 2882, 2857], [2754, 2770, 2820, 2785, 2783, 2791, 2793, 2785, 2791, 2819, 2809, 2833, 2813, 2828, 2851, 2820, 2830, 2828, 2851, 2845, 2847, 2829, 2865, 2851, 2902, 2860, 2898, 2863, 2864, 2862], [2800, 2751, 2770, 2772, 2811, 2835, 2798, 2802, 2832, 2824, 2832, 2819, 2848, 2816, 2829, 2845, 2869, 2851, 2844, 2870, 2812, 2840, 2846, 2823, 2845, 2850, 2863, 2850, 2887, 2848], [2819, 2770, 2788, 2792, 2783, 2789, 2780, 2792, 2821, 2821, 2810, 2814, 2795, 2813, 2860, 2839, 2818, 2835, 2845, 2847, 2824, 2857, 2848, 2853, 2853, 2851, 2853, 2865, 2877, 2867], [2743, 2750, 2755, 2759, 2754, 2811, 2800, 2803, 2800, 2805, 2791, 2828, 2819, 2814, 2814, 2859, 2852, 2852, 2869, 2878, 2852, 2843, 2857, 2857, 2852, 2851, 2865, 2866, 2919, 2872], [2751, 2764, 2783, 2785, 2781, 2804, 2795, 2802, 2824, 2843, 2841, 2821, 2787, 2809, 2829, 2830, 2820, 2810, 2832, 2863, 2865, 2842, 2848, 2872, 2837, 2857, 2853, 2869, 2876, 2883], [2720, 2767, 2801, 2781, 2790, 2775, 2816, 2813, 2826, 2830, 2809, 2864, 2846, 2854, 2846, 2822, 2816, 2832, 2840, 2846, 2838, 2852, 2848, 2850, 2889, 2852, 2868, 2839, 2880, 2853], [2737, 2773, 2753, 2794, 2810, 2817, 2795, 2778, 2806, 2830, 2824, 2829, 2855, 2852, 2839, 2838, 2835, 2838, 2867, 2837, 2874, 2837, 2847, 2844, 2863, 2856, 2854, 2855, 2859, 2858], [2773, 2767, 2755, 2747, 2773, 2795, 2790, 2810, 2810, 2810, 2832, 2809, 2797, 2811, 2824, 2828, 2825, 2891, 2853, 2832, 2875, 2844, 2888, 2853, 2845, 2830, 2895, 2850, 2860, 2875], [2756, 2757, 2817, 2763, 2772, 2777, 2816, 2792, 2804, 2810, 2792, 2811, 2830, 2809, 2819, 2815, 2820, 2813, 2855, 2850, 2846, 2821, 2830, 2843, 2902, 2851, 2843, 2860, 2865, 2873], [2779, 2771, 2780, 2805, 2786, 2788, 2814, 2765, 2827, 2812, 2802, 2816, 2826, 2844, 2828, 2824, 2822, 2837, 2838, 2848, 2837, 2878, 2850, 2851, 2848, 2872, 2850, 2862, 2866, 2863], [2769, 2755, 2765, 2779, 2814, 2813, 2801, 2809, 2816, 2802, 2811, 2795, 2800, 2815, 2832, 2821, 2825, 2845, 2834, 2832, 2838, 2896, 2852, 2865, 2884, 2884, 2858, 2842, 2864, 2853], [2779, 2759, 2744, 2758, 2792, 2786, 2770, 2792, 2853, 2803, 2790, 2835, 2841, 2840, 2838, 2819, 2815, 2846, 2851, 2840, 2810, 2868, 2842, 2846, 2858, 2836, 2874, 2887, 2862, 2898], [2756, 2758, 2780, 2780, 2793, 2783, 2773, 2815, 2787, 2810, 2813, 2810, 2808, 2868, 2841, 2832, 2837, 2851, 2863, 2811, 2857, 2838, 2848, 2855, 2861, 2842, 2864, 2834, 2875, 2855], [2765, 2766, 2771, 2798, 2782, 2797, 2798, 2790, 2792, 2806, 2796, 2832, 2790, 2811, 2823, 2821, 2834, 2854, 2836, 2862, 2843, 2867, 2847, 2839, 2860, 2856, 2846, 2887, 2877, 2882], [2788, 2765, 2794, 2808, 2812, 2794, 2807, 2832, 2822, 2809, 2813, 2809, 2871, 2815, 2808, 2830, 2834, 2846, 2841, 2839, 2878, 2843, 2890, 2865, 2856, 2859, 2853, 2898, 2880, 2866], [2768, 2771, 2791, 2754, 2833, 2799, 2783, 2799, 2803, 2804, 2827, 2811, 2835, 2838, 2862, 2845, 2826, 2822, 2833, 2844, 2866, 2870, 2888, 2843, 2860, 2853, 2856, 2888, 2851, 2861], [2738, 2818, 2780, 2790, 2790, 2784, 2765, 2787, 2812, 2832, 2820, 2807, 2820, 2847, 2806, 2827, 2863, 2813, 2858, 2833, 2820, 2888, 2822, 2841, 2852, 2899, 2850, 2880, 2870, 2865], [2772, 2774, 2778, 2780, 2751, 2809, 2826, 2821, 2835, 2817, 2790, 2815, 2852, 2831, 2843, 2822, 2854, 2842, 2876, 2841, 2852, 2850, 2855, 2845, 2862, 2875, 2859, 2811, 2895, 2879], [2761, 2761, 2790, 2763, 2771, 2794, 2794, 2800, 2845, 2785, 2870, 2820, 2859, 2815, 2839, 2872, 2875, 2833, 2854, 2844, 2865, 2859, 2852, 2878, 2860, 2875, 2828, 2845, 2842, 2875], [2790, 2780, 2756, 2832, 2775, 2768, 2777, 2784, 2804, 2801, 2769, 2821, 2826, 2815, 2862, 2808, 2840, 2840, 2844, 2871, 2840, 2838, 2849, 2861, 2873, 2860, 2824, 2888, 2851, 2875], [2740, 2791, 2786, 2772, 2830, 2801, 2819, 2810, 2801, 2810, 2811, 2835, 2816, 2829, 2820, 2835, 2863, 2840, 2829, 2841, 2863, 2844, 2867, 2873, 2896, 2854, 2910, 2832, 2853, 2875], [2741, 2788, 2783, 2791, 2801, 2796, 2798, 2791, 2796, 2802, 2798, 2814, 2814, 2808, 2844, 2803, 2831, 2828, 2854, 2859, 2851, 2837, 2859, 2868, 2868, 2866, 2837, 2854, 2871, 2878]]




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


# Enhancements
# 1 Lower bound lifting inequalities
Dij_list = LBL(F, F_E, F_D, F_C, OMEGA, scenario_arrival_time, occupy_time, b, C_E, C_D, C_C)



UB = 1000000000
LB = 0
GAP = UB - LB



start_time = time.time()
CPU_time = time.time() - start_time




# 3 BUILD THE MODEL
model = Model('MP')
#model.setParam('OutputFlag', 0)
model.Params.timelimit = CPU_time_limit
model.Params.MIPGap = 0.0000001



model._Optimality_cuts_counter = 0


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


# 11a
obj = LinExpr(0)
for g in r:
    for i in F:
        obj.addTerms((1 + Lambda) * C_apron, x[g, i])
for omega in OMEGA:
    obj.addTerms(scenario_weight, theta[omega])
# CVaR
obj.addTerms(Lambda, eta)
for omega in OMEGA:
    obj.addTerms(scenario_weight * (Lambda / (1 - Alpha)), upsilon[omega])
model.setObjective(obj, GRB.MINIMIZE)
model.Params.lazyConstraints = 1

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
# 12b
for omega in OMEGA:
    model.addConstr(theta[omega] - eta <= upsilon[omega])
# 19 LBL
for omega in OMEGA:
    expr = LinExpr(0)
    for k in K:
        for i in F:
            for j in F:
                if i != j:
                    expr.addTerms(Dij_list[omega - 1][i - 1][j - 1], y[k, i, j])
    model.addConstr(theta[omega] >= expr)








# 定义Callback函数
def mycallback(model, where):
    if where == GRB.Callback.MIPSOL:
        # 获取当前节点的变量取值
        x_val = model.cbGetSolution(x)
        y_val = model.cbGetSolution(y)

        Xk_list = []
        k_counter = 0
        while k_counter < len(K):
            k_list = []
            for key in x_val.keys():
                if key[0] == k_counter + 1:
                    if round(x_val[key], 6) >= 0.9:
                        k_list.append(key[1])
            k_counter += 1
            Xk_list.append(k_list)

        # Update Y
        test_Binary_Yij = copy.deepcopy(Binary_Yij)
        for key in y_val.keys():
            test_Binary_Yij[key[1]][key[2]] += round(y_val[key])

        Ykij_list = []
        for k in K:
            sub_yij_list = []
            for key in y_val.keys():
                if key[0] == k:
                    if y_val[key] > 0.9:
                        sub_yij_list.append([key[1], key[2]])
            Ykij_list.append(copy.deepcopy(sub_yij_list))

        Xki_list = []
        for key in x_val.keys():
            if x_val[key] > 0.9:
                if key[0] in r:
                    Xki_list.append([key[0], key[1]])

        subtour_counter = 0
        for Yij in Ykij_list:
            subtour_list = subtour_check(Yij, N)
            if len(subtour_list) > 0:
                subtour_counter = 1
            for sl in subtour_list:
                #Subtour_elimination_cuts.append(sl)
                # Subtour elimination
                for k in K:
                    expr = LinExpr(0)
                    for arc in sl:
                        expr.addTerms(1, y[k, arc[0], arc[1]])
                    model.cbLazy(expr <= len(sl) - 1)



        # 如果没有子路径，计算SP
        if subtour_counter == 0:

            for omega in OMEGA:
                arrival_time = copy.deepcopy(scenario_arrival_time[omega - 1])
                SP_result = SP(F, F_E, F_D, F_C, arrival_time, occupy_time, C_E, C_D, C_C, M, b,
                               test_Binary_Yij, test_Pi, test_Sigma, test_Tau)

                # Benders optimality cuts
                pi_info = copy.deepcopy(SP_result[1])
                sigma_info = copy.deepcopy(SP_result[2])
                tau_info = copy.deepcopy(SP_result[3])

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

                model._Optimality_cuts_counter += 1

                model.cbLazy(theta[omega] >= para - M * expr)






# 3.5 solve the model
model.optimize(mycallback)




# 打印结果
# print("\n\n-----optimal value-----")
# print(model.Objval)
objective_value = model.Objval


print('\n')
# 需要返回的内容
# optimlaity gap
mip_gap = model.MIPGap
print(mip_gap)

# 计算时间
CPU_time = time.time() - start_time
print(CPU_time)

# Objective value
print(objective_value)


# Solution
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
print("Xk_list = " + str(Xk_list))

Ykij_list = []
for k in K:
    sub_yij_list = []
    for key in y.keys():
        if key[0] == k:
            if y[key].x > 0.9:
                sub_yij_list.append([key[1], key[2]])
    Ykij_list.append(copy.deepcopy(sub_yij_list))
print("Ykij_list = " + str(Ykij_list))


#print(upper_bound_list)
#print(lower_bound_list)



















