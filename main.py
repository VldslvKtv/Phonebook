import ast


class Validation(object):
    @staticmethod
    def validate_int():
        while True:
            try:
                int_obj = int(input())
            except ValueError:
                print('Введите целое неотрицательное число.')
            else:
                return int_obj

    @staticmethod
    def validate_id(explantion: str, quantity: int, former_id: int):
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
                        and len(phone_number) == 12 and phone_number[1:].isdigit()) | (phone_number == 'None'):
                return phone_number
            else:
                print('Некорректный номер. Введите ещё раз')

    @staticmethod
    def validation_line_number(quantity_lines: int):
        while True:
            line_number: int = Validation.validate_int()
            if (line_number < 0) | (line_number > quantity_lines):
                print('Некорректно введен id записи. Попробуйте еще раз.')
            else:
                return line_number


class Record(object):
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
        return {'ID': self.id_record, 'Name': self.name, 'Lastname': self.lastname, 'Surname': self.surname,
                'Organization': self.organization,
                'Work_phone': self.work_phone, 'Personal_phone': self.personal_phone}


def print_dict(dict_for_print: dict):
    for key, value in dict_for_print.items():
        print("{}: {}".format(key, value))
    print('\n')


def add_note(directory: list):
    print('Добавить запись:')
    new_elem: str = str(Record.from_input(0, len(directory)).convert_record_to_dict()) + '\n'
    directory.append(new_elem)


def numbers_of_lines(directory: list):
    return len(directory)


def print_info(directory: list):
    if len(directory) > 0:
        for elem in directory:
            d_elem: dict = ast.literal_eval(str(elem))
            print_dict(d_elem)
    else:
        print('Файл пуст\n')


def change_book(directory: list):
    quantity = numbers_of_lines(directory)
    print(f'Выберете id записи, начиная c 1 и до {quantity}')
    num = Validation.validation_line_number(quantity)
    line = directory[num - 1]
    print(f'Cтрока для изменений:\n {line}')
    old_id = (ast.literal_eval(line))['ID']
    print('Вводите новые поля записи')
    directory[num - 1] = str(Record.from_input(old_id, len(directory)).convert_record_to_dict()) + '\n'
    print('\n')


def comprasion(s_elem: dict, elem_from_file: dict):
    for key in (s_elem.keys() - {'ID'}):
        if s_elem[key] != elem_from_file[key] and s_elem[key] != 'None':
            return False
    return True


def search(directory: list):
    print('Если по какой-то характеристике не нужен поиск - впишите в значения поля None')
    search_element: dict = Record.from_input(-1, len(directory)).convert_record_to_dict()
    print('\n')
    records: list = []
    for elem in directory:
        d_elem: dict = ast.literal_eval(str(elem))
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
    with open(BASE_DIRECTORY, 'r+') as file:
        array_of_dict: list = file.readlines()
    print('\033[1m' + 'Телефонный справочник' + '\033[0m\n')
    while True:
        print('Информация для взаимодействия со справочником:')
        print(''' 1 - Вывод постранично записей из справочника\n 2 - Добавление новой записи в справочник
 3 - Редактирование записи\n 4 - Поиск записи\n 5 - Закрыть справочник\n''')
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
