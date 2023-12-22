'''
  家人生日提醒
'''

import datetime
import ulunar

familyBirthdays = {
'9': [(6, '陈立,邹武'), (27, '李四')],
'3': [(24, '王麻子')],
'4': [(21, '张三')],
'11': [(5, '汤正')],
}

def binary_search(sorted_data, search_number):
    left, right = 0, len(sorted_data) - 1

    while left <= right:
        mid = (left + right) // 2
        mid_number = sorted_data[mid][0]

        if mid_number == search_number:
            return sorted_data[mid]
        elif mid_number < search_number:
            left = mid + 1
        else:
            right = mid - 1

    return None

def get_familyBirthday(lunar:ulunar.Lunar) -> str :
    if f'{lunar.lunarMonth}' in familyBirthdays:
        person = binary_search(familyBirthdays[f'{lunar.lunarMonth}'], lunar.lunarDate)
        if person is not None:
            return person[1]
    return ''
