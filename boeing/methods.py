import plane

# create 2 global variable which is the first row and the last row, the rows with the emergency exit
first_row = 3
last_row = 50

# scoot plus
first_scoot_plus_row = 3
last_scoot_plus_row = 8
scoot_plus_seats = [1, 2, 6, 7, 8, 12, 13]

# scoot silence
first_scoot_silence_row = 9
last_scoot_silence_row = 14

# scoot economy
first_scoot_economy_row = 15
last_scoot_economy_row = 51


# row 8, 14, 34 are evac seats
evac_seats = [8, 14, 34]
special_cols = [33, 35, 49, 50]
scoot_plus_cols = [3, 4, 5, 6, 7]


def random(model):
    #
    """ Creates one boarding group """
    """ Boeing 737"""
    id = 1
    scoot_plus_grp = []
    scoot_silence_grp = []
    econ_group = []
    final_group = []

    for x in range(first_scoot_plus_row, last_scoot_plus_row):
        for y in scoot_plus_seats:
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_plus_grp.append(agent)
    model.random.shuffle(scoot_plus_grp)
    final_group.extend(scoot_plus_grp)

    for x in range(first_scoot_silence_row, last_scoot_silence_row):
        for y in (0, 1, 2, 6, 7, 8, 12, 13, 14):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_silence_grp.append(agent)
    model.random.shuffle(scoot_silence_grp)
    final_group.extend(scoot_silence_grp)

    for x in range(first_scoot_economy_row, last_scoot_economy_row):
        if x in special_cols:
            # 3 0 0 configuration
            if x == 33:
                for y in (0, 1, 2):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
            # 0 3 0 configuration
            elif x == 35 or x == 50:
                for y in (6, 7, 8):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
            # 2 3 2 configuration
            elif x == 49:
                for y in (0, 1, 6, 7, 8, 13, 14):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)

        for y in (0, 1, 2, 6, 7, 8, 12, 13, 14):
            if (x not in evac_seats and x not in special_cols):
                agent = plane.PassengerAgent(id, model, (x, y), 1)
                id += 1
                econ_group.append(agent)

    model.random.shuffle(econ_group)
    final_group.extend(econ_group)

    model.boarding_queue.extend(final_group)


def front_to_back_gr(model):

    id = 1
    sub_group = []
    counter = 0

    scoot_plus_grp = []
    scoot_silence_grp = []
    econ_group = []
    final_group = []

    for x in range(first_scoot_plus_row, last_scoot_plus_row):
        for y in scoot_plus_seats:
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_plus_grp.append(agent)
    model.random.shuffle(scoot_plus_grp)
    final_group.extend(scoot_plus_grp)

    for x in range(first_scoot_silence_row, last_scoot_silence_row):
        for y in (0, 1, 2, 6, 7, 8, 12, 13, 14):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_silence_grp.append(agent)
    model.random.shuffle(scoot_silence_grp)
    final_group.extend(scoot_silence_grp)

    for x in range(first_scoot_economy_row, last_scoot_economy_row):
        while counter < 4:
            if x in special_cols:
                # 3 0 0 configuration
                if x == 33:
                    for y in (0, 1, 2):
                        agent = plane.PassengerAgent(id, model, (x, y), 1)
                        id += 1
                        sub_group.append(agent)
                # 0 3 0 configuration
                elif x == 35 or x == 50:
                    for y in (6, 7, 8):
                        agent = plane.PassengerAgent(id, model, (x, y), 1)
                        id += 1
                        sub_group.append(agent)
                # 2 3 2 configuration
                elif x == 49:
                    for y in (0, 1, 6, 7, 8, 13, 14):
                        agent = plane.PassengerAgent(id, model, (x, y), 1)
                        id += 1
                        sub_group.append(agent)

            for y in (0, 1, 2, 6, 7, 8, 12, 13, 14):
                if (x not in evac_seats and x not in special_cols):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    sub_group.append(agent)

            w = w + 1
        model.random.shuffle(sub_group)
        econ_group.extend(sub_group)
        sub_group = []
        w = 0

    final_group.extend(econ_group)

    model.boarding_queue.extend(final_group)

