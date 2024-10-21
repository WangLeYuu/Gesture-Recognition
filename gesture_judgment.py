import math


"""
Calculate the distance between two points: L2 distance (Euclidean distance)
"""
def points_distance(x0, y0, x1, y1):
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


"""
Calculate the angle between two line segments in radians
"""
def compute_angle(x0, y0, x1, y1, x2, y2, x3, y3):
    AB = [x1 - x0, y1 - y0]
    CD = [x3 - x2, y3 - y2]

    dot_product = AB[0] * CD[0] + AB[1] * CD[1]

    AB_distance = points_distance(x0, y0, x1, y1) + 0.001   # Prevent the denominator from appearing as 0
    CD_distance = points_distance(x2, y2, x3, y3) + 0.001

    cos_theta = dot_product / (AB_distance * CD_distance)

    theta = math.acos(cos_theta)

    return theta


"""
Detect the status of all fingers (determine whether each finger is bent or extended)
The thumb only has two states: bent and straight. Other fingers, in addition to bent and straight, also have a third state (the fingers are not straight, but they have not reached the bending standard). The third state is for subsequent updates and iterations and cannot be used here
"""
def detect_all_finger_state(all_points):

    finger_first_angle_bend_threshold = math.pi * 0.25  # Thumb bending threshold
    finger_other_angle_bend_threshold = math.pi * 0.5  # Other finger bending thresholds
    finger_other_angle_straighten_threshold = math.pi * 0.2  # Other finger extension threshold

    first_is_bend = False
    first_is_straighten = False
    second_is_bend = False
    second_is_straighten = False
    third_is_bend = False
    third_is_straighten = False
    fourth_is_bend = False
    fourth_is_straighten = False
    fifth_is_bend = False
    fifth_is_straighten = False

    finger_first_angle = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point1'][0], all_points['point1'][1],
                                        all_points['point2'][0], all_points['point2'][1], all_points['point4'][0], all_points['point4'][1])
    finger_sencond_angle = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point5'][0], all_points['point5'][1],
                                        all_points['point6'][0], all_points['point6'][1], all_points['point8'][0], all_points['point8'][1])
    finger_third_angle = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point9'][0], all_points['point9'][1],
                                        all_points['point10'][0], all_points['point10'][1], all_points['point12'][0], all_points['point12'][1])
    finger_fourth_angle = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point13'][0], all_points['point13'][1],
                                        all_points['point14'][0], all_points['point14'][1], all_points['point16'][0], all_points['point16'][1])
    finger_fifth_angle = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point17'][0], all_points['point17'][1],
                                        all_points['point18'][0], all_points['point18'][1], all_points['point20'][0], all_points['point20'][1])

    if finger_first_angle > finger_first_angle_bend_threshold:              # Determine if the thumb is bent
        first_is_bend = True
        first_is_straighten = False
    else:
        first_is_bend = False
        first_is_straighten = True

    if finger_sencond_angle > finger_other_angle_bend_threshold:            # Determine if the index finger is bent
        second_is_bend = True
    elif finger_sencond_angle < finger_other_angle_straighten_threshold:
        second_is_straighten = True
    else:
        second_is_bend = False
        second_is_straighten = False

    if finger_third_angle > finger_other_angle_bend_threshold:              # Determine if the middle finger is bent
        third_is_bend = True
    elif finger_third_angle < finger_other_angle_straighten_threshold:
        third_is_straighten = True
    else:
        third_is_bend = False
        third_is_straighten = False

    if finger_fourth_angle > finger_other_angle_bend_threshold:             # Determine if the ring finger is bent
        fourth_is_bend = True
    elif finger_fourth_angle < finger_other_angle_straighten_threshold:
        fourth_is_straighten = True
    else:
        fourth_is_bend = False
        fourth_is_straighten = False

    if finger_fifth_angle > finger_other_angle_bend_threshold:              # Determine if the little finger is bent
        fifth_is_bend = True
    elif finger_fifth_angle < finger_other_angle_straighten_threshold:
        fifth_is_straighten = True
    else:
        fifth_is_bend = False
        fifth_is_straighten = False

    # Save the bent or extended state of the fingers in the dictionary to simplify the parameters of subsequent functions
    bend_states = {'first': first_is_bend, 'second': second_is_bend, 'third': third_is_bend, 'fourth': fourth_is_bend, 'fifth': fifth_is_bend}
    straighten_states = {'first': first_is_straighten, 'second': second_is_straighten, 'third': third_is_straighten, 'fourth': fourth_is_straighten, 'fifth': fifth_is_straighten}

    return bend_states, straighten_states


