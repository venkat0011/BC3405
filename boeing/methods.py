import plane

# create 2 global variable which is the first row and the last row, the rows with the emergency exit
first_row = 3
last_row = 35
# row 12 and row 14 are evac seats
evac_seats = [14,16]
def random(model):
    """ Creates one boarding group """
    id = 1
    group = []
    for x in range(first_row, last_row) :
        for y in ( 0, 1, 2, 6, 7,8,12,13,14):
            if(x not in evac_seats):
                agent = plane.PassengerAgent(id, model, (x, y), 1)
                id += 1
                group.append(agent)
    model.random.shuffle(group)
    model.boarding_queue.extend(group)


def front_to_back_gr(model):
    final_group = []
    id = 1
    sub_group = []
    counter = last_row-1
    while(counter - 4 >=2):
        for x in range(counter, counter-4, -1):
            for y in ( 0, 1, 2, 6, 7,8):
                if (x not in evac_seats):
                    agent = plane.PassengerAgent(id, model, (x, y), 4)
                    id += 1
                    sub_group.append(agent)
        model.random.shuffle(sub_group)
        for a in sub_group:
            final_group.append(a)
        sub_group = []
        counter-4
    for a in sub_group:
        final_group.append(a)
    model.boarding_queue.extend(final_group)


def back_to_front_gr(model):
    final_group = []
    id = 1
    sub_group = []
    counter = first_row - 1
    while(counter+4<=last_row-1):
        for x in range(counter+4, counter, -1):
            for y in ( 0, 1, 2, 6, 7,8):
                if (x not in evac_seats):
                    agent = plane.PassengerAgent(id, model, (x, y), 4)
                    id += 1
                    sub_group.append(agent)
        model.random.shuffle(sub_group)
        for a in sub_group:
            final_group.append(a)
        sub_group = []
        counter += 4
    for a in sub_group:
        final_group.append(a)

    model.boarding_queue.extend(final_group)


def front_to_back(model):

    final_group = []
    group_id = 16
    id = 1
    for x in range(last_row-1,first_row-1,-1):
        sub_group = []
        for y in ( 0, 1, 2, 6, 7,8):
            if (x not in evac_seats):
                agent = plane.PassengerAgent(id, model, (x, y), group_id)
                id += 1
                sub_group.append(agent)
        model.random.shuffle(sub_group)
        final_group.extend(sub_group)
        group_id -= 1

    model.boarding_queue.extend(final_group)


def back_to_front(model):

    final_group = []
    group_id = 16
    id = 1
    for x in range(first_row, last_row):
        sub_group = []
        for y in ( 0, 1, 2, 6, 7,8):
            if (x not in evac_seats):
                agent = plane.PassengerAgent(id, model, (x, y), group_id)
                id += 1
                sub_group.append(agent)
        model.random.shuffle(sub_group)
        final_group.extend(sub_group)
        group_id -= 1

    model.boarding_queue.extend(final_group)


def win_mid_ais(model):

    final_group = []
    id = 1
    sub_group = []
    for y in (2, 6):
        for x in range(first_row,last_row):
            if (x not in evac_seats):
                agent = plane.PassengerAgent(id, model, (x, y), 3)
                id += 1
                sub_group.append(agent)
    model.random.shuffle(sub_group)
    final_group.extend(sub_group)

    sub_group = []
    for y in (1, 7):
        for x in range(first_row, last_row):
            if (x not in evac_seats):
                agent = plane.PassengerAgent(id, model, (x, y), 2)
                id += 1
                sub_group.append(agent)
    model.random.shuffle(sub_group)
    final_group.extend(sub_group)

    sub_group = []
    for y in (0, 8):
        for x in range(first_row,last_row):
            if (x not in evac_seats):
                agent = plane.PassengerAgent(id, model, (x, y), 1)
                id += 1
                sub_group.append(agent)
    model.random.shuffle(sub_group)
    final_group.extend(sub_group)

    model.boarding_queue.extend(final_group)

#
# def steffen_perfect(model):
#
#     final_group = []
#     id = 1
#     for y in (2, 4):
#         for x in range(first_row, last_row, 2):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 6)
#                 id += 1
#                 final_group.append(agent)
#     for y in (2, 4):
#         for x in range(first_row+1, last_row, 2):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 5)
#                 id += 1
#                 final_group.append(agent)
#     for y in (1, 5):
#         for x in range(first_row, last_row, 2):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 4)
#                 id += 1
#                 final_group.append(agent)
#     for y in (1, 5):
#         for x in range(first_row+1, last_row, 2):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 3)
#                 id += 1
#                 final_group.append(agent)
#     for y in (0, 6):
#         for x in range(first_row, last_row, 2):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 2)
#                 id += 1
#                 final_group.append(agent)
#     for y in (0, 6):
#         for x in range(first_row+1, last_row, 2):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 1)
#                 id += 1
#                 final_group.append(agent)
#
#     model.boarding_queue.extend(final_group)
#
#
# def steffen_modified(model):
#     group = []
#     id = 1
#     for x in range(first_row, last_row, 2):
#         for y in (2, 1, 0):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 4)
#                 id += 1
#                 group.append(agent)
#     model.random.shuffle(group)
#     model.boarding_queue.extend(group)
#     group = []
#     for x in range(first_row, last_row, 2):
#         for y in (4, 5, 6):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 3)
#                 id += 1
#                 group.append(agent)
#     model.random.shuffle(group)
#     model.boarding_queue.extend(group)
#     group = []
#     for x in range(first_row+1, last_row, 2):
#         for y in (2, 1, 0):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 2)
#                 id += 1
#                 group.append(agent)
#     model.random.shuffle(group)
#     model.boarding_queue.extend(group)
#     group = []
#     for x in range(first_row, last_row, 2):
#         for y in (4, 5, 6):
#             if (x not in evac_seats):
#                 agent = plane.PassengerAgent(id, model, (x, y), 1)
#                 id += 1
#                 group.append(agent)
#     model.random.shuffle(group)
#     model.boarding_queue.extend(group)