# Not done


def back_to_front_gr(model):
    final_group = []
    id = 1
    sub_group = []
    counter = first_row - 1
    while (counter+4 <= last_row-1):
        for x in range(counter+4, counter, -1):
            for y in (1, 2, 3, 5, 6, 7):
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
    """ Boeing 737"""

    id = 1
    scoot_plus_grp = []
    scoot_silence_grp = []
    econ_group = []
    final_group = []

    for x in range(first_scoot_plus_row, last_scoot_plus_row):
        for y in scoot_plus_seats:
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_plus_grp.append(agent)

    final_group.extend(scoot_plus_grp)

    for x in range(first_scoot_silence_row, last_scoot_silence_row):
        for y in (0, 1, 2, 6, 7, 8, 12, 13, 14):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_silence_grp.append(agent)

    final_group.extend(scoot_silence_grp)

    for x in range(first_scoot_economy_row, last_scoot_economy_row):
        if x in special_cols:
            # 3 0 0 configuration
            if x == 33:
                for y in (0, 1, 2):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
            # 0 3 0 configuration
            elif x == 35 or x == 50:
                for y in (6, 7, 8):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
            # 2 3 2 configuration
            elif x == 49:
                for y in (0, 1, 6, 7, 8, 13, 14):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)

        for y in (0, 1, 2, 6, 7, 8, 12, 13, 14):
            if (x not in evac_seats and x not in special_cols):
                agent = plane.PassengerAgent(id, model, (x, y), 1)
                id += 1
                econ_group.append(agent)

    final_group.extend(econ_group)

    model.boarding_queue.extend(final_group)


def back_to_front(model):
    """ Boeing 737"""

    id = 1
    scoot_plus_grp = []
    scoot_silence_grp = []
    econ_group = []
    final_group = []

    for x in range(last_scoot_plus_row - 1, first_scoot_plus_row - 1, -1):
        for y in scoot_plus_seats:
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_plus_grp.append(agent)

    final_group.extend(scoot_plus_grp)

    for x in range(last_scoot_silence_row - 1, first_scoot_silence_row - 1, -1):
        for y in (0, 1, 2, 6, 7, 8, 12, 13, 14):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_silence_grp.append(agent)

    final_group.extend(scoot_silence_grp)

    for x in range(last_scoot_economy_row - 1, first_scoot_economy_row - 1, -1):
        if x in special_cols:
            # 3 0 0 configuration
            if x == 33:
                for y in (0, 1, 2):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
            # 0 3 0 configuration
            elif x == 35 or x == 50:
                for y in (6, 7, 8):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
            # 2 3 2 configuration
            elif x == 49:
                for y in (0, 1, 6, 7, 8, 13, 14):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)

        for y in (0, 1, 2, 6, 7, 8, 12, 13, 14):
            if (x not in evac_seats and x not in special_cols):
                agent = plane.PassengerAgent(id, model, (x, y), 1)
                id += 1
                econ_group.append(agent)

    final_group.extend(econ_group)

    model.boarding_queue.extend(final_group)

# TODO: update for boeing


def front_to_back_gr(model):
    final_group = []
    id = 1
    sub_group = []
    counter = last_row-1
    while (counter - 4 >= 2):
        for x in range(counter, counter-4, -1):
            for y in (1, 2, 3, 5, 6, 7):
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

# TODO: update for boeing


def back_to_front_gr(model):
    final_group = []
    id = 1
    sub_group = []
    counter = first_row - 1
    while (counter+4 <= last_row-1):
        for x in range(counter+4, counter, -1):
            for y in (1, 2, 3, 5, 6, 7):
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


