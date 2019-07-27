# Import necessary modules
import sqlite3
import pandas as pd
from pandas import DataFrame
from datetime import datetime as dt

###########
## MENUS ##
###########

main_menu = '''
##########################################################


    What would you like to do today?
        1 --- Login as Librarian
        2 --- Login as User
        3 --- Register as a User/Librarian
        Please type any key and press enter to quit


##########################################################

>>>  '''

librarian_menu = '''
#########################################################


    What would you like to do today?
        1 --- Check Account Details
        2 --- Update your User Info
        3 --- Delete your Account
        4 --- Add Books to the Database
        5 --- Update Book Details in the Database
        6 --- Delete a Book from the Database
        7 --- See All Books and their Status
        8 --- Who Owes Me Money?
        9 --- Rented Books?
        Please type any key and press enter to log out


#########################################################

>>>  '''

user_menu = '''
##########################################################


    What would you like to do today?
        1 --- Check Account Details
        2 --- Update your User Info
        3 --- Delete your Account
        4 --- See Available Books
        5 --- See All Books and their Status
        6 --- See All Books you've rented
        7 --- Rent a Book
        8 --- Return a Book
        9 --- Check my fees
        Please type any key and press enter to log out


#########################################################

>>>  '''

month_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


############################
##### HELPER FUNCTIONS #####
############################

# Query the books table and return a list of all the books
def generate_book_list():
    con = sqlite3.connect('terminal_mgt_system.db')
    query = f'''
    SELECT * FROM books
    '''
    book_list = DataFrame(pd.read_sql(query,con))
    if book_list.empty:
        print("There are no books at the library")
        return DataFrame()

    print("Here's a table of all the books we have and their current status:")
    print(book_list)
    print("\n")
    return book_list

# Query the books table and return a list of available books
def generate_available_book_list():
    con = sqlite3.connect('terminal_mgt_system.db')
    query = f'''
    SELECT * FROM books
    WHERE rented == 0
    '''
    book_list = DataFrame(pd.read_sql(query,con))
    if book_list.empty:
        print("There are no books available right now. Please try again later.")
        return DataFrame()
    print("Here's a table of all available books:")
    print(book_list[['book_id','name','author','description']])
    print("\n")
    return book_list

# Query the books table and return a list of people who owe fees to the librarian    
def people_who_owe_money():
    query = '''
    SELECT user_id, username, name, contact_information,fees
    FROM users
    WHERE fees > 0
    '''
    con = sqlite3.connect('terminal_mgt_system.db')
    data = pd.read_sql(query,con)
    if data.empty:
        print("No one owes the library money.")
    else:    
        print("Here's a list of people who owe the library money:")
        print(data)
        print("\n")
    

# Query books table and return a list of people who are overdue
def rented_books():
    query = f'''
    SELECT name,rented,rented_at,rented_by
    FROM books
    -- JOIN users ON books.rented_by = users.username
    WHERE books.rented = 1
    '''
    con = sqlite3.connect("terminal_mgt_system.db")
    data = pd.read_sql(query,con)

    print("natha")

    if data.empty:
        print("No one is overdue...YET!")
    else:
        print("Here's a list of people who are overdue: ")
        print(data)
        print("\n")


def get_fine(ask):
    query = f'''
    SELECT rented_at FROM books WHERE book_id = {ask}
    '''
    con = sqlite3.connect('terminal_mgt_system.db')
    cur = con.cursor()
    cur.execute(query)
    rent_date = cur.fetchall()
    rented_month = rent_date[0][0][5] + rent_date[0][0][6]
    rented_day = rent_date[0][0][8] + rent_date[0][0][9]
    r_month = int(rented_month)
    r_day = int(rented_day)
    date = dt.today()
    cur_date = str(date)
    cur_month = cur_date[5] + cur_date[6]
    cur_day = cur_date[8] + cur_date[9]
    c_month = int(cur_month)
    c_day = int(cur_day)
    if(c_month == r_month) :
        days_rented = c_day - r_day
    else :
        days_rented = c_day + (month_days[r_month-1] - r_day)
    fees = 0
    if(days_rented > 3) :
        fees = (days_rented-3) *5
    return days_rented, fees


