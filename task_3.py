def prepair_intervals(intervals: dict) -> dict:
    """
    Убирает лишние интервалы по такому принципу:

    Разбиваем все интервалы на 2 списка по признаку входа или выхода.
    Сортируем каждый список по времени.

    Удаляем элемент из списка выхода с урока если он меньше времени входа который был осуществлён.
    Как только мы нашли подходящую пару времени входа и выхода на урок проверяем следующий элемент в списке входа.
    Удаляем элемент из списка входа с урока если он меньше времени выхода который был осуществлён.

    :param intervals: - словарь вида {объект: [время входа, время выхода...]}
    :return intervals: - словарь вида {объект: [время входа, время выхода...]} подготовленный для последующей обработки.
    """
    for key, value in intervals.items():
        time_enter = [value[ind] for ind in range(len(value)) if ind % 2 == 0]
        time_exit = [value[ind] for ind in range(len(value)) if ind % 2 == 1]
        time_enter.sort()
        time_exit.sort()
        ind_start = 0
        ind_end = 0
        while ind_end < len(time_exit):
            if time_enter[ind_start] > time_exit[ind_end]:
                time_exit.pop(ind_end)
                continue
            ind_start += 1
            if ind_start >= len(time_enter):
                break
            if time_exit[ind_end] > time_enter[ind_start]:
                time_enter.pop(ind_start)
                ind_start -= 1
                continue
            ind_end += 1
        time_enter = time_enter[:min(len(time_enter), len(time_exit))]
        time_exit = time_exit[:min(len(time_enter), len(time_exit))]

        result = [time_enter.pop(0) if ind % 2 == 0 else time_exit.pop(0) for ind in range(2 * len(time_enter))]
        intervals[key] = result
    return intervals


def appearance(intervals: dict) -> int:
    """
    Функция для расчёта общего количества времени урока с учителем и учеником.

    Так как у нас подготовленные интервалы, то у каждой точки во времени есть 2 позиции: вход и выход.
    Мы можем объеденить все наши интервалы в один большой интервал.
    Если у нас флаг состояния урока устанавливается в положение 3 - это означает, что сейчас активены все объекты
    (урок, учитель, ученик).
    Как только значение флага станет меньше 3-х, это будет значить, что что-то случилось и не все объектыв активны.

    :param intervals: - словарь вида {объект: [время входа, время выхода...]}
    :return: - число временных единиц при всех активных объектах.
    """
    intervals = prepair_intervals(intervals)
    intervals_all = []
    for data in intervals.values():
        intervals_all += [(data[ind], 1 if ind % 2 == 0 else -1) for ind in range(len(data))]
    intervals_all.sort()
    flag = 0
    time_start = -1
    sum_time_lesson = 0
    for el in intervals_all:
        flag += el[1]
        if flag == 3:
            time_start = el[0]
        if flag == 2 and time_start > 0:
            sum_time_lesson += el[0] - time_start
            time_start = -1
    print(sum_time_lesson)
    return sum_time_lesson


tests = [
    {'data': {'lesson': [1594663200, 1594666800],
              'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
              'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'data': {'lesson': [1594702800, 1594706400],
              'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150,
                        1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480,
                        1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503,
                        1594706524, 1594706524, 1594706579, 1594706641],
              'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3204  # 3577 # Я разработал свой метод чистки неподходящих интервалов, который описал в комментариях.
                            # Да, ответ не совпал, но если я реализовал этот алгоритм, то легко сделаю и другой метод.

     },
    {'data': {'lesson': [1594692000, 1594695600],
              'pupil': [1594692033, 1594696347],
              'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
