import sqlite3 as sql
from datetime import datetime

'API FILE FOR DATABASE INTRACTION'

#define a class to handle it with context manager(with)
class SqlConnection:

    #give database name
    def __init__(self, database):
        self.database = database
        self.connection = None
    
    #when we open it with context manager it build new connection and cursor
    def __enter__(self):
        self.connection = sql.connect(self.database)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    #automatically when (with) body is closed it close the connection and cursor
    #and if there is no error it commit all the data into database
    #otherwise we should handle errors in else condition
    def __exit__(self, exc_type, exc_val, exc_tb):
        #exc_type: type exception, exc_val: value of the exception, exc_tb: traceback address
        if exc_type is None:
            self.connection.commit()

        else:
            if str(exc_val) == 'no such table: expenses':
                print('The table is not created in database')
                print('''If you see this error it means the database file doesn't have tables with expected format''')
                print('Please remove the data.db inside the db directory')
                print('otherwise if there is no data.db in that directory please contact me')  
                
        self.cursor.close()
        self.connection.close()

#build the databse with expenses table
#TODO we can change it later to take table name so we can have multiple table
def init():
    'initial the database'
    with SqlConnection(r'db/data.db') as c:
        c.execute('''CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY,
            amount REAL,
            category TEXT COLLATE NOCASE,
            message TEXT,
            date TEXT
        )''')

#show the database records if not given category otherwise show all records according to that category
def show(category=None, sort=False, stype='ASC'):
    'show records in database'
    with SqlConnection('db/data.db') as c:
        if category and sort == False:
            c.execute('SELECT * FROM expenses WHERE category = :category',{'category':category})
            records = c.fetchall()
            c.execute('SELECT SUM(amount) FROM expenses WHERE category = :category',{'category':category})
            total = c.fetchone()[0]

        elif sort == False and category == None:
            c.execute('SELECT * FROM expenses')
            records = c.fetchall()
            c.execute('SELECT SUM(amount) FROM expenses')
            total = c.fetchone()[0]

        elif category and sort:
            query = f'SELECT * FROM expenses WHERE category = :category ORDER BY amount {stype}'
            c.execute(query,{'category':category})
            records = c.fetchall()
            c.execute('SELECT SUM(amount) FROM expenses WHERE category = :category',{'category':category})
            total = c.fetchone()[0]

        elif category == None and sort:
            query = f'SELECT * FROM expenses ORDER BY amount {stype}'
            c.execute(query)
            records = c.fetchall()
            c.execute('SELECT SUM(amount) FROM expenses')
            total = c.fetchone()[0]

    return total, records

#add new record in database 
def add(amount:float, category:str, message:str='') -> None:
    'add new record in database'
    with SqlConnection('db/data.db') as c:
        date = datetime.now().strftime('%Y-%m-%d | %H:%M:%S')
        amount = float(amount)
        c.execute('''INSERT INTO expenses(amount, category, date, message) VALUES(
            :amount,
            :category,
            :date,
            :message
        )''',{'amount':amount,'category':category,'date':date,'message':message})

#delete record from database by id
def delete(Id:int):
    'delete record by id from database'
    with SqlConnection('db/data.db') as c:
        c.execute('DELETE FROM expenses WHERE id = :id',{'id':Id})
