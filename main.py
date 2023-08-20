import json
import ast


class Phonebook():
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
            input('Name: '),
            input('Lastname: '),
            input('Surname: '),
            input('Organization: '),
            input('Work_phone: '),
            input('Personal_phone: '),
        )

    def asdict(self):
        return {'Name': self.name, 'Lastname': self.lastname, 'Surname': self.surname,
                'Organization': self.organization,
                'Work_phone': self.work_phone, 'Personal_phone': self.personal_phone}


def add_note(directory: str):
    print('Добавить запись:')
    with open(directory, 'a+') as f:
        new_elem = Phonebook.from_input().asdict()
        f.write(str(new_elem) + '\n')
        f.close()


def print_info(directory: str):
    with open(directory, 'r', encoding='utf-8') as file:  # открыли файл с данными
        for elem in file:
            d_elem = ast.literal_eval(elem)
            for item, amount in d_elem.items():
                print("{}: {}".format(item, amount))
            print('\n')


def numbers_of_lines(directory: str):
    with open(directory, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
    return len(lines)


def change_book(directory: str):
    quantity = numbers_of_lines(directory)
    print(f'Выберете номер записи, начиная c 0 и до {quantity - 1}')
    while True:
        num = int(input())
        if num < 0 | num > (quantity - 1):
            print('Некорректно введен номер записи. Попробуйте еще раз.')
        else:
            break
    count = 0
    with open(directory, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        file.seek(0)
        while count != num:
            file.readline()
            count += 1
        line = file.readline()
        print('Cтрока для изменений:')
        print(line)
    print('Вводите новые поля записи')
    lines[num] = str(Phonebook.from_input().asdict()) + '\n'
    with open(directory, 'w+', encoding='utf-8') as file:
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
    search_element = Phonebook.from_input().asdict()
    with open(directory, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
    records = []
    for elem in lines:
        d_elem = elem.replace("'", "\"")
        d_elem = json.loads(d_elem)
        result = comprasion(search_element, d_elem)
        if result:
            records.append(d_elem)
    if len(records) == 0:
        return 'Записей не найдено'
    else:
        print('Найдены следующие записи:')
        for record in records:
            for item, amount in record.items():
                print("{}: {}".format(item, amount))
        print('\n')
        return 'Конец поиска'


if __name__ == "__main__":
    BASE_DIRECTORY = 'base.txt'
    print('\033[1m' + 'Телефонный справочник' + '\033[0m\n')
    while True:
        print('Информация для взаимодействия со справочником:')
        print(''' 1 - Вывод постранично записей из справочника\n 2 - Добавление новой записи в справочник
 3 - Редактирование записи\n 4 - Поиск записи\n 5 - Закрыть справочник\n''')
        print('Действие:')
        action = int(input())
        match action:
            case 1:
                print_info(BASE_DIRECTORY)
            case 2:
                add_note(BASE_DIRECTORY)
            case 3:
                change_book(BASE_DIRECTORY)
            case 4:
                search(BASE_DIRECTORY)
            case 5:
                exit(0)
            case _:
                print("Такой команды нет")
