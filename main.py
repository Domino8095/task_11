from datetime import datetime
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Телефон повинен містити лише 10 цифр')
    
    def __init__(self, value):
        super().__init__(value)
        self.validate(value)

    def __set__(self, instance, value):
        self.validate(value)
        super().__set__(instance, value)

class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Некоректний формат дати. Використовуйте формат YYYY-MM-DD')

    def __init__(self, value=None):
        if value:
            self.validate(value)
        super().__init__(value)

    def __set__(self, instance, value):
        self.validate(value)
        super().__set__(instance, value)

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def __str__(self):
        return f"Ім'я контакта: {self.name.value}, дата народження: {self.birthday.value if self.birthday.value else 'не задана'}, телефони: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

    def remove_phone(self, phone_number: str):
        phone = self.find_phone(phone_number)
        if phone:
            self.phones.remove(phone)
    
    def edit_phone(self, old_phone_number: str, new_phone_number: str):
        phone = self.find_phone(old_phone_number)
        if phone:
            phone.value = new_phone_number
        else:
            raise ValueError("Телефон не найден")
    
    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.now()
            current_birthday = datetime.strptime(self.birthday.value, '%Y-%m-%d').replace(year=today.year)
            if current_birthday < today:
                current_birthday = current_birthday.replace(year=today.year + 1)
            return (current_birthday - today).days

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def find(self, name: str):
        if name in self.data:
            return self.data[name]

    def display_all_records(self):
        for record in self.data.values():
            print(record)

    def __iter__(self):
        return AddressBookIterator(self)

class AddressBookIterator:
    def __init__(self, address_book):
        self._address_book = address_book
        self._keys = list(address_book.data.keys())
        self._index = 0
        self._step = 2  

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._keys):
            raise StopIteration
        else:
            current_index = self._index
            self._index += self._step
            return [self._address_book.data[key] for key in self._keys[current_index:self._index]]



book = AddressBook()

john_record = Record("John", "2000-05-15")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
book.add_record(john_record)

jane_record = Record("Jane", "1998-10-22")
jane_record.add_phone("9876543210")
book.add_record(jane_record)


book.display_all_records()


john = book.find("John")
if john:
    print(john.days_to_birthday())


book.delete("Jane")
book.display_all_records()
