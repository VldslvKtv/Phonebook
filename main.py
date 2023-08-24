import ast
import re


class Validation(object):
    """Класс для проверки вводимых данных."""

    @staticmethod
    def input_data():
        """Ввод данных типа str."""
        data: str = input()
        return data

    @staticmethod
    def validate_int():
        """Проверка ввода данных типа int."""
        while True:
            try:
                int_obj = int(input())
            except ValueError:
                print('Введите целое неотрицательное число.')
            else:
                return int_obj

    @staticmethod
    def validate_id(explantion: str, quantity: int, former_id: int):
        """Выставление id в зависимости от ситуации.
         Параметры: explantion: строка с названием поля
                    quantity: количество записей в справочнике
                    former_id: id изменямой записи
         Возвращаемые значения:
         При добавление записи(former_id = 0) - вернет новый id, при поиск записи(former_id = -1) - вернет None,
         при изменение записи - вернет id изменяемой записи.
        """
        if former_id == 0:
            new_id = quantity + 1
            print(f'{explantion}{new_id}')
            return new_id
        elif former_id == -1:
            print(f'{explantion}{None}')
            return None
        else:
            print(f'{explantion}{former_id}')
            return former_id

    @staticmethod
    def validate_titles(explantion: str):
        """Проверка ввода Name, Lastname, Surname. """
        while True:
            print(f'{explantion}', end="")
            title: str = Validation.input_data()
            if len(title) < 1 or not title.isalpha():
                print('Некорректный ввод. Введите ещё раз.')
            else:
                return title

    @staticmethod
    def validate_number(explantion: str):
        """Проверка ввода Work_phone,Personal_phone"""
        while True:
            print(f'{explantion}', end="")
            phone_number: str = Validation.input_data()
            if (len(phone_number) == 11 and
                phone_number.isdigit()) | (phone_number[0] == '+' and
                                           len(phone_number) == 12 and
                                           phone_number[1:].isdigit()) | (phone_number.casefold() == 'none'):
                return phone_number
            else:
                print('Некорректный номер. Введите ещё раз')

    @staticmethod
    def validation_line_number(quantity_lines: int):
        """Проверка ввода id при изменение записи"""
        while True:
            line_number: int = Validation.validate_int()
            if (line_number < 0) | (line_number > quantity_lines):
                print('Некорректно введен id записи. Попробуйте еще раз.')
            else:
                return line_number


class Record(object):
    """Класс для реализации записи справочника"""
    def __init__(self, id_record: int, name: str, lastname: str, surname: str, organization: str, work_phone: str,
                 personal_phone: str):
        self.id_record = id_record
        self.name = name
        self.lastname = lastname
        self.surname = surname
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    @classmethod
    def from_input(cls, former_id: int, quantity: int):
        """Заполнение полей обьекта класса Record.
        Параметры:  former_id: id изменяемой записи
                    quantity: количество записей в справочнике
        Возращает:
                   Обьект класса Record
        """
        return cls(
            Validation.validate_id('ID: ', quantity, former_id),
            Validation.validate_titles('Name: '),
            Validation.validate_titles('Lastname: '),
            Validation.validate_titles('Surname: '),
            Validation.validate_titles('Organization: '),
            Validation.validate_number('Work_phone: '),
            Validation.validate_number('Personal_phone: ')
        )

    def convert_record_to_dict(self):
        """Конвертация обьекта класса в словарь"""
        return {'ID': self.id_record, 'Name': self.name, 'Lastname': self.lastname, 'Surname': self.surname,
                'Organization': self.organization,
                'Work_phone': self.work_phone, 'Personal_phone': self.personal_phone}


def print_dict(array_of_dictionary: dict):
    """Вывод данных из словаря. Параметры: array_of_dictionary: список-буфер с записями из справочниа"""
    for key, value in array_of_dictionary.items():
        print("{}: {}".format(key, value))
    print('\n')


def add_note(array_of_dictionary: list):
    """Добавление новой записи. Параметры: array_of_dictionary: список-буфер с записями из справочниа"""
    print('Добавить запись:')
    new_elem: str = str(Record.from_input(0, len(array_of_dictionary)).convert_record_to_dict()) + '\n'
    array_of_dictionary.append(new_elem)