"""
Determine if it is an OK gesture
"""
def judge_OK(all_points, bend_states, straighten_states):

    angle5_6_and_6_8 = compute_angle(all_points['point5'][0], all_points['point5'][1], all_points['point6'][0], all_points['point6'][1],
                                    all_points['point6'][0], all_points['point6'][1], all_points['point8'][0], all_points['point8'][1])

    if angle5_6_and_6_8 > 0.1 * math.pi and straighten_states['third'] and straighten_states['fourth'] and straighten_states['fifth']:

        distance4_and_8 = points_distance(all_points['point4'][0], all_points['point4'][1], all_points['point8'][0], all_points['point8'][1])
        distance2_and_6 = points_distance(all_points['point2'][0], all_points['point2'][1], all_points['point6'][0], all_points['point6'][1])
        distance4_and_6 = points_distance(all_points['point4'][0], all_points['point4'][1], all_points['point6'][0], all_points['point6'][1])

        if distance4_and_8 < distance2_and_6 and distance4_and_6 > distance4_and_8 and all_points['point11'][1] < all_points['point10'][1]:
            return 'OK'
        else:
            return False
    else:
        return False


"""
Determine whether it is a Return gesture
"""
def judge_Return(all_points, bend_states, straighten_states):

    angle18_6_and_18_18_ = compute_angle(all_points['point18'][0], all_points['point18'][1], all_points['point6'][0], all_points['point6'][1],
                                        all_points['point18'][0], all_points['point18'][1], all_points['point18'][0] + 10, all_points['point18'][1])
    angle_6_18_and_6_6_ = compute_angle(all_points['point6'][0], all_points['point6'][1], all_points['point18'][0], all_points['point18'][1],
                                        all_points['point6'][0], all_points['point6'][1], all_points['point6'][0] + 10, all_points['point6'][1])
    angle_0_2_and_0_17 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point2'][0], all_points['point2'][1],
                                        all_points['point0'][0], all_points['point0'][1], all_points['point17'][0], all_points['point17'][1])

    if (bend_states['first'] and bend_states['second'] and bend_states['third'] and bend_states['fourth'] and bend_states['fifth'] and
            angle_0_2_and_0_17 > 0.15 * math.pi and
            all_points['point7'][1] > all_points['point6'][1] and all_points['point11'][1] > all_points['point10'][1] and
            all_points['point15'][1] > all_points['point14'][1] and all_points['point19'][1] > all_points['point18'][1]):

        if angle18_6_and_18_18_ < 0.1 * math.pi or angle_6_18_and_6_6_ < 0.1 * math.pi:
            return 'Return'
        else:
            return False
    else:
        return False


