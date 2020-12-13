import os
import pandas as pd

from datetime import datetime

from time_lord import time_track


@time_track
def incidents(m, delta, df_file, output_file, console=False):
    """
    Функция, вычисляющая для каждого из N инцидентов количество инцидентов, удовлетворяющих следующим условиям:
        1) Инцидент Xi предшествует инциденту Xj по времени (Ti < Tj),
        при этом разница по времени не превосходит dT (Ti - Tj < delta_time);
        2) Имеют значения feature1 и feature2, совпадающие с соответствующими значениями данного инцидента.
    Решение заключается в группировке данных по признакам (feature1, feature2) в новый фрейм, и определение разницы
    по времени между соседними инцидентами с проверкой условия (1) с помощью групповой аггрегации (Series.transform)
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
                               dtype={'feature1': 'uint8', 'feature2': 'uint8', 'time': 'float32'}
                               )

    df_incidents.sort_values(['time'], inplace=True)
    diffs = df_incidents.rename(columns={'time': 'count'}).groupby(['feature1', 'feature2'])['count'].transform(
        lambda label: (abs(label - label.shift()) < delta).cumsum()).astype(int)

    curr_date = datetime.now()
    path = os.path.normpath(os.path.dirname(__file__) + '/outputs' +
                            f'/{curr_date.year}_{curr_date.month}_{curr_date.day}')
    os.makedirs(path, exist_ok=True)

    diffs.sort_index(inplace=True)
    diffs.to_csv(os.path.join(path, output_file), index_label='id')

    return diffs if console else f"Результат сохранён в /outputs/*current date*/{output_file}"


if __name__ == '__main__':
    print(incidents(2, 0.3, 'files/incidents.csv', 'out.csv'))