###########################
### OBJECTS FOR THE APP ###
###########################

# The base class for the librarian and user
class main_class:
    def __init__(self,username,password,name,contact_information):
        self.username = username
        self.password = password
        self.name = name
        self.contact_information = contact_information
        self.loggedIn = False
    
    # Check account details
    def check_details(self):
        print("Here are your account details")
        print(f'''
Username: {self.username}
Password: {self.password}
Name: {self.name}
Contact Information: {self.contact_information}
''')

    # Delete my account
    def delete_self(self):
        table = "users" if self.__class__.__name__ == "user_class" else "librarian"
        response = input("Are you sure you want to delete your account? Please answer Yes or No\n>>>  ")
        if response.strip().lower() == "yes":  
            con = sqlite3.connect('terminal_mgt_system.db')
            query = f'''
                DELETE 
                FROM {table}
                WHERE username = "{self.username}";
                '''
            con.execute(query)
            con.commit()
            con.close()

    # Update personal information
    def update_info(self):
        table = "users" if self.__class__.__name__ == "user_class" else "librarian"
        response = input('''
What field would you like to up
date? You cannot update your username.

    1 --- Name
    2 --- Contact Information
    3 --- Password

>>>  ''')
        if response.strip() not in ["1","2","3"]:
            print("Enter a valid option")
        else:
            if response == "1":
                name = input("Enter your new name now.\n>>>  ")
                print(f"Here's your new name: {name}")
                print("Updating now...")
                self.name = name
                query = f'''
                UPDATE {table}
                SET name = "{name}"
                WHERE username = "{self.username}";
                '''
            elif response == "2":
                contact_information = input("Enter your new email address now.\n>>>  ")
                print(f"Here's your new contact_info: {contact_information}")
                print("Updating now...")
                self.contact_information = contact_information
                query = f'''
                UPDATE {table}
                SET contact_information = "{contact_information}"
                WHERE username = "{self.username}";
                '''
            elif response == "3":
                password = input("Enter your new password now.\n>>>  ")
                print(f"Here's your new password: {password}")
                print("Updating now...")
                self.password = password
                query = f'''
                UPDATE {table}
                SET password = "{password}"
                WHERE username = "{self.username}";
                '''
            
            con = sqlite3.connect('terminal_mgt_system.db')
            con.execute(query)
            con.commit()
            con.close()
            print("Updated your info!")

          
