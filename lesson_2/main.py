import csv
import datetime
import json
import re
import yaml


# 1. Задание на закрепление знаний по модулю CSV. Написать скрипт, осуществляющий выборку определенных данных из
# файлов info_1.txt, info_2.txt, info_3.txt и формирующий новый «отчетный» файл в формате CSV. Для этого: Создать
# функцию get_data(), в которой в цикле осуществляется перебор файлов с данными, их открытие и считывание данных. В
# этой функции из считанных данных необходимо с помощью регулярных выражений извлечь значения параметров
# «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения каждого параметра поместить в
# соответствующий список. Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list,
# os_type_list. В этой же функции создать главный список для хранения данных отчета — например, main_data — и
# поместить в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта»,
# «Тип системы». Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для
# каждого файла); Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать
# получение данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий
# CSV-файл; Проверить работу программы через вызов функции write_to_csv().


def get_data(filenames_list: list):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    headers = []
    for filename in filenames_list:
        with open(filename, 'r', encoding='cp1251') as file:
            text = file.read()
            result_data = re.split(r'\n', text)
            os_prod_list.append(result_data[3].split(':')[1].strip())
            os_name_list.append(result_data[1].split(':')[1].strip())
            os_code_list.append(result_data[8].split(':')[1].strip())
            os_type_list.append(result_data[11].split(':')[1].strip())

            result_headers = re.findall(r'\w+.\w+:', text)
            headers.append(result_headers[3][:-1])
            headers.append(result_headers[1][:-1])
            headers.append(result_headers[8][:-1])
            headers.append(result_headers[12][:-1])

    headers = list(set(headers))
    headers.sort()
    main_data = [headers, os_prod_list, os_type_list, os_code_list, os_name_list]
    for i in range(len(os_name_list)):
        main_data.append([os_prod_list[i], os_type_list[i], os_code_list[i], os_name_list[i]])
    return main_data


def write_to_csv(filename: str, files_list: list):
    with open(f'{filename}.csv', 'w') as file:
        data = get_data(files_list)
        file_writer = csv.writer(file)
        for row in data:
            file_writer.writerow(row)
    print('Done!')


files = ['info_1.txt', 'info_2.txt', 'info_3.txt']
write_to_csv('main_data', files)


# ### 2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# # Написать скрипт, автоматизирующий его заполнение данными. Для этого:
# Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
# цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
# orders.json. При записи данных указать величину отступа в 4 пробельных символа;
# Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.


def write_order_to_json(item: str, quantity: int, price: float, buyer: str, date):
    with open('orders.json', 'w') as f:
        data = {
            'item': item,
            'quantity': quantity,
            'price': price,
            'buyer': buyer,
            'date': str(date)
        }

        json.dump(data, f, indent=4)
    print('Done!')


write_order_to_json(
    item='T-Shirt',
    quantity=10,
    price=9.99,
    buyer='Jonh',
    date=datetime.datetime.now(),
)

# ### 3. Задание на закрепление знаний по модулю yaml. Написать скрипт, автоматизирующий сохранение данных в файле
# # YAML-формата. Для этого:
# Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
# третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
# кодировке ASCII (например, €);
# Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла
# с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
# Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.

data = {
    'admins': ['Rick', 'Alex', 'Morgan'],
    'count': 21,
    'symbols': {
        1: [1, '€'],
        2: [2, '§']
    },
}
with open('file.yaml', 'w') as yaml_file:
    yaml.dump(data, yaml_file, default_flow_style=True, allow_unicode=True)

with open('file.yaml', 'r') as read_file:
    result = yaml.safe_load(read_file)
    print(result)
