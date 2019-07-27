# Import necessary modules
import sqlite3

###########################
## CREATING THE DATABASE ##
###########################

con = sqlite3.connect('terminal_mgt_system.db') 
c = con.cursor()

# Creating users table
c.execute(
'''
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
name TEXT UNIQUE NOT NULL,
contact_information TEXT NOT NULL,
fees INTEGER NOT NULL DEFAULT 0
);
'''
)

# Creating librarian table
c.execute(
'''
CREATE TABLE IF NOT EXISTS librarian(
librarian_id INTEGER PRIMARY KEY AUTOINCREMENT ,
username TEXT UNIQUE NOT NULL,
password TEXT NOT NULL,
name TEXT NOT NULL,
contact_information TEXT NOT NULL
);
'''
)

# Creating books table
c.execute(
'''
CREATE TABLE IF NOT EXISTS books(
book_id INTEGER PRIMARY KEY AUTOINCREMENT ,
author TEXT NOT NULL,
name TEXT UNIQUE NOT NULL,
description TEXT NOT NULL,
rented BOOLEAN default 0,
rented_at DATE default NULL,
rented_by INTEGER default NULL
);
'''
)
try:
    # Initializing a user
    con.execute(
        '''
        INSERT INTO users (username, password, name, contact_information) 
        VALUES ("user1",1234,"user 1","user1@gmail.com")
        '''
    )
    con.execute(
        '''
        INSERT INTO users (username, password, name, contact_information) 
        VALUES ("user2",1234,"User 2","user2@gmail.com")
        '''
    )
    con.execute(
        '''
        INSERT INTO users (username, password, name, contact_information) 
        VALUES ("user3",1234,"User 3","user3@gmail.com")
        '''
    )
    con.execute(
        '''
        INSERT INTO users (username, password, name, contact_information) 
        VALUES ("user4",1234,"User 4","user4@gmail.com")
        '''
    )
    con.execute(
        '''
        INSERT INTO users (username, password, name, contact_information) 
        VALUES ("user5",1234,"User 5","user5@gmail.com")
        '''
    )                
except:
    pass

try:
    # Initializing a librarian
    con.execute(
        '''
        INSERT INTO librarian (username,password,name,contact_information) 
        VALUES ("nrj001","natha","Librarian","library@123.com")
        '''
    )
except:
    pass

try:
    # Initializing books
    con.execute(
        '''
        INSERT INTO books (author,name,description,rented,rented_at,rented_by) 
        VALUES ("JK Rowling","Harry Potter","Sorcerers Stone",1,"2019-08-01","dillkillbill")
        '''
    )
    con.execute(
        '''
        INSERT INTO books (author,name,description,rented,rented_at,rented_by) 
        VALUES ("JK Rowling","Harry Potter 2","Chamber of Secrets",0,"2019-08-01",NULL,NULL)
        '''
    )
    con.execute(
        '''
        INSERT INTO books (author,name,description,rented,rented_at,rented_by) 
        VALUES ("JK Rowling","Harry Potter 3","Prisoner of Azkaban",0,"2019-08-01",NULL,NULL)
        '''
    )

    con.execute(
        '''
        INSERT INTO books (author,name,description,rented,rented_at,rented_by) 
        VALUES ("JK Rowling","Harry Potter 4","Goblet of Fire",1,"2019-08-01","user5")
        '''
    )
    con.execute(
        '''
        INSERT INTO books (author,name,description,rented,rented_at,rented_by) 
        VALUES ("JK Rowling","Harry Potter 5","The Order of the Phoenix",1,"2019-08-01",NULL,NULL)
        '''
    )

    con.execute(
        '''
        INSERT INTO books (author,name,description,rented,rented_at,rented_by) 
        VALUES ("JK Rowling","Harry Potter 6","The Half Blood Prince",0,"2019-08-01",NULL,NULL)
        '''
    )
    con.execute(
        '''
        INSERT INTO books (author,name,description,rented,rented_at,rented_by) 
        VALUES ("JK Rowling","Harry Potter 7","The Deathly Hallows",1,"2019-08-01","user3")
        '''
    )

    con.execute(
        '''
        INSERT INTO books (author,name,description,rented,rented_at,rented_by) 
        VALUES ("George RR Martin","Game of Thrones","A Song of Ice and Fire",1,"2019-08-01","user2")
        '''
    )    
except:
    pass
con.commit()
con.close()