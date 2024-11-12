

F = [1, 2, 3, 4, 5, 6, 7]
F_large = [1, 3, 5]
F_medium = [2, 4, 6]
F_small = [7]

Separation_matrix = []
for i in F:
    sub_sm = []
    for j in F:
        if i != j:
            if i in F_large and j in F_large:
                sd = 4
            elif i in F_large and j in F_medium:
                sd = 5
            elif i in F_large and j in F_small:
                sd = 7
            elif i in F_medium and j in F_large:
                sd = 3
            elif i in F_medium and j in F_medium:
                sd = 3
            elif i in F_medium and j in F_small:
                sd = 5
            elif i in F_small and j in F_large:
                sd = 3
            elif i in F_small and j in F_medium:
                sd = 3
            elif i in F_small and j in F_small:
                sd = 3
        else:
            sd = 0

        sub_sm.append(sd)

    Separation_matrix.append(sub_sm)

print(Separation_matrix)