def win_mid_ais(model):
    """ Boeing 737"""
    id = 1
    scoot_plus_grp = []
    scoot_silence_grp = []
    econ_group = []
    final_group = []

    scoot_plus_grp = []
    for y in (1, 8, 13):
        for x in range(first_scoot_plus_row, last_scoot_plus_row):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_plus_grp.append(agent)
    model.random.shuffle(scoot_plus_grp)
    final_group.extend(scoot_plus_grp)

    scoot_plus_grp = []
    for y in (2, 7, 12):
        for x in range(first_scoot_plus_row, last_scoot_plus_row):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_plus_grp.append(agent)
    model.random.shuffle(scoot_plus_grp)
    final_group.extend(scoot_plus_grp)

    scoot_plus_grp = []
    for y in ([6]):
        for x in range(first_scoot_plus_row, last_scoot_plus_row):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_plus_grp.append(agent)
    model.random.shuffle(scoot_plus_grp)
    final_group.extend(scoot_plus_grp)

    scoot_silence_grp = []
    for y in (0, 8, 14):
        for x in range(first_scoot_silence_row, last_scoot_silence_row):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_silence_grp.append(agent)
    model.random.shuffle(scoot_silence_grp)
    final_group.extend(scoot_silence_grp)

    scoot_silence_grp = []
    for y in (1, 7, 13):
        for x in range(first_scoot_silence_row, last_scoot_silence_row):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_silence_grp.append(agent)
    model.random.shuffle(scoot_silence_grp)
    final_group.extend(scoot_silence_grp)

    scoot_silence_grp = []
    for y in (2, 6, 12):
        for x in range(first_scoot_silence_row, last_scoot_silence_row):
            agent = plane.PassengerAgent(id, model, (x, y), 1)
            id += 1
            scoot_silence_grp.append(agent)
    model.random.shuffle(scoot_silence_grp)
    final_group.extend(scoot_silence_grp)

    econ_group = []
    for y in (0, 8, 14):
        for x in range(first_scoot_economy_row, last_scoot_economy_row):
            if x in special_cols:
                # 3 0 0 configuration
                if x == 33 and y == 0:
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
                # 0 3 0 configuration
                elif (x == 35 or x == 50) and y == 8:
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
                # 2 3 2 configuration
                elif x == 49:
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)

            elif x not in evac_seats:
                agent = plane.PassengerAgent(id, model, (x, y), 1)
                id += 1
                econ_group.append(agent)

    model.random.shuffle(econ_group)
    final_group.extend(econ_group)

    econ_group = []
    for y in (1, 7, 13):
        for x in range(first_scoot_economy_row, last_scoot_economy_row):
            if x in special_cols:
                # 3 0 0 configuration
                if x == 33 and y == 1:
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
                # 0 3 0 configuration
                elif (x == 35 or x == 50) and (y == 7):
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
                # 2 3 2 configuration
                elif x == 49:
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)

            elif x not in evac_seats:
                agent = plane.PassengerAgent(id, model, (x, y), 1)
                id += 1
                econ_group.append(agent)

    model.random.shuffle(econ_group)
    final_group.extend(econ_group)

    econ_group = []
    for y in (2, 6, 12):
        for x in range(first_scoot_economy_row, last_scoot_economy_row):
            if x in special_cols:
                # 3 0 0 configuration
                if x == 33 and y == 2:
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
                # 0 3 0 configuration
                elif (x == 35 or x == 50) and y == 6:
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)
                # 2 3 2 configuration
                elif x == 49 and y == 6:
                    agent = plane.PassengerAgent(id, model, (x, y), 1)
                    id += 1
                    econ_group.append(agent)

            elif x not in evac_seats:
                agent = plane.PassengerAgent(id, model, (x, y), 1)
                id += 1
                econ_group.append(agent)
    model.random.shuffle(econ_group)
    final_group.extend(econ_group)

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
