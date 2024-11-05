'''
Author: Jonathan Romao
Date Created: 09-18-2023
Date Modified: 11-10-2023

Description: This a database that stores student information (student #, name, year, major, contact info), 
and then allows you to search and filter through the students by any of their info. 
It would also sort the students by a parameter that the user specifies. The user will also be able to add and delete students if they please. 
There will be a 4th option, sort of to the side where the user can display the database for all the information (pie charts, bar graphs). 
'''

import mysql.connector
import random, os, time
import matplotlib.pyplot as plt
from colorama import Fore

# ------------------------------------------------------------------
#                        F U N C T I O N S
# ------------------------------------------------------------------

# a function to implement tabs without causing any problems 
def tab(l, n):
    temp = ""
    spaces = n*8
    for i in l:
        temp += i + " "*(spaces - len(i))
    return temp

# function to generate each of the students attributes indvidually and all together
def generate_f_name():
    return FIRST_NAMES[random.randint(0, len(FIRST_NAMES)-1)]

def generate_l_name():
    return LAST_NAMES[random.randint(0, len(LAST_NAMES)-1)]

def generate_year():
    return str(random.randint(1,4))

def generate_major():
    return MAJORS[random.randint(0, len(MAJORS)-1)]

def generate_id():
    temp = random.randint(10**(STUDENT_ID_LEN-1), 10**STUDENT_ID_LEN-1)
    while temp in ids:
        temp = random.randint(10**(STUDENT_ID_LEN-1), 10**STUDENT_ID_LEN-1)
    return str(temp)
    
def generate_all_info(f_name=None, l_name=None, year=None, major=None, id=None):
    f_name = generate_f_name() if f_name == None else f_name
    l_name = generate_l_name() if l_name == None else l_name
    year = generate_year() if year == None else year
    major = generate_major() if major == None else major
    id = generate_id() if id == None else id
    email = f_name[0] + l_name[:3] + id[:3] + "@uni.ca"
    
    return f_name, l_name, year, major, id, email

# function to delay the timing of the programs 
def delay(timing = 1):
    time.sleep(timing)

# a function to update the ids list, which is used for the creation of the ids
def update_ids_list():
    global ids
    mycursor.execute("SELECT id FROM students")
    ids = [x[0] for x in mycursor]   

# function to generate n students
def generate_students(n):
    for i in range(n):
        update_ids_list()
        mycursor.execute("INSERT INTO students(f_name, l_name, study_year, major, id, email) VALUES(%s,%s,%s,%s,%s,%s)",
                        generate_all_info())

# function that contains the add student section of the code
def add_students():
    print("\n1. Specify the students attributes\n2. Generate random students")
    ans = input("\n(1 or 2) --> ")

    # specified
    if ans == "1":
        # input for the first name
        ans = input("\nPlease specify the students first name (enter -1 if unspecified) --> ")
        input_f_name = ans if ans != "-1"   else None
                
        # input for the last name
        ans = input("\nPlease specify the students last name (enter -1 if unspecified) --> ")
        input_l_name = ans if ans != "-1"   else None
                
        # input for the year
        while type(ans) != type(1) and ans != "-1":
            ans = input("\nPlease specify the students year (enter -1 if unspecified) --> ")
            try:
                ans = int(ans)
            except ValueError:
                print("\nPlease enter a number"); delay()
        input_year = str(ans) if ans != "-1"   else None
        
        # input for the major
        while not(ans in MAJORS) and ans != "-1":
            ans = input("\nPlease specify the students major (enter -1 if unspecified) --> ")
            if not(ans in MAJORS):
                print("\nPlease enter a major "); delay()
        input_major = ans if ans != "-1"   else None

        # adding the data to the database
        mycursor.execute("INSERT INTO students(f_name, l_name, study_year, major, id, email) VALUES(%s,%s,%s,%s,%s,%s)",
                        generate_all_info(f_name=input_f_name, l_name=input_l_name, year=input_year, major=input_major))

        update_ids_list()

    # random
    if ans == "2":
        n = ""
        while type(n) != int:
            n = input("\nPlease enter how many students you would like to generate --> ")
            try:
                n = int(n)
            except TypeError:
                print("\nPlease enter a number")
        generate_students(n)
      
