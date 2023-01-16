import os
import csv
import config
import random

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..', 'database')

'''
DB_Controller -> Class

This class will be used to manage the databases
it's unique argument is the database name where to 
make the connections.
'''
class DB_Controller:
    def __init__(self, name) -> None:
        self.name = name + '.csv'
        self.dir = os.path.join(BASE_DIR, self.name)
        self.has_index = False
        self.db_size = 0
        self.create_db()
    '''
    create_db() -> None
    This function creates the database if not exists
    the csv files will use a semi colon as a delimiter
    '''
    def create_db(self) -> None:
        if os.path.exists(self.dir):
            with open(self.dir, 'r') as file:
                db = csv.reader(file, delimiter=',')
                for row in db:
                    if row[0] == 'index':
                        self.has_index = True
                        break;
        else:
            try:
                with open(self.dir, 'x'):
                    pass
            except Exception as e:
                print(e)
    '''
    create_index(list) -> None
    This function takes a list with the column
    names as argument.
    do not add to the argument the 'index' column
    it will be added automatically.
    After the index is created the function will no create
    another indexes.
    '''
    def create_index(self, initialRow: list) -> None:
        try:
            initialRow.remove("index")
        except ValueError:
            pass
        if not(self.has_index):
            initialRow.insert(0, 'index')
            with open(self.dir, 'a') as file:
                db = csv.writer(file, delimiter=',')
                db.writerow(initialRow)
                file.close()
    '''
    check_size() -> None
    This function calculates
    the amount of data (it does not counts the indexes)
    '''        
    def check_size(self) -> None:
        self.db_size = 0
        with open(self.dir, 'r') as file:
            db = csv.reader(file, delimiter=',')
            temp_list = [] # This list will check the last index
            for row in db:
                temp_list.append(row[0])
            try:
                self.db_size = int(temp_list[-1]) + 1
            except:
                self.db_size = 1
            file.close()
    '''
    create_data(list) -> None
    This function add entries to the data base
    (remember to check the column size)
    '''
    def create_data(self, data: list = [])->None:
        self.check_size()
        data.insert(0, self.db_size)
        with open(self.dir, 'a') as file:
            db = csv.writer(file, delimiter=',')
            db.writerow(data)
            file.close()
    '''
    remove_by_value(str, str) -> Bool
    This function delete a row, taking as argument it's
    value and column name
    returns true if the deletion was ok.
    '''
    def remove_by_value(self, val: str, column_name: str)->bool:
        self.db_size = 0
        value_found = False
        index_y = 0
        index_x = int()
        lines = []
        with open(self.dir, 'r') as file:
            db = csv.reader(file, delimiter=',')
            for row in db:
                try:
                    index_x = row.index(column_name)
                    break;
                except ValueError:
                    if config.DEBUG:
                        print("{} is not a column".format(column_name))
                    return False
            for row in db:
                index_y += 1
                if val in row[index_x]:
                    value_found = True
                    break
            file.close()
        if index_y == -1:
            return False
        if value_found:
            with open(self.dir, 'r') as file:
                lines = file.readlines()
                file.close()
            with open(self.dir, 'w') as file:
                for number, line in enumerate(lines):
                    if number not in [index_y]:
                        file.write(line)
                file.close()
        else:
            if config.DEBUG:
                print("{0} value not found in column {1}".format(val, column_name))
            return False
        if config.DEBUG:
            print("{0} value removed from column {1}".format(val, column_name))
        return True
    '''
    is_unique() -> None
    This function will be used by the create_data() function
    to avoid the creation of users with same user or mail
    '''
    def is_unique(self)->None:
        pass
            
if __name__ == '__main__':
    if config.DEBUG:
        mydb = DB_Controller("test")
        mydb.create_index(['user', 'password'])
        mydb2 = DB_Controller("test")
        users = ['Juan', 'Alberto', 'Ignacio', 'Ramiro', 'Lucía', 'Maquiavelo']
        for user in users:
            mydb2.create_data([user, str(random.randint(20000000, 8999999999))])
            pass

    