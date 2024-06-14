from abc import ABC, abstractmethod

from datetime import datetime as dt, timedelta
from collections import UserList
import pickle
from info import *
import os

class ABCAddressBook(ABC, UserList):
    @abstractmethod
    def __str__(self):
        pass
    
    @abstractmethod
    def __next__(self):
        pass
    
    @abstractmethod
    def __iter__(self):
        pass
    
    @abstractmethod
    def add (self, record):
        pass
    
    @abstractmethod
    def save (self, file_name):
        pass
    
    @abstractmethod
    def Load (self, file_name):
        pass
    
    @abstractmethod
    def search(self, pattern, category):
        pass
    
    @abstractmethod
    def edit (self, contact_name, parameter, new_laue):
        pass

    @abstractmethod
    def remove (self, pattern):
        pass

    @abstractmethod
    def congratulate (self):
        pass



class AddressBook(UserList):
    def __init__(self):
        self.data = []
        self.counter = -1

    def __str__(self):
        result = []
        for account in self.data:
            
            birth = account['birthday'].strftime("%d/%m/%Y") if account['birthday'] else ''
            phone = ','.join(account['phones']) if account['phones'] else ''
            
            result.append(
                "_" * 50 + "\n" + 
                f"Name: {account['name']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+
                "_" * 50 + '\n'
                )
        
        return '\n'.join(result)

    def __next__(self):
        phones = []
        self.counter += 1
        
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        
        account = self.data[self.counter]
        birth = account['birthday'].strftime("%d/%m/%Y") if account['birthday'] else ''
        phone = ','.join(account['phones']) if account['phones'] else ''
            
        result = (
                "_" * 50 + "\n" + 
                f"Name: {account['name']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n"+
                "_" * 50 + '\n'
                )
        
        return result

    def __iter__(self):
        return self

    def __setitem__(self, index, record):
        self.data[index] = {'name': record.name,
                            'phones': record.phones,
                            'birthday': record.birthday}

    def __getitem__(self, index):
        return self.data[index]
    
    def add(self, record):
        account = {'name': record.name,
                   'phones': record.phones,
                   'birthday': record.birthday,
                   'email': record.email,
                   'status': record.status,
                   'note': record.note}
        
        self.data.append(account)
        self.log(f"Contact {record.name} has been added.")

    def save(self, file_name):
        with open(file_name + '.bin', 'wb') as file:
            pickle.dump(self.data, file)
        self.log("Addressbook has been saved!")

        
    def load(self, file_name):
        # emptyness = os.stat(file_name + '.bin')
        # if emptyness.st_size != 0:
        #     with open(file_name + '.bin', 'rb') as file:
        #         self.data = pickle.load(file)
        #     self.log("Addressbook has been loaded!")
        # else:
        #     self.log('Addressbook has been created!')
        # return self.data
        
        if os.path.getsize(file_name + '.bin') > 0:
            with open(file_name + '.bin', 'rb') as file:
                self.data = pickle.load(file)
            self.log("Addressbook has been loaded!")
        else:
            self.log('Addressbook is empty!')
        return self.data

    def search(self, pattern, category):
        result = []
        category_new = category.strip().lower().replace(' ', '')
        pattern_new = pattern.strip().lower().replace(' ', '')

        for account in self.data:
            if category_new == 'phones':

                for phone in account['phones']:

                    if phone.lower().startswith(pattern_new):
                        result.append(account)
            elif account[category_new].lower().replace(' ', '') == pattern_new:
                result.append(account)
        if not result:
            print('There is no such contact in address book!')
        return result

    def edit(self, contact_name, parameter, new_value):
        # names = []
        names = [account['name'] for account in self.data]
        try:
            for account in self.data:
                # names.append(account['name'])
                if account['name'] == contact_name:
                    if parameter == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parameter == 'email':
                        new_value = Email(new_value).value
                    elif parameter == 'status':
                        new_value = Status(new_value).value
                    elif parameter == 'phones':
                        # new_contact = new_value.split(' ')
                        # new_value = []
                        # for number in new_contact:
                        #      new_value.append(Phone(number).value)
                        new_value = [Phone(phone).value for phone in new_value.split()]
                    
                    # if parameter in account.keys():
                    if parameter in account:
                        account[parameter] = new_value
                    else:
                        raise ValueError("Incorrect parameter!")
        
                    self.log(f"Contact {contact_name} has been edited!")
                    return True
        
            if contact_name not in names:
                raise NameError("There is no such contact in address book!")
            return False
        except ValueError:
            print('Incorrect parameter! Please provide correct parameter')
        except NameError:
            print('There is no such contact in address book!')
        # else:
        #     self.log(f"Contact {contact_name} has been edited!")
        #     return True
        # return False

    def remove(self, pattern):
        flag = False
        for account in self.data:
            if account['name'] == pattern:
                self.data.remove(account)
                self.log(f"Contact {account['name']} has been removed!")
                flag = True
            if pattern in account['phones']:
                        account['phones'].remove(pattern)
                        self.log.log(f"Phone number of {account['name']} has been removed!")
                        
        return flag    
    
    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {day: [] for day in WEEKDAYS[:5]}
        for account in self.data:
            if account['birthday']:
                new_birthday = account['birthday'].replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday.date() < self.__get_current_week()[1]:
                    # if birthday_weekday < 5:
                    #     congratulate[WEEKDAYS[birthday_weekday]].append(account['name'])
                    # else:
                    #     congratulate['Monday'].append(account['name'])
                    day = WEEKDAYS[birthday_weekday if birthday_weekday < 5 else 0]
                    congratulate[day].append(account['name'])
                    
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return '_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50   
    

    def log(self, action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')

    def __get_current_week(self):
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]


# class Record:
#     def __init__(self, name, phones=None, birthday=None, email=None, status=None, note=None):
#         self.name = name
#         self.phones = phones if phones else []
#         self.birthday = birthday
#         self.email = email
#         self.status = status
#         self.note = note   

