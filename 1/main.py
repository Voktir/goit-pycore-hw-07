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
        
class BirthdayError(Exception):
    # def __init__(self, message="Invalid date format. Use DD.MM.YYYY"):
    #     self.message = message
    #     super().__init__(self.message)
    pass
        
class Birthday(Field):
    def __init__(self, value: str) -> datetime:
        try:
            today = datetime.today().date()
            b_day = datetime.strptime(value, "%d.%m.%Y").date()
        except:
            self.value = None
            print("Invalid date format. Use DD.MM.YYYY")
            # raise BirthdayError
            return self.value
        
        value = b_day if today >= b_day else None
        
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
            # print(b_day)
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

    def get_upcoming_birthdays(self):    

        today = datetime.today()
        b_users = []

        for name, user in self.data.items():
            user_year = str(user.birthday.value.year)
            year_now = str(today.year)
            user_data = str(user.birthday.value)
            # print(user_data)
            last_birthday = re.sub(user_year, year_now, user_data)
            last_birthday_to_data = datetime.strptime(last_birthday, "%Y-%m-%d")
            # print((last_birthday_to_data - today).days)
            if -1 <= (last_birthday_to_data - today).days < 6:

                match last_birthday_to_data.weekday():
                    case 5:
                        last_birthday_to_data = last_birthday_to_data + timedelta(days=2)
                    case 6:
                        last_birthday_to_data = last_birthday_to_data + timedelta(days=1)
        
                b_users.append({"name": user.name.value, "congratulation_date": last_birthday_to_data.strftime("%Y.%m.%d")})
        return b_users

# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("19.05.2023")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("17.05.2023")
book.add_record(jane_record)

# Виведення всіх записів у книзі
for name, record in book.data.items():
    print(record)

upcoming_birthdays = book.get_upcoming_birthdays()
print("Список привітань з ДН:", upcoming_birthdays)

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