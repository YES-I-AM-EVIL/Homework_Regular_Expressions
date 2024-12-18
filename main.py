from pprint import pprint
import csv
import re
from collections import defaultdict

# Чтение данных из CSV файла
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Приведение ФИО в правильный формат
def format_name(contact):
    full_name = ' '.join(contact[:3]).strip()
    parts = full_name.split()
    if len(parts) == 2:
        lastname, firstname = parts
        surname = ''
    elif len(parts) == 3:
        lastname, firstname, surname = parts
    else:
        lastname, firstname, surname = '', '', ''
    return [lastname, firstname, surname] + contact[3:]

contacts_list = [format_name(contact) for contact in contacts_list]

# Приведение телефонов в правильный формат
def format_phone(phone):
    phone = phone.strip()
    phone = re.sub(r'(\+7|8)?\s*\(?(\d{3})\)?\s*\-?(\d{3})\-?(\d{2})\-?(\d{2})', r'+7(\2)\3-\4-\5', phone)
    if 'доб.' in phone:
        phone = re.sub(r'\s*доб\.\s*(\d+)', r' доб.\1', phone)
    return phone

for contact in contacts_list:
    contact[5] = format_phone(contact[5])

# Объединение дублирующихся записей
def merge_contacts(contacts_list):
    merged_contacts = defaultdict(list)
    for contact in contacts_list:
        key = tuple(contact[:2])
        merged_contacts[key].append(contact)

    result = []
    for key, contacts in merged_contacts.items():
        merged_contact = contacts[0]
        for contact in contacts[1:]:
            for i in range(3, 7):
                if not merged_contact[i]:
                    merged_contact[i] = contact[i]
        result.append(merged_contact)
    return result

contacts_list = merge_contacts(contacts_list)

# Сохранение данных в новый CSV файл
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)