# The librarian class               
class librarian_class(main_class):
    def __init__(self,username, password, name, contact_information):
        main_class.__init__(self,username,password,name,contact_information)
    
    # Librarian can add books to the database using this method
    def add_books(self):
        print("Welcome to add a book feature! Please enter the information as requested...")
        book_name = input("What's the name of the book?\n>>>")
        while book_name == "":
            book_name = input("What's the name of the book?\n>>>")
        book_author = input("What's the author's name?\n>>>")
        while book_author == "":
            book_author = input("What's the name of the book?\n>>>")
        book_description = input("Please give a small description of the book.\n>>>  ")
        while book_description == "":
            book_description = input("What's the name of the book?\n>>>")        
        print(f'''
Here's the information we're updating to the system. You can always edit or delete the book from the options menu:
Book Name: {book_name}
Author: {book_author}
Description: {book_description}
        ''')
        input("Press enter to proceed.")
        query = '''
        INSERT INTO books (author,name,description) 
        VALUES (?,?,?)
        '''
        print("Updating the database now...")
        con = sqlite3.connect('terminal_mgt_system.db')
        con.execute(query,(book_name,book_author,book_description))
        con.commit()
        con.close()
        print("Added the book to the database!")        
        
    # Librarian can update book details using this method
    def update_book_details(self):
        book_list = generate_book_list()
        try:
            ask = int(input("What Book ID would you like to update?\n>>>  "))
            if ask not in book_list['book_id'].values:
                print("Book ID not in database.")
                self.update_book_details()
            else:
                response = input('''
What information about the book would you like to update? Please enter 1, 2, or 3
    1 --- Book Name
    2 --- Book Author
    3 --- Book Description
>>>  ''')
                if response.strip() not in ["1","2","3"]:
                    print("Enter a valid option")
                    self.update_info()
                else:
                    if response == "1":
                        name = input("Enter the new name now.\n>>>  ")
                        print(f"Here's your new book name: {name}")
                        print("Updating now...")
                        query = f'''
                        UPDATE books
                        SET name = "{name}"
                        WHERE book_id = "{ask}";
                        '''
                    elif response == "2":
                        author = input("Enter the new author.\n>>>  ")
                        print(f"Here's the new author: {author}")
                        print("Updating now...")
                        query = f'''
                        UPDATE books
                        SET author = "{author}"
                        WHERE book_id = "{ask}";
                        '''
                    elif response == "3":
                        description = input("Enter the new description.\n>>>  ")
                        print(f"Here's your new password: {password}")
                        print("Updating now...")
                        query = f'''
                        UPDATE books
                        SET description = "{description}"
                        WHERE book_id = "{ask}";
                        '''

                    con = sqlite3.connect('terminal_mgt_system.db')
                    con.execute(query)
                    con.commit()
                    con.close()
                    print("Updated the book successfully")
                    generate_book_list()
        except:
            print("Please enter a valid ID")
        
    # The librarian can delete books from the database using this method
    def delete_books(self):
        book_list = generate_book_list()
        ask = int(input("What book ID would you like to delete?\n>>>  "))
        try:
        
            if ask not in book_list['book_id'].values :
                print("Book ID not in database.")

            else:
                query = f'''
                DELETE
                FROM books
                WHERE book_id = {ask}
                '''
                print("Here's the book you're trying to delete:")
                print(book_list[book_list['book_id']==ask])
                response = input("Proceed? Yes or No?\n>>>  ")
                if response.strip().lower() == "yes":
                    print("Deleting the book now...")
                    con = sqlite3.connect('terminal_mgt_system.db')
                    con.execute(query)
                    con.commit()
                    con.close()                
                    print("The book has been deleted.")
                else:
                    print("Not deleting book.")
        except:
            print("Please enter a valid book ID")
        