"""
Determine if it is a Left gesture
"""
def judge_Left(all_points, bend_states, straighten_states):

    angle5_6_and_6_8 = compute_angle(all_points['point5'][0], all_points['point5'][1], all_points['point6'][0], all_points['point6'][1],
                                    all_points['point6'][0], all_points['point6'][1], all_points['point8'][0], all_points['point8'][1])
    angle9_10_and_10_12 = compute_angle(all_points['point9'][0], all_points['point9'][1], all_points['point10'][0], all_points['point10'][1],
                                        all_points['point10'][0], all_points['point10'][1], all_points['point12'][0], all_points['point12'][1])
    angle13_14_and_14_16 = compute_angle(all_points['point13'][0], all_points['point13'][1], all_points['point14'][0], all_points['point14'][1],
                                        all_points['point14'][0], all_points['point14'][1], all_points['point16'][0], all_points['point16'][1])
    angle17_18_and_18_20 = compute_angle(all_points['point17'][0], all_points['point17'][1], all_points['point18'][0], all_points['point18'][1],
                                        all_points['point18'][0], all_points['point18'][1], all_points['point20'][0], all_points['point20'][1])
    angle0_6_and_0_4 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point6'][0], all_points['point6'][1],
                                    all_points['point0'][0], all_points['point0'][1], all_points['point4'][0], all_points['point4'][1])
    angle0_5_and_0_17 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point5'][0], all_points['point5'][1],
                                    all_points['point0'][0], all_points['point0'][1], all_points['point17'][0], all_points['point17'][1])

    if ((straighten_states['first'] and bend_states['second'] and bend_states['third'] and bend_states['fourth'] and bend_states['fifth']) or
        (straighten_states['first'] and angle5_6_and_6_8 > 0.2 * math.pi and angle9_10_and_10_12 > 0.2 * math.pi and
        angle13_14_and_14_16 > 0.2 * math.pi and angle17_18_and_18_20 > 0.2 * math.pi)):

        angle0_0__and_0_4 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point0'][0] + 10, all_points['point0'][1],
                                    all_points['point0'][0], all_points['point0'][1], all_points['point4'][0], all_points['point4'][1])

        if (angle0_5_and_0_17 > 0.15 * math.pi and angle0_0__and_0_4 > 0.7 * math.pi and all_points['point3'][0] < all_points['point2'][0] and
            angle0_6_and_0_4 > 0.1 * math.pi and all_points['point11'][1] > all_points['point10'][1] and all_points['point7'][1] > all_points['point6'][1] and
            all_points['point15'][1] > all_points['point14'][1] and all_points['point19'][1] > all_points['point18'][1]):
            return 'Left'
        else:
            return False
    else:
        return False


"""
Determine if it is a Right gesture
"""
def judge_Right(all_points, bend_states, straighten_states):

    angle0_5_and_0_17 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point5'][0], all_points['point5'][1],
                                    all_points['point0'][0], all_points['point0'][1], all_points['point17'][0], all_points['point17'][1])
    angle5_6_and_6_8 = compute_angle(all_points['point5'][0], all_points['point5'][1], all_points['point6'][0], all_points['point6'][1],
                                    all_points['point6'][0], all_points['point6'][1], all_points['point8'][0], all_points['point8'][1])
    angle9_10_and_10_12 = compute_angle(all_points['point9'][0], all_points['point9'][1], all_points['point10'][0], all_points['point10'][1],
                                        all_points['point10'][0], all_points['point10'][1], all_points['point12'][0], all_points['point12'][1])
    angle13_14_and_14_16 = compute_angle(all_points['point13'][0], all_points['point13'][1], all_points['point14'][0], all_points['point14'][1],
                                        all_points['point14'][0], all_points['point14'][1], all_points['point16'][0], all_points['point16'][1])
    angle17_18_and_18_20 = compute_angle(all_points['point17'][0], all_points['point17'][1], all_points['point18'][0], all_points['point18'][1],
                                        all_points['point18'][0], all_points['point18'][1], all_points['point20'][0], all_points['point20'][1])
    angle0_6_and_0_4 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point6'][0], all_points['point6'][1],
                                    all_points['point0'][0], all_points['point0'][1], all_points['point4'][0], all_points['point4'][1])

    if ((straighten_states['first'] and bend_states['second'] and bend_states['third'] and bend_states['fourth'] and bend_states['fifth']) or
        (straighten_states['first'] and angle5_6_and_6_8 > 0.2 * math.pi and angle9_10_and_10_12 > 0.2 * math.pi and
        angle13_14_and_14_16 > 0.2 * math.pi and angle17_18_and_18_20 > 0.2 * math.pi)):

        angle0_0__and_0_4 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point0'][0] + 10, all_points['point0'][1],
                                        all_points['point0'][0], all_points['point0'][1], all_points['point4'][0], all_points['point4'][1])

        if (angle0_5_and_0_17 > 0.15 * math.pi and angle0_0__and_0_4 < 0.25 * math.pi and all_points['point3'][0] > all_points['point2'][0] and
            angle0_6_and_0_4 > 0.1 * math.pi and all_points['point11'][1] > all_points['point10'][1] and all_points['point7'][1] > all_points['point6'][1] and
            all_points['point15'][1] > all_points['point14'][1] and all_points['point19'][1] > all_points['point18'][1]):
            return 'Right'
        else:
            return False
    else:
        return False


