import os
import pandas as pd
from datetime import datetime

from time_lord import time_track


def _sub_comparator(data, dt):
    """
    Very heavy calculations
    Раз векторным пока не получилось
    :param data: данные вида (id, time)
        :type data: Pandas.Series
    :param dt: Delta time, ограничение по времени для инцидентов
        :type dt: float
    :return (Pandas.Series): Преобразованные данные вида (id, time[transform as count])
    """
    index_list, values_list = data.index.tolist(), data.values.tolist()
    copy_values = values_list[:-1].copy()

    current = values_list.pop()
    limiter = len(values_list)

    while values_list:
        idx = index_list.pop()
        data[idx] += sum([(current - previous) < dt for previous in copy_values[:limiter]])
        current = values_list.pop()
        limiter -= 1

    return data


@time_track
def incidents(m, delta, df_file, output_file, console=False):
    """
    Функция, вычисляющая для каждого из N инцидентов количество инцидентов, удовлетворяющих следующим условиям:
        1) Инцидент Xi предшествует инциденту Xj по времени (Ti < Tj),
        при этом разница по времени не превосходит dT (Ti - Tj < delta_time);
        2) Имеют значения feature1 и feature2, совпадающие с соответствующими значениями данного инцидента.
    Решение заключается в группировке данных по признакам (feature1, feature2) в новый фрейм, и определение разницы
    по времени между соседними инцидентами с проверкой условия (1) с помощью групповой функции (_sub_comparator)
    :param m: максимальное значение категориального признака (int): [0, m-1]
    :param delta: ограничение по времени для инцидентов
        :type delta: float
    :param df_file: путь к входному файлу с инцидентами
        :type df_file: str
    :param output_file: выходной файл с инцидентами
        :type output_file: csv (рекомендуется)
    :param console: Вывод результатов на консоль (при этом файл также сохранится)
        :type console: bool
    :return: Результат pandas.Series [console=True] или user-message str
    """

    df_incidents = pd.read_csv(df_file,
                               index_col='id',
                               dtype={'feature1': 'uint8', 'feature2': 'uint8', 'time': 'float64'}
                               )

    df_incidents.sort_values(['time'], inplace=True)
    diffs = df_incidents. \
        rename(columns={'time': 'count'}). \
        groupby(['feature1', 'feature2'])['count']. \
        apply(_sub_comparator, dt=delta).astype(int)

    curr_date = datetime.now()
    path = os.path.normpath(os.path.dirname(__file__) + '/outputs' +
                            f'/{curr_date.year}_{curr_date.month}_{curr_date.day}')
    os.makedirs(path, exist_ok=True)

    diffs.sort_index(inplace=True)
    diffs.to_csv(os.path.join(path, output_file), index_label='id')

    return diffs if console else f"Результат сохранён в /outputs/*current date*/{output_file}"