# Creating a user object    
class user_class(main_class):
    def __init__(self,username,password,name,contact_information,fees):
        main_class.__init__(self,username,password,name,contact_information)
        self.fees = fees

    # Users can rent books using this method        
    def rent_book(self):
        available = generate_available_book_list()
        if available.empty:
            print("Going back to the menu")
            return None
        try:
            ask = int(input("What Book ID would you like to rent?\n>>>"))
            if ask not in available['book_id'].values:
                print("Book ID not in list")
            else: 
                book = available[available['book_id'] == ask].copy()
                print(book)
                print("\n")
                ask2 = input("Do you want to rent the book above? Yes or No?\n>>>  ")
                if ask2.strip().lower() == "yes":
                    name = book['name'].values[0]
                    date = dt.now().strftime("%Y-%m-%d")
                    rented = 1
                    rented_by = self.username
                    book_id = ask
                    con = sqlite3.connect("terminal_mgt_system.db")
                    con.execute(
                    '''
                    UPDATE books
                    SET rented = ?,
                    rented_at = ?,
                    rented_by = ?
                    WHERE book_id = ?
                    ''', (rented,date,rented_by,book_id)
                    )
                    con.commit()
                    con.close()
                    print(f"You successfully rented {name}! Enjoy!")
            
        except:
            print("Enter a valid book ID")

    # See all books the user has rented
    def see_rented_books(self):
        query = f'''
        SELECT * 
        FROM books
        WHERE rented = 1
        AND rented_by = "{self.username}"
        '''
        con = sqlite3.connect('terminal_mgt_system.db')
        rented = pd.read_sql(query,con)
        con.close()
        if rented.empty:
            print("You haven't rented any books")
            return None
        print("Here's a list of all the books you've rented:")
        print(rented)
        return rented

    # # Calculate the fees for a rented book
    # def calculate_fine():
    #     print("ntahdad")
    #     query = f'''
    #     SELECT rented_at, rented by FROM books
    #     JOIN users ON books.rented_by = users.username
    #     '''
    #     con = sqlite3.connect("terminal_mgt_system.db")
    #     data = pd.read_sql(query,con)

    #     print("natha")
    #     print(query)
    #     f_date = rented_at
    #     l_date = dt.now()
    #     delta = l_date - f_date

    #     # fees = (n/2)*(2*20 + (n-1)*5)

    #     print(delta.days)

    #     return delta.days

    # Users can return books using this method   


        # print(qry)
        # difference = dt.today().date() - rented_at
        # print(difference)
        # days_rented = difference.days
        # print(days_rented)


    def return_book(self):
        rented = self.see_rented_books()
        if rented.empty:
            return None
        try:
            inp = input("What book ID would you like to return?\n")
            ask = int(inp)
            if ask not in rented['book_id'].values:
                print("You've not rented this book.")
            else:
                book = rented[rented['book_id'] == ask]
                days_rented, fees = get_fine(ask)
                print("Returning your book...")
                query = f'''
                UPDATE books
                SET rented = 0,
                rented_at = NULL,
                rented_by = NULL
                WHERE book_id = {ask}
                '''
                con = sqlite3.connect('terminal_mgt_system.db')
                con.execute(query)
                con.commit()
                con.close()
                print("Returning done.")

                if fees == 0:
                    print("Good job on returning the book on time!")
                else:
                    print("Our systems indicate that its been %i days since you rented the book. Hence you will incur a charge of Rs %i" %(days_rented, fees))
                    print("The librarian will be notified of these fees")
                    query = '''
                    UPDATE users
                    SET fees = ?
                    WHERE username = ?
                    '''
                    con = sqlite3.connect('terminal_mgt_system.db')
                    con.execute(query, (self.fees, self.username))
                    con.commit()
                    con.close()
        
        except:
            print("Please enter a valid input.")
 
    def check_fees(self):
            fees = get_fine()
            if self.fees == 0:
                print("You don't owe anything")
            else:
                print(f"You owe the library {self.fees}")
            return self.fees  

############################
##### MAIN APP SYSTEMS #####
############################
        
# Login system
def login(table):
    logged_in = False
    while not logged_in:
        con = sqlite3.connect('terminal_mgt_system.db')
        users = pd.read_sql(f"SELECT * FROM {table}",con)
        con.close()
        username = input("What's your username? Type q to go back to main menu.\n>>>  ")
        if username == "q":
            return None
        if username in users['username'].values:
            for i in range(1,4):
                password = input(f"What's your password? You have {4-i} tries...\n>>>  ")
                if password == users[users['username'] == username]['password'].values[0]:
                    print("Correct password. You are logged in.") 
                    user_details = users[users['username'] == username]
                    if table == "librarian":
                        current_user = librarian_class(user_details['username'].values[0],user_details['password'].values[0],user_details['name'].values[0],user_details['contact_information'].values[0])
                    else:                        
                        current_user = user_class(user_details['username'].values[0],user_details['password'].values[0],user_details['name'].values[0],user_details['contact_information'].values[0],user_details['fees'].values[0])
                    input("Press enter to go to your homepage.")    
                    return current_user
                else:
                    if i != 3:
                        print("Enter a valid password")
                        continue
                    else:
                        print("You have exceeded the limit.")
                        input("Press enter to go back to the main menu.") 
                        return None
        else:
            print("enter a valid username")
            input("Press enter to go back to the main menu.") 
            return None


