import json
import ast


class Phonebook(object):
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
            check_titles('Name: '),
            check_titles('Lastname: '),
            check_titles('Surname: '),
            check_titles('Organization: '),
            check_number('Work_phone: '),
            check_number('Personal_phone: ')
        )

    def asdict(self):
        return {'Name': self.name, 'Lastname': self.lastname, 'Surname': self.surname,
                'Organization': self.organization,
                'Work_phone': self.work_phone, 'Personal_phone': self.personal_phone}


def check_titles(explantion: str):
    while True:
        print(f'{explantion}', end="")
        title: str = input()
        if len(title) < 1:
            print('Некорректный ввод. Введите ещё раз.')
        else:
            return title


def check_number(explantion: str):
    while True:
        print(f'{explantion}', end="")
        phone_number: str = input()
        if (len(phone_number) == 12 and phone_number.isdigit()) | (phone_number[0] == '+'
                    and len(phone_number) == 12 and phone_number[1:].isdigit()) | (phone_number == 'None'):
            return phone_number
        else:
            print('Некорректный номер. Введите ещё раз')


def add_note(directory: str):
    print('Добавить запись:')
    with open(directory, 'a+') as f:
        new_elem: dict = Phonebook.from_input().asdict()
        f.write(str(new_elem) + '\n')
        f.close()


def print_info(directory: str):
    with open(directory, 'r') as file:  # открыли файл с данными
        for elem in file:
            d_elem: dict = ast.literal_eval(elem)
            for item, amount in d_elem.items():
                print("{}: {}".format(item, amount))
            print('\n')


def numbers_of_lines(directory: str):
    with open(directory, 'r+') as file:
        lines: list = file.readlines()
    return len(lines)


def change_book(directory: str):
    quantity = numbers_of_lines(directory)
    print(f'Выберете номер записи, начиная c 0 и до {quantity - 1}')
    while True:
        num: int = int(input())
        if num < 0 | num > (quantity - 1):
            print('Некорректно введен номер записи. Попробуйте еще раз.')
        else:
            break
    count: int = 0
    with open(directory, 'r+') as file:
        lines: list = file.readlines()
        print(type(lines))
        file.seek(0)
        while count != num:
            file.readline()
            count += 1
        line: str = file.readline()
        print('Cтрока для изменений:')
        print(line)
    print('Вводите новые поля записи')
    lines[num] = str(Phonebook.from_input().asdict()) + '\n'
    with open(directory, 'w+') as file:
        for elem in lines:
            file.write(elem)
    print('\n')


def comprasion(s_elem: dict, elem_from_file: dict):
    if (s_elem['Name'] != 'None' and s_elem['Name'] == elem_from_file['Name']) or (s_elem['Name'] == 'None'):
        if ((s_elem['Lastname'] != 'None' and s_elem['Lastname'] == elem_from_file['Lastname']) or
                (s_elem['Lastname'] == 'None')):
            if ((s_elem['Surname'] != 'None' and s_elem['Surname'] == elem_from_file['Surname']) or
                    (s_elem['Surname'] == 'None')):
                if ((s_elem['Organization'] != 'None' and s_elem['Organization'] == elem_from_file[
                    'Organization']) or
                        (s_elem['Organization'] == 'None')):
                    if ((s_elem['Work_phone'] != 'None' and s_elem['Work_phone'] == elem_from_file['Work_phone']) or
                            (s_elem['Work_phone'] == 'None')):
                        if ((s_elem['Personal_phone'] != 'None' and s_elem['Personal_phone'] == elem_from_file[
                            'Personal_phone']) or
                                (s_elem['Personal_phone'] == 'None')):
                            return True


def search(directory: str):
    print('Если по какой-то характеристике не нужен поиск - впишите в значения поля None')
    search_element: dict = Phonebook.from_input().asdict()
    print('\n')
    with open(directory, 'r+') as file:
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
            for item, amount in record.items():
                print("{}: {}".format(item, amount))
            print('\n')
        return print('Конец \n')


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