"""
Determine whether it is a Like gesture
"""
def judge_Like(all_points, bend_states, straighten_states):

    angle2_4_and_2_8 = compute_angle(all_points['point2'][0], all_points['point2'][1], all_points['point4'][0], all_points['point4'][1],
                                    all_points['point2'][0], all_points['point2'][1], all_points['point8'][0], all_points['point8'][1])
    angle2_3_and_3_4 = compute_angle(all_points['point2'][0], all_points['point2'][1], all_points['point3'][0], all_points['point3'][1],
                                    all_points['point3'][0], all_points['point3'][1], all_points['point4'][0], all_points['point4'][1])
    angle5_6_and_6_8 = compute_angle(all_points['point5'][0], all_points['point5'][1], all_points['point6'][0], all_points['point6'][1],
                                    all_points['point6'][0], all_points['point6'][1], all_points['point8'][0], all_points['point8'][1])
    angle9_10_and_10_12 = compute_angle(all_points['point9'][0], all_points['point9'][1], all_points['point10'][0], all_points['point10'][1],
                                        all_points['point10'][0], all_points['point10'][1], all_points['point12'][0], all_points['point12'][1])
    angle13_14_and_14_16 = compute_angle(all_points['point13'][0], all_points['point13'][1], all_points['point14'][0], all_points['point14'][1],
                                        all_points['point14'][0], all_points['point14'][1], all_points['point16'][0], all_points['point16'][1])
    angle17_18_and_18_20 = compute_angle(all_points['point17'][0], all_points['point17'][1], all_points['point18'][0], all_points['point18'][1],
                                        all_points['point18'][0], all_points['point18'][1], all_points['point20'][0], all_points['point20'][1])
    angle0_6_and_0_4 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point6'][0], all_points['point6'][1],
                                    all_points['point0'][0], all_points['point0'][1], all_points['point4'][0], all_points['point4'][1])

    if ((angle2_3_and_3_4 < 0.2 * math.pi and bend_states['second'] and bend_states['third'] and bend_states['fourth'] and bend_states['fifth']) or
        (angle2_3_and_3_4 < 0.2 * math.pi and angle5_6_and_6_8 > 0.2 * math.pi and angle9_10_and_10_12 > 0.2 * math.pi and
        angle13_14_and_14_16 > 0.2 * math.pi and angle17_18_and_18_20 > 0.2 * math.pi)):

        angle0_0__and_0_4 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point0'][0] + 10, all_points['point0'][1],
                                        all_points['point0'][0], all_points['point0'][1], all_points['point4'][0], all_points['point4'][1])

        if (angle0_0__and_0_4 > 0.25 * math.pi and angle0_0__and_0_4 < 0.75 * math.pi and
            all_points['point3'][1] > all_points['point4'][1] and all_points['point5'][1] < all_points['point9'][1] and all_points['point9'][1] < all_points['point13'][1] and
                all_points['point13'][1] < all_points['point17'][1] and all_points['point2'][1] < all_points['point5'][1] and
                angle0_6_and_0_4 > 0.1 * math.pi and angle2_4_and_2_8 > 0.1 * math.pi):
            return 'Like'
        else:
            return False
    else:
        return False


