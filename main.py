import json
import ast


class Validation():

    @staticmethod
    def validate_titles(explantion: str):
        while True:
            print(f'{explantion}', end="")
            title: str = input()
            if len(title) < 1:
                print('Некорректный ввод. Введите ещё раз.')
            else:
                return title

    @staticmethod
    def validate_number(explantion: str):
        while True:
            print(f'{explantion}', end="")
            phone_number: str = input()
            if (len(phone_number) == 11 and phone_number.isdigit()) | (phone_number[0] == '+'
                                                                       and len(phone_number) == 12 and phone_number[
                                                                                                       1:].isdigit()) | (
                    phone_number == 'None'):
                return phone_number
            else:
                print('Некорректный номер. Введите ещё раз')

    @staticmethod
    def validation_line_number(quantity_lines):
        while True:
            line_number: int = int(input())
            if line_number < 0 | line_number > (quantity_lines - 1):
                print('Некорректно введен номер записи. Попробуйте еще раз.')
            else:
                return line_number


class Record(object):
    def __init__(self, name: str, lastname: str, surname: str, organization: str, work_phone: str, personal_phone: str):
        self.name = name
        self.lastname = lastname
        self.surname = surname
        self.organization = organization
        self.work_phone = work_phone
        self.personal_phone = personal_phone

    @classmethod
    def from_input(cls):
        return cls(
            Validation.validate_titles('Name: '),
            Validation.validate_titles('Lastname: '),
            Validation.validate_titles('Surname: '),
            Validation.validate_titles('Organization: '),
            Validation.validate_number('Work_phone: '),
            Validation.validate_number('Personal_phone: ')
        )

    def convert_record_to_dict(self):
        return {'Name': self.name, 'Lastname': self.lastname, 'Surname': self.surname,
                'Organization': self.organization,
                'Work_phone': self.work_phone, 'Personal_phone': self.personal_phone}


def print_dict(dict_for_print: dict):
    for key, value in dict_for_print.items():
        print("{}: {}".format(key, value))
    print('\n')


def add_note(directory: str):
    print('Добавить запись:')
    with open(directory, 'a+') as f:
        new_elem: dict = Record.from_input().convert_record_to_dict()
        f.write(str(new_elem) + '\n')
        f.close()


def print_info(directory: str):
    with open(directory, 'r') as file:  # открыли файл с данными
        for elem in file:
            d_elem: dict = ast.literal_eval(elem)
            print_dict(d_elem)


def numbers_of_lines(directory: str):
    with open(directory, 'r+') as file:
        lines: list = file.readlines()
    return len(lines)


def change_book(directory: str):
    quantity = numbers_of_lines(directory)
    print(f'Выберете номер записи, начиная c 0 и до {quantity - 1}')
    num = Validation.validation_line_number(quantity)
    with open(directory, 'r+') as file:
        lines: list = file.readlines()
        file.seek(0)
        count: int = 0
        while count != num:
            file.readline()
            count += 1
        line: str = file.readline()
        print('Cтрока для изменений:')
        print(line)
    print('Вводите новые поля записи')
    lines[num] = str(Record.from_input().convert_record_to_dict()) + '\n'
    with open(directory, 'w+') as file:
        for elem in lines:
            file.write(elem)
    print('\n')


def comprasion(s_elem: dict, elem_from_file: dict):
    for key in s_elem.keys():
        if s_elem[key] != elem_from_file[key] and s_elem[key] != 'None':
            return False
    return True


def search(file_name: str):
    print('Если по какой-то характеристике не нужен поиск - впишите в значения поля None')
    search_element: dict = Record.from_input().convert_record_to_dict()
    print('\n')
    with open(file_name, 'r+') as file:
        lines: list = file.readlines()
    records: list = []
    for elem in lines:
        d_elem: str = elem.replace("'", "\"")
        d_elem: dict = json.loads(d_elem)
        result: bool = comprasion(search_element, d_elem)
        if result:
            records.append(d_elem)
    if len(records) == 0:
        return print('Записей не найдено\n')
    else:
        print('Найдены следующие записи:\n')
        for record in records:
            print_dict(record)
        return print('\n')


if __name__ == "__main__":
    BASE_DIRECTORY: str = 'base.txt'
    print('\033[1m' + 'Телефонный справочник' + '\033[0m\n')
    while True:
        print('Информация для взаимодействия со справочником:')
        print(''' 1 - Вывод постранично записей из справочника\n 2 - Добавление новой записи в справочник
 3 - Редактирование записи\n 4 - Поиск записи\n 5 - Закрыть справочник\n''')
        print('Действие:')
        action: str = input()
        match action:
            case '1':
                print_info(BASE_DIRECTORY)
            case '2':
                add_note(BASE_DIRECTORY)
            case '3':
                change_book(BASE_DIRECTORY)
            case '4':
                search(BASE_DIRECTORY)
            case '5':
                exit(0)
            case _:
                print("Такой команды нет. Введите существующую команду.\n")
