import random

IMD = 4  # impact melee difficulty
KD = 5  # kill difficulty


def calculate_distance_kills(s_atk, s_obj):
    impact_ratio = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # restore impact probability

    s_atk_dA = s_atk.get_dA()  # getting necessary values
    s_atk_S = s_atk.get_S()
    obj_R = s_obj.get_R()

    for i in range(0, s_atk_dA):  # update probability
        impact_ratio[i] = 1

    shots_left = s_atk.units  # get total shots
    num_of_impacts = 0

    # calculate total impacts
    while shots_left > 0:
        if random.choice(impact_ratio) == 1:  # check if it was (0 = no impact, 1 = impact)
            num_of_impacts += 1  # if it was, update counter
        shots_left -= 1

    # calculate kill difficulty
    calc_difference = (obj_R - s_atk_S)  # calculate difference S/R
    kill_difficulty = KD + calc_difference
    if kill_difficulty <= 0:  # set min
        kill_difficulty = 1  # equal numbers means win, fix min to 1
    elif kill_difficulty > 10:  # set max
        kill_difficulty = 10

    impacts_left = num_of_impacts
    kills = 0

    # calculate total kills
    while impacts_left > 0:
        r2 = random.randint(0, 10)
        if r2 >= kill_difficulty:  # equal is a kill
            kills += 1
        impacts_left -= 1

    return kills


def calculate_artillery_kills(s_atk, s_obj):
    impact_ratio = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # restore impact probability

    s_atk_dA = s_atk.get_dA()
    s_atk_S = s_atk.get_S()
    obj_R = s_obj.get_R()

    for i in range(0, s_atk_dA):  # update probability
        impact_ratio[i] = 1

    num_of_impacts = 0

    if random.choice(impact_ratio) == 1:  # check if it was (0 = no impact, 1 = impact)
        num_of_impacts = 10  # if it was, update counter

    # calculate kill difficulty
    calculate_difference = (obj_R - s_atk_S)  # calculate difference S/R
    kill_difficulty = KD + calculate_difference
    if kill_difficulty <= 0:  # set min
        kill_difficulty = 1  # because equal numbers means win, we fix min to 1
    if kill_difficulty > 10:  # set max
        kill_difficulty = 10

    impacts_left = num_of_impacts
    kills = 0

    # calculate total kills
    while impacts_left > 0:
        r2 = random.randint(0, 10)
        if r2 >= kill_difficulty:  # if its at least than, will be a kill
            kills += 1
        impacts_left -= 1

    return kills


def calculate_melee_kills(s1, s2):
    s1_mA = s1.get_mA()
    s2_mA = s2.get_mA()
    s1_S = s1.get_S()
    s2_S = s2.get_S()
    s1_R = s1.get_R()
    s2_R = s2.get_R()

    s1_attacks_left = s1.get_front()
    s1_num_of_impacts = 0

    s2_attacks_left = s2.get_front()
    s2_num_of_impacts = 0

    calculate_difference_1 = (s1_mA - s2_mA) / 2.

    impact_difficulty_1 = IMD - calculate_difference_1

    if impact_difficulty_1 <= 0:  # set min
        impact_difficulty_1 = 1  # equal numbers means win, fix min to 1
    if impact_difficulty_1 > 10:  # set max
        impact_difficulty_1 = 10

    impact_difficulty_2 = IMD + calculate_difference_1

    if impact_difficulty_2 <= 0:  # set min
        impact_difficulty_2 = 1  # equal numbers means win, fix min to 1
    if impact_difficulty_2 > 10:  # set max
        impact_difficulty_2 = 10

    while s1_attacks_left > 0:
        r = random.randint(0, 10)
        if r >= impact_difficulty_1:
            s1_num_of_impacts += 1
        s1_attacks_left -= 1

    while s2_attacks_left > 0:
        r2 = random.randint(0, 10)
        if r2 >= impact_difficulty_2:
            s2_num_of_impacts += 1
        s2_attacks_left -= 1

    calculate_difference2 = (s2_R - s1_S)
    kill_difficulty_1 = KD + calculate_difference2
    if kill_difficulty_1 <= 0:  # set min
        kill_difficulty_1 = 1  # equal numbers means win, fix min to 1
    if kill_difficulty_1 > 10:  # set max
        kill_difficulty_1 = 10

    calculate_difference_3 = (s1_R - s2_S)
    kill_difficulty_2 = KD + calculate_difference_3
    if kill_difficulty_2 <= 0:  # set min
        kill_difficulty_2 = 1  # equal numbers means win, fix min to 1
    if kill_difficulty_2 > 10:  # set max
        kill_difficulty_2 = 10

    # calculate s1 kills
    s1_wounds_left = s1_num_of_impacts
    s1_kills = 0

    while s1_wounds_left > 0:
        r3 = random.randint(0, 10)
        if r3 >= kill_difficulty_1:  # if its at least than, will be a kill
            s1_kills += 1
        s1_wounds_left -= 1

    # calculate s2 kills
    s2_wounds_left = s2_num_of_impacts
    s2_kills = 0

    while s2_wounds_left > 0:
        r4 = random.randint(0, 10)
        if r4 >= kill_difficulty_2:  # if its at least than, will be a kill
            s2_kills += 1
        s2_wounds_left -= 1

    return s1_kills, s2_kills
