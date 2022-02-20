"""מציאת התת מחרוזת הכי ארוכה במחרוזת"""
def main():
    original_string = "baasdaddf31"
    # [original_string, current_substring,current_substring_times, max_times_substring, max_times] :מקרא
    final_list = rec([original_string, original_string, 0, original_string, 0])
    print(f"{final_list[3]} appears {final_list[4]} times.")
    way2(original_string)


def rec(list1):
    """על ידי רקורסיה"""
    # האורך המינימלי של תת מחרוזת הוא 2 וזהו התנאי עצירה
    if len(list1[1]) == 2:
        return list1
    # ניצור שלוש רשימות ל: מחרוזת העיקרית, מחרוזת החתוכה מימין, מחרוזת החתוכה משמאל
    list1[2] = list1[0].count(list1[1])
    list2 = [list1[0], list1[1][:-1], list1[0].count(list1[1][:-1]), "", 0]
    list3 = [list1[0], list1[1][1:], list1[0].count(list1[1][1:]), "", 0]

    # נשים באינדקסים 3,4 ערכים מעודכנים של התת מחרוזת שמופיעה הכי הרבה ואת כמות הפעמים שהיא מופיעה
    max_times = max(list1[2], list2[2], list3[2])  # נבדוק למי יש תת מחרוזת נוכחית הכי ארוכה ונעדכן את זה בזכרון של כולם
    if max_times == list1[2]:
        list1[3], list1[4] = list1[1], list1[2]
        list2[3], list2[4] = list1[1], list1[2]
        list3[3], list3[4] = list1[1], list1[2]
    elif max_times == list2[2]:
        list1[3], list1[4] = list2[1], list2[2]
        list2[3], list2[4] = list2[1], list2[2]
        list3[3], list3[4] = list2[1], list2[2]
    else:
        list1[3], list1[4] = list3[1], list3[2]
        list2[3], list2[4] = list3[1], list3[2]
        list3[3], list3[4] = list3[1], list3[2]

    # נשלח את המחרוזות החתוכות לרקורסיה ונקבל רשימה שמכילה את התת מחרוזת שמופיעה הכי הרבה פעמים אצל כל אחת
    new_list2 = rec(list2)
    new_list3 = rec(list3)

    # נחזיר את התת מחרוזת שמופיעה הכי הרבה פעמים
    max_times = max(list1[4], new_list2[4], new_list3[4])
    if max_times == list1[4]:
        return list1
    elif max_times == new_list2[4]:
        return new_list2
    else:
        return new_list3


def way2(string):
    """הדרך הפשוטה ללא רקורסיה"""
    maximum = 1
    substring = string
    for i in range(len(string)):
        for j in range(i+2, len(string)+1):
            if string.count(string[i:j]) > maximum:
                maximum = string.count(string[i:j])
                substring = string[i:j]
    print(f"{substring} appears {maximum} times.")


if __name__ == "__main__":
    main()
