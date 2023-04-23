import locale
import subprocess
from pprint import pprint


# 1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и содержание
# соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление в формат Unicode
# и также проверить тип и содержимое переменных.


def decode_python(words: list):
    for word in words:
        print(type(word), word)

    print('Result decoding unicode word in python:')
    unicode_words = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430',
                     '\u0441\u043e\u043a\u0435\u0442',
                     '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

    for un_word in unicode_words:
        print(type(un_word), un_word)


decode_python(['разработка', 'сокет', 'декоратор'])
print('*' * 100)


# 2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность кодов
# (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

def check_type_byte_words(words: list):
    print('Result second question:')
    for word in words:
        print(f'Word: {word}, Type: {type(word)}, Length: {len(word)}')


check_type_byte_words([b'class', b'function', b'method'])
print('*' * 100)
# 3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

first_word = b'attribute'
print(first_word)

# SyntaxError: bytes can only contain ASCII literal characters:
second_word = 'класс'.encode('ascii', 'replace')
print(second_word)

# SyntaxError: bytes can only contain ASCII literal characters:
third_word = 'функция'.encode('ascii', 'replace')
print(third_word)

fourth_word = b'type'
print(fourth_word)
print('*' * 100)

# 4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления в
# байтовое и выполнить обратное преобразование (используя методы encode и decode).

list_words = ['разработка', 'администрирование', 'protocol', 'standard']
list_byte_words = [word.encode() for word in list_words]
pprint(f"Result encoding words: {list_byte_words}")

decode_list_words = [byte_word.decode() for byte_word in list_byte_words]
pprint(f"Result decoding words: {decode_list_words}")
print('*' * 100)


# 5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип на
# кириллице.

def check_ping(site: list):
    subproc_ping = subprocess.Popen(site, stdout=subprocess.PIPE)
    for line in subproc_ping.stdout:
        l = line.decode('cp866')
        print(type(l), l)
        # Remove 'break' for checking ping
        break


youtube = ['ping', 'youtube.com']
google = ['ping', 'google.com']

check_ping(youtube)
check_ping(google)
print('*' * 100)

# 6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
# «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести
# его содержимое.
with open('test_file.txt', 'r', encoding='utf-8') as file:
    check_encoding_file = locale.getpreferredencoding()
    print(f'Encoding file: {check_encoding_file}')
    for line in file:
        print(line)
