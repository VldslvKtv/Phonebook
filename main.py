import json
import ast
import pprint
import pandas


class Phonebook():
    def __init__(self, name, lastname, surname, organization, work_phone, personal_phone):
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


def add_note(directory):
    print('Добавить запись:')
    with open(directory, 'a+') as f:
        new_elem = Phonebook.from_input().asdict()
        f.write(str(new_elem) + '\n')
        f.close()


def print_info(directory):
    with open(directory, 'r', encoding='utf-8') as file:  # открыли файл с данными
        for elem in file:
            d_elem = ast.literal_eval(elem)
            for item, amount in d_elem.items():
                print("{}: {}".format(item, amount))
            print('\n')


def change_book(directory):
    print('Выберете номер запись')
    num = int(input())
    count = 0
    with open(directory, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        file.seek(0)
        while count != num:
            file.readline()
            count += 1
        line = file.readline()
        print('Cтрока для изменений')
        print(line)
    print('Вводите новые поля записи')
    lines[num] = str(Phonebook.from_input().asdict()) + '\n'
    with open(directory, 'w+', encoding='utf-8') as file:
        for elem in lines:
            file.write(elem)


def comprasion(s_elem, elem_from_file):
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


def search(directory):
    print('Если по какой-то характеристике не нужне поиск - впишите в значения поля None')
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
            print(record)
        return 'Конец поиска'


directory1 = 'base.txt'
print_info(directory1)
# change_book(directory1)
# print_info(directory1)
# add_note(directory1)

res = search(directory1)
print(res)
