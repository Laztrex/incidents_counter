# Incidents counter
Функция, подсчитывающая количество инцидентов в data frame, удовлетворяющих следующим условиям:
- Инцидент_1 предшествуют инциденту_2 по времени, при этом разница по времени не превосходит ∆T;
- feature1 и feature2 инцидентов совпадают.
> Тестовое задание
---
## Описание
Входной dataframe имеет структуру Nx4:  
~~~
id,feature1,feature2,time  
row_num,[0; M-1],[0; M-1],[0., inf]

type(id): int
type(feature1, feature2): int
type(time): float
~~~
Функция выполнена в pandas-way подходе  

Command line:  
- **Подсчитать инциденты** 
~~~
python run.py -dt 0.3 -df files/incidents.csv -o ooo.csv
~~~
Расшифровка: python name_module delta_time df_file(path) output file [-m]

- **Подробнее про параметры** 
~~~
python run.py -h
~~~
Именованные (согласно заданию):  
1. -m, _int_: Диапазон значений категориальных признаков
2. -dt (delta_time), _float_: признак времени, характеризует разницу во времени между двумя инцидентами
3. -df (dataframe_file), _str_ (path): путь к входному датафрейму
4. -o (output_file), _str_ (имя): файл для сохранения результатов. Файлы будут храниться в /outputs с распределением по дате
5. -c (console), _bool_: Вывод результата на консоль

- **Пример входного dataframe** 
~~~
id,feature1,feature2,time
0,1,0,0.206520219143
1,0,0,0.233725001118
2,0,1,0.760992754734
3,1,1,0.92776979943
4,1,0,0.569711498585
5,0,1,0.99224586863
6,0,0,0.593264390713
7,1,0,0.694181201747
8,1,1,0.823812651856
9,0,1,0.906011017725
~~~

- **Пример вывода на консоль** 
~~~
python run.py -dt 0.3 -df files/incidents.csv -o result.csv -c
~~~
~~~
id
0    0
1    0
2    0
3    1
4    0
5    2
6    0
7    1
8    0
9    1
Name: count, dtype: int32
~~~
- **Пример записи в csv-файл** 
~~~
id,count
0,0
1,0
2,0
3,1
4,0
5,2
6,0
7,1
8,0
9,1
~~~
- **Дополнительно**  
Также на вывод идёт время работы функции
~~~
Функция работала 0.014 секунд(ы)
~~~
Для небольшой оптимизации потребления оперативной памяти используется преобразование к подтипам
~~~
...,
dtype={'feature1': 'uint8', 'feature2': 'uint8', 'time': 'float32'},
...
~~~
Данный подход было решено не предавать анафеме, так как результат показал хорошую тенденцию к оптимизации памяти.
Пример с помощью *memory_profiler* на сгенерированном фрейме при M=100, N=1000000
~~~
@memory_profiler.profile
def incidents(m, delta, df_file, output_file, console=False):
...
~~~
~~~
python run.py -dt 0.3 -df files/big_incidents.csv -o result.csv
~~~
*До преобразования к подтипам*  
![Image alt](https://github.com/Laztrex/WeatherParser/raw/master/pics/before_subtypes.jpg)

*После преобразования к подтипам*  
![Image alt](https://github.com/Laztrex/WeatherParser/raw/master/pics/after_subtypes.jpg)

~~~
python3 give_weather.py push -s api -c Рязань -d 2020.08.12-2020.08.15
~~~

> При огромных входных данных практикуется обработка "по частям". Например, с помощью chunk'ов
>~~~
>for incident in pd.read_csv(incidents.csv, chunksize=chunksize):
>    # подсчитываем инциденты по условиям...
> В данной функции такой подход не реализовывался, но готовность масштабировать её имеется
>~~~

Для запуска тестов:
~~~
python -m unittest tests/test_incidents.py
~~~

- **Requirements**  
~~~
numpy==1.19.4
pandas==1.1.5
psutil==5.7.3
python-dateutil==2.8.1
pytz==2020.4
six==1.15.0

# Для исследования оптимизации памяти дополнительно
memory-profiler==0.58.0
~~~