# function that contains the delete student section of the code  
def delete_student():
    # input of id
    ans = input("\nPlease enter the students id number that you want to delete --> ")
    while (not ans.isdigit()) and (len(ans) != STUDENT_ID_LEN) and (not (ans in ids)):
        print(f"\nPlease enter a valid {STUDENT_ID_LEN} digit number")
        ans = input("\nPlease enter the students id number that you want to delete --> ")

    # getting the students full name
    mycursor.execute("SELECT f_name, l_name FROM students WHERE id = " + ans)
    for x in mycursor:
        full_name = x[0] + " " + x[1]

    # removing the student from the data
    mycursor.execute("DELETE FROM students WHERE id = " + ans)

    update_ids_list()
    print(f"\nYou have removed {full_name}"); delay()
      
# function that contains the graph students section of the code
def graph_students():
    # creating the data lists for the pie charts
    mycursor.execute("SELECT major FROM students")
    major_list = [x[0] for x in mycursor]
    major_pop = [major_list.count(v) for v in MAJORS]

    mycursor.execute("SELECT study_year FROM students")
    year_list = [x[0] for x in mycursor]
    year_pop = [year_list.count(v) for v in ["1","2","3","4"]]

    # creating the figure that holds both pie charts
    fig, axs = plt.subplots(1,2)

    # creating the pie charts
    axs[0].pie(major_pop, labels=MAJORS, autopct="%.2f%%")
    axs[0].set_title("Major Popularity")
    axs[1].pie(year_pop, labels=["Year 1", "Year 2", "Year 3", "Year 4"], startangle=0, autopct="%.2f%%")
    axs[1].set_title("Year Distribution")
    
    # displaying the pie charts
    plt.show(block=False)
    os.system("cls")
    # closing the pie charts
    input("Press enter when done looking at the graphs --> ")
    plt.close(fig)

# function that contains the search students section of the code
def search_students():
    # input for the first name
    ans = input("\nPlease specify the students first name (enter -1 if unspecified) --> ")
    input_f_name = ans if ans != "-1"   else None
            
    # input for the last name
    ans = input("\nPlease specify the students last name (enter -1 if unspecified) --> ")
    input_l_name = ans if ans != "-1"   else None

    # input for the year
    ans = ""
    while type(ans) != type(1) and ans != "-1":
        ans = input("\nPlease specify the students year (enter -1 if unspecified) --> ")
        try:
            ans = int(ans)
        except ValueError:
            print("\nPlease enter a number"); delay()
    input_year = str(ans) if ans != -1   else None

    # input for the major
    ans = ""
    while not(ans in MAJORS) and ans != "-1":
        ans = input("\nPlease specify the students major (enter -1 if unspecified) --> ")
        if not(ans in MAJORS) and ans != "-1":
            print("\nPlease enter a major "); delay()
    input_major = ans if ans != "-1"   else None
    
    # input for the id
    ans = ""
    while (type(ans) != type(1) or len(str(ans)) != STUDENT_ID_LEN) and ans != -1:
        ans = input("\nPlease specify the students ID (enter -1 if unspecified) --> ")
        try:
            ans = int(ans)
        except ValueError:
            print(f"\nPlease enter a number with {STUDENT_ID_LEN} digits"); delay()
    input_id = str(ans) if ans != -1   else None

    
    
    # filtering the results
    sql_select = ""
    if input_f_name != None:
        sql_select += "WHERE f_name = '" + input_f_name + "'"
    
    if input_l_name != None:
        if sql_select == "":
            sql_select += "WHERE l_name = '" + input_l_name + "'"
        else:
            sql_select += " AND l_name = '" + input_l_name + "'"

    if input_year != None:
        if sql_select == "":
            sql_select += "WHERE study_year = '" + input_year + "'"
        else:
            sql_select += " AND study_year = '" + input_year + "'"

    if input_major != None:
        if sql_select == "":
            sql_select += "WHERE major = '" + input_major + "'"
        else:
            sql_select += " AND major = '" + input_major + "'"

    if input_id != None:
        if sql_select == "":
            sql_select += "WHERE id = '" + input_id + "'"
        else:
            sql_select += " AND id = '" + input_id + "'"

    mycursor.execute("SELECT * from students " + sql_select)

    # displaying the results
    os.system("cls")
    print(Fore.RED + tab(["First Name:","Last Name:","Year:","Major:","ID:","Email:"],3))
    for x in mycursor:
        print(Fore.WHITE + tab([x[0],x[1],x[2],x[3],x[4],x[5]], 3))
    
    print(Fore.WHITE + "\n1. Re-search\n2. Exit")
    ans = input("\nWhat would you like to do? (1 or 2) --> ")

    if ans == "1" or ans.lower().strip() == "one":
        search_students()

        
