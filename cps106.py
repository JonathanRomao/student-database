'''
Author: Jonathan Romao
Date Created: 09-18-2023
Date Modified: 11-27-2023

Description: I'm gonna create a database that stores student information (student #, name, year, major, contact info), 
and then allows you to search and filter through the students by any of their info. 
It would also sort the students by a parameter that the user specifies. The user will also be able to add and delete students if they please. 
There will be a 4th option, sort of to the side where the user can display the database for all the information (pie charts, bar graphs). 
'''

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

# function to generate each of the students attributes indvidually 
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

# function to delay the timing of the programs 
def delay(timing=1):
    time.sleep(timing)

# a function to update the ids list, which is used for the creation of the ids
def update_ids_list():
    global ids
    ids = [students[i].id for i in range(len(students))]
      
# function to generate n students
def generate_students(n):
    for i in range(n):
        update_ids_list()
        students.append(Student())

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
        ans = ""
        while type(ans) != type(1) and ans != "-1":
            ans = input("\nPlease specify the students year (enter -1 if unspecified) --> ")
            try:
                ans = int(ans)
            except ValueError:
                print("\nPlease enter a number"); delay()
        input_year = str(ans) if str(ans) != "-1"   else None
        
        # input for the major
        ans = ""
        while not(ans in MAJORS) and ans != "-1":
            ans = input("\nPlease specify the students major (enter -1 if unspecified) --> ")
            if not(ans in MAJORS) and ans != "-1":
                print("\nPlease enter a major "); delay()
        input_major = ans if ans != "-1"   else None

        # creating the student object
        students.append(Student(f_name = input_f_name, l_name = input_l_name, year = input_year, major = input_major))
      
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
    while not ans.isdigit() and len(ans) != STUDENT_ID_LEN:
        print(f"\nPlease enter a {STUDENT_ID_LEN} digit number")
        ans = input("\nPlease enter the students id number that you want to delete --> ")

    # removing the student from the data
    ind = ids.index(ans)
    removed_student = students.pop(ind)

    update_ids_list()
    print(f"\nYou have removed {removed_student.get_name()}"); delay()

# function that contains the graph students section of the code
def graph_students():
    # creating the data lists for the pie charts
    major_list = [students[i].major for i in range(len(students))]
    major_pop = [major_list.count(MAJORS[i]) for i in range(len(MAJORS))]
    year_list = [students[i].year for i in range(len(students))]
    year_pop = [year_list.count(["1","2","3","4"][i]) for i in range(4)]

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
    i = 0
    search_students_list = [students[j] for j in range(len(students))]
    while i < len(search_students_list):
        stu = search_students_list[i]
        if input_f_name != None and input_f_name != stu.f_name:
            search_students_list.pop(i)
        elif input_l_name != None and input_l_name != stu.l_name:
            search_students_list.pop(i)
        elif input_year != None and input_year != stu.year:
            search_students_list.pop(i)
        elif input_major != None and input_major != stu.major:
            search_students_list.pop(i)
        elif input_id != None and input_id != stu.id:
            search_students_list.pop(i)
        else:
            i += 1


    # displaying the results
    os.system("cls")
    print(Fore.RED + tab(["First Name:","Last Name:","Year:","Major:","ID:","Email:"],3))
    for s in search_students_list:
        print(Fore.WHITE + tab([s.f_name,s.l_name,s.year,s.major,s.id,s.email], 3))
    
    print("\n1. Re-search\n2. Exit")
    ans = input("\nWhat would you like to do? (1 or 2) --> ")

    if ans == "1" or ans.lower().strip() == "one":
        search_students()

# function that writes the data to the file 
def write_file():
    with open(path + "\students.txt", "w") as file:
        for i, stu in enumerate(students):
            if i != len(students) - 1:
                file.writelines(stu.write_to_file() + "\n")
            else:
                file.writelines(stu.write_to_file())

# function that reads the data from the file and creates one if the file doesn't exist
def read_file():
    temp1 = []
    try:
        with open(path + "\students.txt", "r") as file:
            file_contents = file.read()
            if file_contents != "":
                temp2 = file_contents.split("\n")
                temp2 = [temp2[i].split(",") for i in range(len(temp2))]
                for v in temp2:
                    temp1.append(Student(all_info=v))
    except FileNotFoundError:
        file = open("G:\My Drive\Sem 1\CPS 106\Programs\Big_project\students.txt", "x")
        file.close()
    return temp1

# ------------------------------------------------------------------
#                          C L A S S E S  
# ------------------------------------------------------------------

# a class that contains all the information about each student
class Student:
    def __init__(self, all_info=None, f_name=None, l_name=None, year=None, major=None):
        if all_info == None:
            self.f_name = f_name if f_name != None else generate_f_name()
            self.l_name =  l_name if l_name != None else generate_l_name()
            self.year = str(year) if year != None else generate_year()
            self.major = major if major != None else generate_major()
            self.id = generate_id()
            self.email = (self.f_name[0] + self.l_name[:3] + str(self.id)[-3:] + "@uni.ca").lower()
        else:
            self.f_name = all_info[0]
            self.l_name = all_info[1]
            self.year = all_info[2]
            self.major = all_info[3]
            self.id = all_info[4]
            self.email = all_info[5]

    def __str__(self):
        return f"Name: {self.f_name} {self.l_name}\nYear: {self.year}\nID: {self.id} \nMajor: {self.major}"
    
    def get_name(self):
        return f"{self.f_name} {self.l_name}" 
    
    def write_to_file(self):
        return f"{self.f_name},{self.l_name},{self.year},{self.major},{self.id},{self.email}"

# ------------------------------------------------------------------
#             C O N S T A N T S  &  V A R R I A B L E S
# ------------------------------------------------------------------

# path for the current directory of the py file
path = "\\".join(__file__.split("\\")[:-1])

# varriables that store the students info
students = read_file()
# list of all the currently taken ids
ids = []
update_ids_list()

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

    print(f"There are currently {len(students)} students loaded from the database"); delay()
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
        write_file()
        print("\nThank you for using this program, bye bye!\n")
    
    # I N V A L I D   I N P U T
    else:
        print("Sorry please try entering a valid input (1,2,3,4,5)"); delay()

    update_ids_list()