"""
Determine if it is a Pause gesture
"""
def judge_Pause(all_points, bend_states, straighten_states):

    angle0_5_and_0_17 = compute_angle(all_points['point0'][0], all_points['point0'][1], all_points['point5'][0], all_points['point5'][1],
                                    all_points['point0'][0], all_points['point0'][1], all_points['point17'][0], all_points['point17'][1])
    angle2_3_and_2_4 = compute_angle(all_points['point2'][0], all_points['point2'][1], all_points['point3'][0], all_points['point3'][1],
                                    all_points['point2'][0], all_points['point2'][1], all_points['point4'][0], all_points['point4'][1])
    angle5_6_and_6_8 = compute_angle(all_points['point5'][0], all_points['point5'][1], all_points['point6'][0], all_points['point6'][1],
                                    all_points['point6'][0], all_points['point6'][1], all_points['point8'][0], all_points['point8'][1])
    angle9_10_and_10_12 = compute_angle(all_points['point9'][0], all_points['point9'][1], all_points['point10'][0], all_points['point10'][1],
                                        all_points['point10'][0], all_points['point10'][1], all_points['point12'][0], all_points['point12'][1])
    angle13_14_and_14_16 = compute_angle(all_points['point13'][0], all_points['point13'][1], all_points['point14'][0], all_points['point14'][1],
                                        all_points['point14'][0], all_points['point14'][1], all_points['point16'][0], all_points['point16'][1])
    angle17_18_and_18_20 = compute_angle(all_points['point17'][0], all_points['point17'][1], all_points['point18'][0], all_points['point18'][1],
                                        all_points['point18'][0], all_points['point18'][1], all_points['point20'][0], all_points['point20'][1])
    angle1_2_and_2_4 = compute_angle(all_points['point1'][0], all_points['point1'][1], all_points['point2'][0], all_points['point2'][1],
                                    all_points['point2'][0], all_points['point2'][1], all_points['point4'][0], all_points['point4'][1])

    if (angle2_3_and_2_4 < 0.2 * math.pi and angle5_6_and_6_8 < 0.07 * math.pi and angle9_10_and_10_12 < 0.07 * math.pi and angle13_14_and_14_16 < 0.07 * math.pi and
        angle17_18_and_18_20 < 0.07 * math.pi and angle9_10_and_10_12 < 0.07 * math.pi and angle1_2_and_2_4 < 0.25 * math.pi):
        if (angle0_5_and_0_17 > 0.1 * math.pi and all_points['point3'][1] > all_points['point4'][1] and all_points['point6'][1] > all_points['point8'][1] and
            all_points['point10'][1] > all_points['point12'][1]):
            return 'Pause'
        else:
            return False
    else:
        return False


"""
Detect the current gesture and return the current gesture
"""
def detect_hand_state(all_points, bend_states, straighten_states):

    state_OK = judge_OK(all_points, bend_states, straighten_states)
    state_Return = judge_Return(all_points, bend_states, straighten_states)
    state_Left = judge_Left(all_points, bend_states, straighten_states)
    state_Right = judge_Right(all_points, bend_states, straighten_states)
    state_Like = judge_Like(all_points, bend_states, straighten_states)
    state_Pause = judge_Pause(all_points, bend_states, straighten_states)

    if state_OK == 'OK':
        return 'OK'
    elif state_Return == 'Return':
        return 'Return'
    elif state_Left == 'Left':
        return 'Left'
    elif state_Right == 'Right':
        return 'Right'
    elif state_Like == 'Like':
        return 'Like'
    elif state_Pause == 'Pause':
        return 'Pause'
    else:
        return 'None'