# ------------------------------------------------------------------
#             C O N S T A N T S  &  V A R R I A B L E S
# ------------------------------------------------------------------

# connecting the the database
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "Root",
    database = "University"
    )

# creating a cursor
mycursor = db.cursor(buffered=True)

# creation of the database and table 
# mycursor.execute("CREATE DATABASE University")
# mycursor.execute("CREATE TABLE students (f_name VARCHAR(20), l_name VARCHAR(20), study_year VARCHAR(1), major VARCHAR(20), id VARCHAR(15), email VARCHAR(15))")

# path for the current directory of the py file
path = "\\".join(__file__.split("\\")[:-1])

# list of all the currently taken ids
ids = []

# reading the constants.txt to import all the information about the constants
with open(path + "\constants.txt", "r") as file:
    MAJORS = file.readline()[:-1].split(" , ")
    FIRST_NAMES = file.readline()[:-1].split(" , ")
    LAST_NAMES = file.readline()[:-1].split(" , ")

# varriable to determine wheather the program is running or not
running = True
# varriable that states the length of student Id's
STUDENT_ID_LEN = 9

# ------------------------------------------------------------------
#                            M A I N
# ------------------------------------------------------------------


# clears the terminal
os.system("cls")

print("Hello and welcome to the student database"); delay()
while running:
    os.system("cls")

    # counts the amount of students in the database currently
    stu_count = 0
    mycursor.execute("SELECT id FROM students")
    for x in mycursor:
        stu_count += 1

    print(f"There are currently {stu_count} students loaded from the database"); delay()
    print("\n1. Add Students\n2. Delete Students\n3. Graph Students\n4. Search Students\n5. Quit Program"); delay()
    ans = input("\nWhat would you like to do? (1,2,3,4,5) --> ")

    # A D D I N G   S T U D E N T S
    if ans == "1" or ans.lower().strip() == "one" or ans.lower().strip() == "add":
        add_students()

    # D E L E T I N G   S T U D E N T S
    elif ans == "2" or ans.lower().strip() == "two" or ans.lower().strip() == "delete":
        delete_student()
    
    # G R A P H I N G   S T U D E N T S
    elif ans == "3" or ans.lower().strip() == "three" or ans.lower().strip() == "graph":
        graph_students()
    
    # S E A R C H I N G   S T U D E N T S
    elif ans == "4" or ans.lower().strip() == "four" or ans.lower().strip() == "search":
        search_students()

    # Q U I T
    elif ans == "5" or ans.lower().strip() == "five" or ans.lower().strip() == "quit":
        running = False
        plt.close()
        print("\nThank you for using this program, bye bye!\n")
    
    # I N V A L I D   I N P U T
    else:
        print("Sorry please try entering a valid input (1,2,3,4,5)"); delay()

    # commits the changes to the database every loop
    db.commit()
