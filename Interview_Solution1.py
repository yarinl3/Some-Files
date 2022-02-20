__author__ = 'Yarin Levi'
__email__ = 'yarinl330@gmail.com'
"""
My solution for 'Google Coding Interview With A College Student'
https://www.youtube.com/watch?v=3Q_oYDQ2whs&t=1991s
"""

from operator import itemgetter


def main():
    man1_list = [['9:00', '10:30'], ['12:00', '13:00'],['16:00', '18:00']]
    man1_range = ['9:00', '20:00']
    man2_list = [['10:00', '11:30'], ['12:30', '14:30'], ['14:30', '15:00'], ['16:00', '17:00']]
    man2_range = ['10:00', '18:30']
    # meeting time in minutes
    meeting_time = 30

    man1_list = convert_list(man1_list)
    man1_range = convert_list([man1_range])[0]
    man2_list = convert_list(man2_list)
    man2_range = convert_list([man2_range])[0]
    meeting_time /= 60

    x = max(man1_range[0], man2_range[0])
    x_in_range = False
    all_meetings = man1_list + man2_list
    all_meetings = sorted(all_meetings, key=itemgetter(0))

    success_list = []
    while True:
        y, z = -1, -1
        min_right_boundary = min(man1_range[1], man2_range[1])
        if x + meeting_time > min_right_boundary:
            break
        for i in all_meetings:
            if i[0] <= x < i[1]:
                x = i[1]
                x_in_range = True
                break
        if x_in_range is True:
            x_in_range = False
            continue
        for meeting in all_meetings:
            if meeting[0] > x:
                y = meeting[0]
                z = meeting[1]
                break
        if y != -1 and z != -1:
            if x + meeting_time <= y:
                success_list.append([x, y])
                x = y
            else:
                x = z
        else:
            success_list.append([x, min_right_boundary])
            break

    print(convert_back_to_string(success_list))


def convert_list(time_list):
    for i in range(len(time_list)):
        for j in range(2):
            time = time_list[i][j].split(':')
            time_list[i][j] = int(time[0]) + int(time[1]) / 60
    return time_list


def convert_back_to_string(time_list):
    for i in range(len(time_list)):
        for j in range(2):
            time_list[i][j] = f'{str(int(time_list[i][j]//1)).zfill(2)}:{str(int((time_list[i][j]%1) * 60)).zfill(2)}'
    return time_list


if __name__ == '__main__':
    main()
