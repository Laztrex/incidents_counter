# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import sys

from incidents_analyze import incidents


def get_incidents(**kwargs):
    run_counting = incidents(**kwargs)
    print(run_counting)


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', default=2,
                        help='Диапазон значений категориальных признаков', type=int)
    parser.add_argument('-dt', '--delta', help='delta time, ограничение по времени '
                                               'при сравнении инцидентов', type=float)
    parser.add_argument('-df', '--df_file', help='Файл с инцидентами')
    parser.add_argument('-o', '--output_file', default='result.csv', help='Файл с результатами сравнения')
    parser.add_argument('-c', '--console', action='store_true', help='Вывод на консоль, опционально')

    return parser


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])
    get_incidents(**namespace.__dict__)
