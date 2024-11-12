

def SMG(F, F_size):

    sep_matrix = []
    for i in F:
        sub_sm = []
        for j in F:
            if i != j:
                if F_size[i - 1] == 1 and F_size[j - 1] == 1:
                    sep_time = 96
                elif F_size[i - 1] == 1 and F_size[j - 1] == 2:
                    sep_time = 157
                elif F_size[i - 1] == 1 and F_size[j - 1] == 3:
                    sep_time = 157
                elif F_size[i - 1] == 2 and F_size[j - 1] == 1:
                    sep_time = 96
                elif F_size[i - 1] == 2 and F_size[j - 1] == 2:
                    sep_time = 157
                elif F_size[i - 1] == 2 and F_size[j - 1] == 3:
                    sep_time = 157
                elif F_size[i - 1] == 3 and F_size[j - 1] == 1:
                    sep_time = 60
                elif F_size[i - 1] == 3 and F_size[j - 1] == 2:
                    sep_time = 69
                elif F_size[i - 1] == 3 and F_size[j - 1] == 3:
                    sep_time = 69
                sub_sm.append(sep_time)
            else:
                sub_sm.append(0)
        sep_matrix.append(sub_sm)

    return sep_matrix