def numbers_of_lines(array_of_dictionary: list):
    """Вернуть количество записей в справочнике.
     Параметры:
               array_of_dictionary: список-буфер с записями из справочниа
     """
    return len(array_of_dictionary)


def print_info(array_of_dictionary: list):
    """Вывести все записи из справочника. Параметры: array_of_dictionary: список-буфер с записями из справочниа"""
    if len(array_of_dictionary) > 0:
        for element in array_of_dictionary:
            d_elem: dict = ast.literal_eval(str(element))
            print_dict(d_elem)
    else:
        print('Файл пуст\n')


def change_book(array_of_dictionary: list):
    """Изменение записи с когкретным id, который выберет пользователь.
    Параметры:
              array_of_dictionary: список-буфер с записями из справочниа
    """
    quantity: int = numbers_of_lines(array_of_dictionary)
    print(f'Выберете id записи, начиная c 1 и до {quantity}')
    num: int = Validation.validation_line_number(quantity)
    line: str = array_of_dictionary[num - 1]
    print(f'Cтрока для изменений:\n {line}')
    old_id: int = (ast.literal_eval(line))['ID']
    print('Вводите новые поля записи')
    array_of_dictionary[num - 1]: str = str(Record.from_input(old_id,
                                                              len(array_of_dictionary)).convert_record_to_dict()) + '\n'
    print('\n')


def comprasion(s_elem: dict, elem_from_file: dict):
    """Сравнение характеристик при поиске записи. Совпадение засчитывается даже в том случае,
     если характеристика, которую ввел пользователь, полностью содержится в характеристике записи,
      в которой идет поиск.
      Параметры:
                s_elem: словарь, представляющий запись, которую ввел пользовтаель
                elem_from_file: словарь, представляющий запись, котороя хранится в справочнике
      Возвращает:
                True: если по всем характеристикам прошла проверка
                False: если хоть по одной характеристике есть несовпадение
      """
    for key in (s_elem.keys() - {'ID'}):
        if re.search(f"{s_elem[key]}", elem_from_file[key], re.IGNORECASE) or s_elem[key].casefold() == 'none':
            continue
        else:
            return False
    return True


def search(array_of_dictionary: list):
    """Поиск записей в справочнике относительно той, которою введет пользователь.
     Параметры:
              array_of_dictionary: список-буфер с записями из справочниа
     Если подходящих записей нет, то пользователя проинформируют. Иначе же выведутся все подходящие записи.
    """
    print('Если по какой-то характеристике не нужен поиск - впишите в значения поля None')
    search_element: dict = Record.from_input(-1, len(array_of_dictionary)).convert_record_to_dict()
    print('\n')
    records: list = []
    for element in array_of_dictionary:
        d_elem: dict = ast.literal_eval(str(element))
        result: bool = comprasion(search_element, d_elem)
        if result:
            records.append(d_elem)
    if len(records) == 0:
        print('Записей не найдено\n')
    else:
        print('Найдены следующие записи:\n')
        for record in records:
            print_dict(record)
        print('\n')


if __name__ == "__main__":
    BASE_DIRECTORY: str = 'base.txt'
    with open(BASE_DIRECTORY, 'r+') as file:
        array_of_dict: list = file.readlines()
    print('\033[1m' + 'Телефонный справочник' + '\033[0m\n')
    while True:
        print('Информация для взаимодействия со справочником:')
        print(''' 1 - Вывод постранично записей из справочника\n 2 - Добавление новой записи в справочник
 3 - Редактирование записи\n 4 - Поиск записи\n 5 - Закрыть справочник и записать изменения\n''')
        print('Действие:')
        action: str = input()
        match action:
            case '1':
                print_info(array_of_dict)
            case '2':
                add_note(array_of_dict)
            case '3':
                change_book(array_of_dict)
            case '4':
                search(array_of_dict)
            case '5':
                with open(BASE_DIRECTORY, 'w+') as file:
                    for elem in array_of_dict:
                        file.write(elem)
                exit(0)
            case _:
                print("Такой команды нет. Введите существующую команду.\n")