# Registration system
def register():
    registered = False
    while not registered:
        print("Hi, welcome to the registration page!")
        stay = input('''Please type q and hit enter if you want to go back to the main menu. 
If you wish to proceed with registration, please hit enter.   

>>>  ''')
        if stay == "q":
            return None
        type_of_role = input('''
Do you want to be a librarian or a user? 
Please select from the following choices:
    lib --- librarian
    user --- user
>>>  ''')
        if type_of_role not in ["lib","user"]:
            continue
        name = input("What's your name?\n>>>  ")
        contact_info = input("What's your email?\n>>>  ")
        
        if type_of_role == "lib":
            con = sqlite3.connect('terminal_mgt_system.db')
            users = pd.read_sql(f"SELECT username,password FROM librarian",con)
            con.close()
        else:
            con = sqlite3.connect('terminal_mgt_system.db')
            users = pd.read_sql(f"SELECT username,password FROM users",con)
            con.close()
            
        username = input("What username would you like?\n>>>  ")
        if username in users['username'].values:
            print("Your username already exists.")
            continue
        password = input("What password would you like?\n>>>  ")
        print(f'''
Here are your details...
    Name: {name}
    Contact: {contact_info}
    Username: {username}
    Password: {password}
        ''')
        registered = True    
        response = input("Are these details fine? Please enter Yes or No.\n>>>  ")
        if response.strip().lower() == "yes":
            print(f"Congrats {name}! We're adding you to our system.")
            con = sqlite3.connect('terminal_mgt_system.db')
            if type_of_role == 'lib':
                con.execute(
                "INSERT INTO librarian (username, password, name, contact_information) VALUES (?,?,?,?)", (username,password,name,contact_info)
                )
                con.commit()
                con.close()
            else:
                con.execute(
                "INSERT INTO users (username, password, name, contact_information) VALUES (?,?,?,?)", (username,password,name,contact_info)
                )
                con.commit()
                con.close()   
            print("You were successfully added!")
            registered = True
        elif response.strip().lower() == "no":
            print("Taking you back to the registration page.")
            input("Press enter to go back to the registration page.")
            continue
        else:
            print("Please enter yes or no.")
            input("Press enter to go back to the start of the registration page.")
            continue



#################
##### VIEWS #####
#################

# Librarian View
def library_app(librarian):
    while librarian.loggedIn:
        try:
            response = int(input(librarian_menu))
            if response == 1:
                librarian.check_details()
            elif response == 2:
                librarian.update_info()
            elif response == 3:
                librarian.delete_self()
                print("Deleting your user and logging you out...")
                librarian.loggedIn = False
            elif response == 4:
                librarian.add_books()
            elif response == 5:
                librarian.update_book_details()
            elif response == 6:
                librarian.delete_books()
            elif response == 7:
                generate_book_list()
            elif response == 8:
                rented_books()
            else:
                librarian.loggedIn = False
            input("Please press enter to go back to your menu.")    
        except:
            librarian.loggedIn = False

# User View
def user_app(user):
    while user.loggedIn:
        try:
            response = int(input(user_menu))
            if response == 1:
                user.check_details()            
            elif response == 2:
                user.update_info()
            elif response == 3:
                user.delete_self()
                print("Deleting your user and logging you out...")
                user.loggedIn = False
            elif response == 4:
                generate_available_book_list()
            elif response == 5:
                generate_book_list()
            elif response == 6:
                user.see_rented_books()  
            elif response == 7:
                user.rent_book()
            elif response == 8:
                user.return_book()
            elif response == 9:
                user.check_fees()
            # else:
            #     user.loggedIn = False
            input("Please press enter to go back to your menu.")      
        except:
            user.loggedIn = False




####################
##### MAIN APP #####
####################

# Main app
def run_app():
    option = "run"
    while option == "run":
        try:
            question = int(input(main_menu))
            if question == 1:
                librarian = login('librarian')
                if librarian is None:
                    continue
                librarian.loggedIn = True
                library_app(librarian)
                
            elif question == 2:
                user = login('users')
                if user is None:
                    continue
                user.loggedIn = True
                user_app(user)
                
            elif question == 3:
                register()
                
            else:
                print('''
Now exiting the program...
Goodbye!
''')
                break
            
        except:
            print('''
Now exiting the program...
Goodbye!
''')
            break
    

if __name__ == '__main__':
    run_app()