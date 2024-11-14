import copy

def subtour_check(Yij_list, N):

    #print(Yij_list)

    aircraft_sequence = copy.deepcopy(Yij_list)

    #print(aircraft_sequence)

    # find all the subtours
    origin_node = N[0]
    destination_node = N[-1]

    current_node = origin_node

    no_subour_sequence = []
    while current_node != destination_node:
        for arc in aircraft_sequence:
            if arc[0] == current_node:
                current_node = copy.deepcopy(arc[1])
                break
        no_subour_sequence.append(copy.deepcopy(arc))
        #print(arc)
        aircraft_sequence.remove(arc)

    #print(aircraft_sequence)

    subtour_list = []
    while len(aircraft_sequence) > 0:

        origin_node = copy.deepcopy(aircraft_sequence[0][0])
        current_node, destination_node = origin_node, origin_node
        origin_node_counter = 0

        sub_subtour = []

        while origin_node_counter < 1:
            for arc in aircraft_sequence:
                if arc[0] == current_node:
                    current_node = copy.deepcopy(arc[1])
                    break
            sub_subtour.append(copy.deepcopy(arc))
            aircraft_sequence.remove(arc)

            if current_node == destination_node:
                origin_node_counter += 1

        subtour_list.append(copy.deepcopy(sub_subtour))

    return subtour_list
