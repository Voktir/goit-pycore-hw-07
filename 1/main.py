from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value: str):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value: str):

        self.validation(value)

        super().__init__(value)


    def validation(self, value):
        pattern = r'\d'
        regular_value = re.findall(pattern, value)
        if list(value) == regular_value:
            if len(value) == 10:
                return value
            else:
                print("not 10 nums")
                raise ValueError ("Invalid number. Use 10 nums")
    
        else:
            print("not a number")
            raise ValueError("Invalid number format. Not a number")
        
class Birthday(Field):
    def __init__(self, value: str) -> datetime:
        try:
            date_time = datetime.strptime(value, "%d.%m.%Y")
        except:
            print("Invalid date format. Use DD.MM.YYYY")
            self.value = None
            return self.value       
        self.value = date_time.date()
        print(self.value)

        super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        # print(self.name)
        self.phones: list[Phone] = []
        self.birthday: Birthday = None

    def add_phone(self, p_number: str):
        phone = self.find_phone(p_number)
        if phone:
            print( "Phone exists")
            return
        valid_phone = Phone(p_number)
        self.phones.append(valid_phone)
        # print(self.phones)
    
    def remove_phone(self, rem_ph_number):
        self.phones = [p for p in self.phones if p.value != rem_ph_number]
    
    def edit_phone(self, find_num: str, replace_num: str):
        phone = self.find_phone(find_num)
        if not phone:
            print( "Phone not found")
            return        
        phone.value = Phone(replace_num).value
    
    def find_phone(self, find_num: str) -> Phone:
        for p in self.phones:
            if find_num == p.value:
                return p
    
    def add_birthday(self, b_date: str):
        self.birthday = Birthday(b_date)

    def __str__(self):
        try:
            b_day = self.birthday.value
        except:
            b_day = None
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {b_day}"

class AddressBook(UserDict):

    def add_record(self, record: Record):
        # print(record.name.value)
        self.data[record.name.value] = record
        # print("..............")

    def find(self, name) -> Record:
        return self.data.get(name)

    def delete(self, del_record: str):
        d = self.find(del_record)
        if not d:
            print( "Record not found")
            return
        self.data.pop(del_record)

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("01.01,2001")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
# jane_record.add_birthday("02.02.2002")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(name)
    print(record)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555
# john.remove_phone("5555555555")
# print(john)

# # Видалення запису Jane
# book.delete("Jane")

# for name, record in book.data.items():
#     print(name)
#     print(record)