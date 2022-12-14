import sqlite3
import bcrypt
import csv
from datetime import datetime

dt = datetime.now()

import curses

# pipen install windows-curses
from curses import wrapper

# pipen install tqdm
from tqdm import tqdm
import time
import os


connection = sqlite3.connect("assessments.db")
cursor = connection.cursor()


def loading_bar():
    text = ""
    for char in tqdm(["a", "b", "c", "d"], leave=False):
        time.sleep(0.25)
        text += char


def input_not_recognized(asdf):
    asdf.clear()
    asdf.addstr(0, 0, "ERROR\n \nINPUT NOT RECOGNIZED \n \nPRESS ENTER TO CONTINUE \n")
    asdf.refresh()
    asdf.getch()


def make_table():
    with open("data.sql") as exercise:
        queries = exercise.read()

        cursor.executescript(queries)
        connection.commit()


def import_mock_users():
    try:
        insert_query = "INSERT INTO Users (full_name, phone, email, user_type, hire_date, date_created) VALUES(?, ?, ?, ?, ?, ?);"

        with open("MOCK_DATA.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            csv_data = []

            fields = next(reader)
            # print(fields)
            for row in reader:
                csv_data.append(row)

        for user in csv_data:
            cursor.execute(insert_query, user)

        connection.commit()

        print("\n ////////// MOCK USERS ADDED /////////// \n")
    except sqlite3.IntegrityError:
        return None


def import_tests(test_list):
    try:
        with open("import_tests.csv", "w", newline="") as writing_csv:
            writer = csv.writer(writing_csv)
            writer.writerow(["date_created"])
            for data in test_list:
                writer.writerow(data)

        insert_query = "INSERT INTO Competency_Assessment_Data (comp_name, test_name, date_created) VALUES(?,?,?);"

        with open("import_tests.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            csv_data = []

            fields = next(reader)
            # print(fields)
            for row in reader:
                csv_data.append(row)

        for user in csv_data:
            cursor.execute(insert_query, user)

        connection.commit()
        print("\n ////////// TESTS ADDED ////////// \n")
    except:
        return None


list_of_lists_of_tests = [
    [
        "Computer Anatomy",
        "Physical Computer Anatomy Test",
        str(dt.strftime("%m/%d/%Y")),
    ],
    ["Data Types", "Data Types Exam", str(dt.strftime("%m/%d/%Y"))],
    ["Variables", "Variables Exam", str(dt.strftime("%m/%d/%Y"))],
    ["Functions", "Functions Exam", str(dt.strftime("%m/%d/%Y"))],
    [
        "Boolean Logic",
        "Building Block Boolean Logic Test",
        str(dt.strftime("%m/%d/%Y")),
    ],
    ["Conditionals", "Physical Conditiols Test", str(dt.strftime("%m/%d/%Y"))],
    ["Loops", "Fruit Loops Test", str(dt.strftime("%m/%d/%Y"))],
    [
        "Data Structures",
        "Data Structures Competency Exam",
        str(dt.strftime("%m/%d/%Y")),
    ],
    ["Lists", "List Exam", str(dt.strftime("%m/%d/%Y"))],
    ["Dictionaries", "Dictionaries Exam", str(dt.strftime("%m/%d/%Y"))],
    [
        "Working with Files",
        "Working with Files Competency Exam",
        str(dt.strftime("%m/%d/%Y")),
    ],
    ["Exception Handling", "Exception Handling Exam", str(dt.strftime("%m/%d/%Y"))],
    ["Quality Assurance (QA)", "Physical QA Exam", str(dt.strftime("%m/%d/%Y"))],
    ["Object-Oriented Programming", "OOP Exam", str(dt.strftime("%m/%d/%Y"))],
    ["Recursion", "Recursion Exam", str(dt.strftime("%m/%d/%Y"))],
    ["Databases", "Databases Exam", str(dt.strftime("%m/%d/%Y"))],
]


def import_mock_test_results():
    try:
        insert_query = "INSERT INTO Assessment_Results (test_id, comp_id, user_id, score, date_taken, admin_id, best_score) VALUES(?, ?, ?, ?, ?, ?, ?);"

        with open("MOCK_TESTS.csv", "r") as csv_file:
            reader = csv.reader(csv_file)
            csv_data = []

            fields = next(reader)
            # print(fields)
            for row in reader:
                csv_data.append(row)

        for user in csv_data:
            cursor.execute(insert_query, user)

        connection.commit()
        return print("\n ////////// MOCK TEST RESULTS ADDED ////////// \n")

    except sqlite3.IntegrityError:
        return None


class Users:
    def __init__(
        self,
        name,
        phone,
        email,
        hire_date,
        date_created,
        id=None,
        hashed_password=None,
        user_type="user",
        active=True,
    ):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.hashed_password = hashed_password
        self.user_type = user_type
        self.date_created = date_created
        self.hire_date = hire_date
        self.active = active
        self.attributes = [
            self.name,
            self.phone,
            self.email,
            self.hashed_password,
            self.user_type,
            self.date_created,
            self.hire_date,
            self.active,
            self.id,
        ]

    def db_update(self):
        self.attributes = [
            self.name,
            self.phone,
            self.email,
            self.hashed_password,
            self.user_type,
            self.date_created,
            self.hire_date,
            self.active,
            self.id,
        ]

        query = "UPDATE Users SET full_name = ?, phone = ?, email = ?, hashed_password = ?, user_type = ?, date_created = ?, hire_date = ?, active = ? WHERE user_id = ?;"

        cursor.execute(query, self.attributes)
        connection.commit()

    def insert_user(self):
        self.attributes = [
            self.name,
            self.phone,
            self.email,
            self.hashed_password,
            self.user_type,
            self.date_created,
            self.hire_date,
            self.active,
        ]

        query = "INSERT Users SET full_name = ?, phone = ?, email = ?, hashed_password = ?, user_type = ?, date_created = ?, hire_date = ?, active = ?"

    def pass_check(self, pass_change=None):
        first_pass = False
        new_password = False
        salt = bcrypt.gensalt()
        if self.attributes[3]:
            while True:
                if new_password == True:
                    break
                else:
                    current_pass = self.attributes[3]
                    pass_check = input(
                        "Input current password \n[PRESS ENTER TO RETURN] \n > "
                    )
                    os.system("cls||clear")
                    pass_check = pass_check.encode()
                    if pass_check:
                        encoded_pass = current_pass.encode()
                        password_matches = bcrypt.checkpw(pass_check, encoded_pass)
                        if password_matches == True:
                            if pass_change:
                                break
                            else:
                                return True
                        else:
                            print("Password incorrect")
                            continue
                    else:
                        os.system("cls||clear")
                        return None

            if pass_change:
                while True:
                    new_pass = input(
                        "Input new password \n[PRESS ENTER TO RETURN] \n > "
                    )
                    if new_pass:
                        new_pass = new_pass.encode()
                        confirm_pass = input("Confirm new password \n > ")
                        confirm_pass = confirm_pass.encode()
                        if new_pass == confirm_pass:
                            new_password = True
                            os.system("cls||clear")
                            break
                        else:
                            continue
                    else:
                        os.system("cls||clear")
                        return None

        elif not self.attributes[3]:
            while True:
                new_pass = input(
                    "Password not found. Please enter new password \n[PRESS ENTER TO RETURN] \n > "
                )
                if new_pass:
                    new_pass = new_pass.encode()
                    confirm_pass = input("Confirm first password \n > ")
                    confirm_pass = confirm_pass.encode()
                    os.system("cls||clear")
                    if new_pass == confirm_pass:
                        first_pass = True
                        break
                    else:
                        input(
                            "ERROR: Passwords do not match \nPRESS ENTER TO CONTINUE \n"
                        )
                else:
                    os.system("cls||clear")
                    return None

        new_pass = bcrypt.hashpw(confirm_pass, salt)
        new_pass = new_pass.decode()
        self.hashed_password = new_pass
        self.attributes[3] = self.hashed_password

        self.db_update()

        if new_password == True:
            os.system("cls||clear")
            print("\n///// Password has been changed ///// \n")
            return True

        if first_pass == True:
            print("\n///// First password has been created ///// \n")
            return True


def add_user():
    name_checkpoint = False
    phone_checkpoint = False
    email_checkpoint = False
    date_checkpoint = False
    valid_checkpoint = False
    os.system("cls||clear")
    while True:
        if name_checkpoint == False:
            full_name = input(
                "Enter new users full name (first and last) \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING] \n > "
            )
            if not full_name:
                return None
            name_checkpoint = True

        if phone_checkpoint == False:
            phone = input(
                "Enter new users phone number: \n[PRESS ENTER IF PHONE NUMBER IS CURRENTLY UNKNOWN] \n >  "
            )
            if not phone:
                print(
                    "!!!!! REMINDER !!!!! \nPhone number has not been entered for this user. Please ensure their phone number will be entered in at a later date as soon as possible! \n"
                )
                phone = "UPDATE ASAP"
            phone_checkpoint = True

        if email_checkpoint == False:
            email = input(
                "Enter users email: \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING] \n > "
            )
            if email:
                print(
                    "!!!!! REMINDER !!!!! \nEmail entered, please remind user they can create the password to their login when they first login \n"
                )
            elif not email:
                return None
            email_checkpoint = True

        if date_checkpoint == False:
            hire_date = input(
                "Please enter users hire date: \nIf Hire date is currently unkown, undecided, or the information is currently unavailable at this time, please enter 'N/A' \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING]\n  (MM/DD/YYYY) \n > "
            )
            if not hire_date:
                return None
            if hire_date.upper() == "N/A" or hire_date.upper() == "N\A":
                hire_date = "INFO REQUIRED"
            date_checkpoint = True

        while (
            name_checkpoint
            and phone_checkpoint
            and email_checkpoint
            and date_checkpoint
            and valid_checkpoint == False
        ):
            while True:
                validate_info = input(
                    f'Please validate the following information has been entered correctly. \n[1] Full name: {full_name} \n[2] Phone: {phone} \n[3] Email: {email} \n[4] Hire date: {hire_date} \n[Q] Quit to menu without saving \n \nIf all entered information is correct, please hit "ENTER" \nIf any information is incorrect, please enter the corrisponding number to the field that requires changing. \n > '
                )
                if validate_info:
                    if validate_info.upper() == "Q":
                        return None
                    elif validate_info == "1":
                        name_checkpoint = False
                        break
                    elif validate_info == "2":
                        phone_checkpoint = False
                        break
                    elif validate_info == "3":
                        email_checkpoint = False
                        break
                    elif validate_info == "4":
                        date_checkpoint = False
                        break
                    else:
                        wrapper(input_not_recognized)
                        os.system("cls||clear")
                        break
                else:
                    valid_checkpoint = True

                    break

        while valid_checkpoint == True:
            date_created = str(dt.strftime("%m/%d/%Y"))
            new_user = Users(full_name, phone, email, hire_date, date_created)

            query = "INSERT INTO Users (full_name, phone, email, hashed_password, user_type, date_created, hire_date, active, user_id) VALUES (?,?,?,?,?,?,?,?,?)"

            cursor.execute(query, new_user.attributes)
            connection.commit()
            return print("User added")


def get_user(user_id=None, email=None):
    watever = ()
    if user_id:
        query = "SELECT * FROM Users WHERE user_id = ?"
        watever = (user_id,)

    elif email:
        query = "SELECT * FROM Users WHERE email = ?"
        watever = (email,)

    (
        id,
        names,
        phone,
        email,
        hashed_password,
        user_type,
        date_created,
        hire_date,
        active,
    ) = cursor.execute(query, watever).fetchone()

    user = Users(
        names,
        phone,
        email,
        hire_date,
        date_created,
        id,
        hashed_password,
        user_type,
        active,
    )

    return user


def search_users():
    while True:
        os.system("cls||clear")
        name_for_search = input(
            "Enter name you would like to search. \n(Entering name partially will work as long as input is spelt correctly) \n \n[PRESS ENTER TO RETURN] \n > "
        )
        if name_for_search:
            name_for_search = f"%{name_for_search}%"
            while True:
                query = "SELECT * FROM Users WHERE full_name like ?;"
                rows = cursor.execute(query, (name_for_search,)).fetchall()
                if not rows:
                    os.system("cls||clear")
                    input(
                        "NO USERS FOUND WITH THAT NAME \n \nPRESS ENTER TO CONTINUE\n"
                    )
                    break
                print(
                    f'{"User ID":<9}{"Full name":<19}{"Phone Number":<14}{"email":<31}{"Hashed Password":<18}{"User Type":<12}{"Date Added":<12}{"Hire Date":<12}{"Active":<}'
                )
                for row in rows:
                    if row[4]:
                        hash_pass = "True"
                    else:
                        hash_pass = "None"
                    print(
                        f"{row[0]:<9}{row[1]:<19}{row[2]:<14}{row[3]:<31}{hash_pass:<18}{row[5]:<12}{row[6]:<12}{row[7]:<12}{row[8]:<8}"
                    )
                inquiry = input(
                    "To select a specific user above, enter their User ID \n[TO SEARCH AGAIN PRESS ENTER] \n > "
                )
                if inquiry:
                    try:
                        os.system("cls||clear")
                        view_users(inquiry)
                    except TypeError:
                        wrapper(input_not_recognized)
                        os.system("cls||clear")
                else:
                    break
        else:
            return None


def view_users(id_num=None, email=None, user_type_filter=None):
    # os.system("cls||clear")
    while True:
        if user_type_filter:
            query = "SELECT * FROM Users WHERE user_type ="
            if user_type_filter == "user" or user_type_filter == "User":
                query = f"{query} 'user'"

            elif user_type_filter == "admin" or user_type_filter == "Admin":
                query = f"{query} 'admin'"

            rows = cursor.execute(query).fetchall()

            print(
                f'{"User ID":<9}{"Full name":<19}{"Phone Number":<14}{"email":<31}{"Hashed Password":<18}{"User Type":<12}{"Date Added":<12}{"Hire Date":<12}{"Active":<}'
            )
            for row in rows:
                if row[4]:
                    hash_pass = "True"
                else:
                    hash_pass = "None"
                print(
                    f"{row[0]:<9}{row[1]:<19}{row[2]:<14}{row[3]:<31}{hash_pass:<18}{row[5]:<12}{row[6]:<12}{row[7]:<12}{row[8]:<8}"
                )
            return None

        if admin == True:
            if not id_num:
                rows = cursor.execute("SELECT * FROM Users").fetchall()
                print(
                    f'{"User ID":<9}{"Full name":<19}{"Phone Number":<14}{"email":<31}{"Hashed Password":<18}{"User Type":<12}{"Date Added":<12}{"Hire Date":<12}{"Active":<}'
                )
                for row in rows:
                    if row[4]:
                        hash_pass = "True"
                    else:
                        hash_pass = "None"
                    print(
                        f"{row[0]:<9}{row[1]:<19}{row[2]:<14}{row[3]:<31}{hash_pass:<18}{row[5]:<12}{row[6]:<12}{row[7]:<12}{row[8]:<8}"
                    )
                return None
            elif id_num or email:
                if id_num:
                    id_num = f"{id_num}"
                    selected_user = get_user(id_num)
                    query = "SELECT * FROM Users WHERE user_id = ?"
                    watever = (id_num,)
                elif email:
                    email = f"{email}"
                    selected_user = get_user(None, email)
                    query = "SELECT * FROM Users WHERE email = ?"
                    watever = (email,)
                while True:
                    row = cursor.execute(query, watever).fetchone()
                    print(
                        f"{'User ID: '} {row[0]} \n{'[1] Name: '} {row[1]} \n{'[2] Phone: '} {row[2]} \n{'[3] Email: '}{row[3]} \n{'[4] Hashed Password: '} {row[4]} \n{'[5] User Type: '} {row[5]} \n{'[6] Date Created: '} {row[6]} \n{'[7] Hire Date: '} {row[7]} \n{'[8] Active: '} {row[8]} \n \n[D]elete \n"
                    )

                    inquiry = input(
                        "To make changes to any information, enter the number of the field. \n[TO RETURN TO MENU PRESS ENTER]\n > "
                    )
                    inquiry_range = ("1", "2", "3", "4", "5", "6", "7", "8", "d", "D")
                    if inquiry:
                        if inquiry not in inquiry_range:
                            inquiry = None
                            wrapper(input_not_recognized)
                            os.system("cls||clear")
                        else:
                            if inquiry.upper() == "D":
                                os.system("cls||clear")
                                confirmation = input(
                                    "WARNING. DELETING USERS NOT RECOMMENEDED. INFORMATION WILL HAVE TO BE RE-ENTERED MANUALLY IF DELETED. \n \nAre you sure you would like to delete this user? \n[Y]es \n[N]o \n > "
                                )
                                if confirmation.upper() == "Y":
                                    if id_num:
                                        query = "DELETE FROM Users WHERE user_id = ?"
                                    if email:
                                        query = "DELETE FROM Users WHERE email = ?"
                                    cursor.execute(query, watever)
                                    connection.commit()
                                    os.system("cls||clear")
                                    return input(
                                        "USER HAS BEEN DELETED \nPRESS ENTER TO CONTINUE \n"
                                    )

                                elif confirmation.upper() == "N":
                                    os.system("cls||clear")

                                else:
                                    wrapper(input_not_recognized)
                                    os.system("cls||clear")
                            elif inquiry == "1":
                                name_change = input(
                                    "Enter new full name for User \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n > "
                                )
                                os.system("cls||clear")
                                if name_change:
                                    selected_user.name = name_change
                                    selected_user.db_update()

                            elif inquiry == "2":
                                phone_change = input(
                                    "Enter new phone number for User \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n[###-###-####] \n > "
                                )
                                os.system("cls||clear")
                                if phone_change:
                                    selected_user.phone = phone_change
                                    selected_user.db_update()

                            elif inquiry == "3":
                                email_change = input(
                                    "Enter new email for User \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n > "
                                )
                                os.system("cls||clear")
                                if email_change:
                                    selected_user.email = email_change
                                    selected_user.db_update()

                            elif inquiry == "4":
                                os.system("cls||clear")
                                selected_user.pass_check(pass_change=True)

                            elif inquiry == "5":
                                if selected_user.user_type == "user":
                                    selected_user.user_type = "admin"
                                else:
                                    selected_user.user_type = "user"
                                os.system("cls||clear")
                                selected_user.db_update()

                            elif inquiry == "6":
                                validate_change = input(
                                    "!!!!! WARNING !!!!! \nCreated date represents when user was added into the system. Changing this requires supervisor permission! \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \nTo make changes, enter new created date for User \n  (MM/DD/YYYY) \n > "
                                )
                                os.system("cls||clear")
                                if validate_change:
                                    selected_user.date_created = validate_change
                                    selected_user.date_created
                                    selected_user.db_update()

                            elif inquiry == "7":
                                validate_change = input(
                                    "!!!!! WARNING, HIRE DATE HAS BEEN SELECTED FOR CHANGE !!!!! \nHire date represents the date user has submitted legal forms (Form W-4, Form I-9, state forms, and other payroll withholding forms) \nMAKING THIS CHANGE REQUIRES SUPERVISOR PERMISSION \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \nTo make changes to Hire Date, enter new hire date for User \n  (MM/DD/YYYY) \n >  "
                                )
                                os.system("cls||clear")
                                if validate_change:
                                    selected_user.hire_date = validate_change
                                    selected_user.hire_date
                                    selected_user.db_update()

                            elif inquiry == "8":
                                if selected_user.active:
                                    selected_user.active = False
                                else:
                                    selected_user.active = True
                                os.system("cls||clear")
                                selected_user.db_update()

                    else:
                        os.system("cls||clear")
                        return None

        elif admin == False:
            if id_num or email:
                if id_num:
                    id_num = f"{id_num}"
                    selected_user = get_user(id_num)
                    query = "SELECT * FROM Users WHERE user_id = ?"
                    watever = (id_num,)
                elif email:
                    email = f"{email}"
                    selected_user = get_user(None, email)
                    query = "SELECT * FROM Users WHERE email = ?"
                    watever = (email,)
                while True:
                    row = cursor.execute(query, watever).fetchone()

                    print(
                        f"\n{'Name: '} {row[1]} \n{'Phone: '} {row[2]} \n{'Email: '}{row[3]} \n{'Hashed Password: '} {row[4]}\n{'Hire Date: '} {row[7]} \n"
                    )

                    inquiry = input(
                        "[1] Change full name (first and last) \n[2] Change Phone \n[3] Change password \n[TO RETURN TO MENU PRESS ENTER] \n \n(FOR OTHER INFORMATION THAT YOU WISH TO BE CHANGED, PLEASE SPEAK WITH A SUPERVISOR) \n > "
                    )

                    if inquiry:
                        if inquiry == "1":
                            new_name = input(
                                "Enter your new Full Name \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n > "
                            )
                            if new_name:
                                os.system("cls||clear")
                                selected_user.name = new_name
                                selected_user.db_update()
                        elif inquiry == "2":
                            new_phone = input(
                                "Enter your new phone number \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n > "
                            )
                            if new_phone:
                                os.system("cls||clear")
                                selected_user.phone = new_phone
                                selected_user.db_update()
                        elif inquiry == "3":
                            os.system("cls||clear")
                            selected_user.pass_check(pass_change=True)
                    else:
                        return None


class Test_Results:
    def __init__(
        self,
        comp_id,
        user_id,
        score,
        date_taken,
        admin_id,
        id=None,
        best_score=False,
    ):
        self.id = id
        self.comp_id = comp_id
        self.user_id = user_id
        self.score = score
        self.date_taken = date_taken
        self.admin_id = admin_id
        self.best_score = best_score
        self.attributes = [
            self.comp_id,
            self.user_id,
            self.score,
            self.date_taken,
            self.admin_id,
            self.best_score,
        ]

    def db_update(self):
        self.attributes = [
            self.comp_id,
            self.user_id,
            self.score,
            self.date_taken,
            self.admin_id,
            self.best_score,
            self.id,
        ]

        query = "UPDATE Assessment_Results SET comp_id = ?, user_id = ?, score = ?, date_taken = ?, admin_id = ?, best_score = ? WHERE test_id = ?;"

        cursor.execute(query, self.attributes)
        connection.commit()


def add_test_results():
    comp_id_checkpoint = False
    user_id_checkpoint = False
    score_checkpoint = False
    date_checkpoint = False
    admin_checkpoint = False
    best_score_checkpoint = False
    validate_checkpoint = False

    while True:
        if comp_id_checkpoint == False:
            view_competencies()
            comp_id = input(
                "Please input the competency ID belonging to the competency this test belongs long to \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING] \n > "
            )
            if not comp_id:
                return None
            comp_id_checkpoint = True

        if user_id_checkpoint == False:
            view_users(user_type_filter="user")
            user_id = input(
                "Input user ID of user that took this test \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING, HIT ENTER] \n > "
            )
            if not user_id:
                return None
            user_id_checkpoint = True

        if score_checkpoint == False:
            score = input(
                "Input New Score (0-4) \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING] \n > "
            )
            while True:
                if not score:
                    return None
                else:
                    score_range = ("0", "1", "2", "3", "4")
                    if score not in score_range:
                        score = input(
                            "INVALID. NOT WITHIN SCORE RANGE \nInput New Score (0-4) \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING] \n > "
                        )
                        continue
                    elif score in score_range:
                        score_checkpoint = True
                        if score == "0":
                            score = "0 (No competency)"
                            break

                        elif score == "1":
                            score = "1 (Basic Competency)"
                            break

                        elif score == "2":
                            score = "2 (Intermediate Competency)"
                            break

                        elif score == "3":
                            score = "3 (Advanced Competency)"
                            break

                        elif score == "4":
                            score = "4 (Expert Competency)"
                            break

        if date_checkpoint == False:
            date = input(
                "Input Date test was taken \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING]\n  (MM/DD/YYYY) \n > "
            )
            if not date:
                return None
            date_checkpoint = True

        if admin_checkpoint == False:
            view_users(user_type_filter="admin")
            admin_id = input(
                "Input ID Manager that monitored the test \n[IF NO MANAGER MONITORED TEST, HIT ENTER. HOWEVER SOME TESTS LIKE FOR COMPETENCY 1 REQUIRE A MANAGER TO MONITOR TEST] \n > "
            )
            if not admin_id:
                admin_id = "N/A"
            admin_checkpoint = True

        if best_score_checkpoint == False:
            check_score = set_best_score(user_id, comp_id, score, date)
            if bool(check_score):
                best_score = True
                # input(f"best score is {best_score}")
            else:
                best_score = False
                # input(f"best score is {best_score}")

            best_score_checkpoint = True

        if (
            comp_id_checkpoint
            and user_id_checkpoint
            and score_checkpoint
            and date_checkpoint
            and admin_checkpoint
            and best_score_checkpoint
        ):
            while True:
                if validate_checkpoint == True:
                    break
                else:
                    validate_info = input(
                        f"Please review information.\n[1] Competency ID: {comp_id} \n[2] User ID: {user_id} \n[3] Score: {score} \n[4] Date test was taken: {date} \n[5] Admin ID: {admin_id} \n[6] Best score: {best_score} \n[Q] Quit to menu without saving \n \nTo make changes to any fields, enter the fields corrisponding number. To enter created test results, press 'ENTER' \n > "
                    )
                    if not validate_info:
                        validate_checkpoint = True
                        break
                    elif validate_info:
                        if validate_info.upper() == "Q":
                            return None
                        elif validate_info == "1":
                            comp_id_checkpoint = False
                            best_score_checkpoint = False
                            break
                        elif validate_info == "2":
                            user_id_checkpoint = False
                            best_score_checkpoint = False
                            break
                        elif validate_info == "3":
                            score_checkpoint = False
                            best_score_checkpoint = False
                            break
                        elif validate_info == "4":
                            date_checkpoint = False
                            best_score_checkpoint = False
                            break
                        elif validate_info == "5":
                            admin_checkpoint = False
                        elif validate_info == "6":
                            ensureance = input(
                                "!!!! WARNING !!!!! \nCHANGING THE BEST SCORE IS NOT RECOMMENDED AS IT AUTOMATICALLY UNCHECKS ALL OTHER ATTEMPTS FROM THIS TEST WHEN BEST SCORE IS DETERMINED AS TRUE \n WOULD YOU LIKE TO CONTINUE TO CHANGE BEST SCORE? \n[Y]es \n[N]o \n \n > "
                            )
                            if ensureance:
                                while True:
                                    if ensureance.upper() == "Y":
                                        if best_score:
                                            best_score = False
                                        else:
                                            best_score = True
                                        break

                                    elif ensureance.upper() == "N":
                                        break

                                    else:
                                        wrapper(input_not_recognized)
                                        os.system("cls||clear")
                                        break
                            else:
                                input(
                                    "No changes have been made \nPress enter to continue"
                                )
                                break

                        else:
                            wrapper(input_not_recognized)
                            os.system("cls||clear")
                            break

        while validate_checkpoint == True:
            new_test = Test_Results(
                comp_id, user_id, score, date, admin_id, best_score=best_score
            )

            query = "INSERT INTO Assessment_Results (comp_id, user_id, score, date_taken, admin_id, best_score) VALUES (?,?,?,?,?,?)"

            cursor.execute(query, new_test.attributes)
            connection.commit()
            return print("Test Added")


def set_best_score(user_id, comp_id, new_score, new_date, debug=None):
    is_best = False
    query = "SELECT * FROM Assessment_Results WHERE user_id = ? AND comp_id = ? ORDER BY date_taken DESC"
    rows = cursor.execute(query, (user_id, comp_id)).fetchall()
    if not rows:
        return True
    else:
        for row in rows:
            if new_date >= row[4]:
                input(row[3])
                if int(new_score[0]) >= int(row[3][0]):
                    prev_test = get_test(row[0])
                    prev_test.best_score = "0"
                    prev_test.db_update()
                    is_best = True
                else:
                    is_best = False
            else:
                is_best = False

    if debug:
        print(
            f"{'[0] Test ID':<13}{'[1] Comp ID':<12}{'[2] User ID':<12}{'[3] Score':<62}{'[4] Date':<15}{'[5] Admin ID':<13}{'[6] Best Score':<15}"
        )

        for row in rows:
            row = [str(i) for i in row]
            print(
                f"{row[0]:<13}{row[1]:<12}{row[2]:<12}{row[3]:<62}{row[4]:<15}{row[5]:<13}{row[6]:<15}"
            )

        print("HERE LOOK HERE")
        print(is_best)
        input()

    if is_best:
        return True
    else:
        return False


def get_test(test_id):

    query = "SELECT * FROM Assessment_Results WHERE test_id = ?"

    (
        id,
        comp_id,
        user_id,
        score,
        date_taken,
        admin_id,
        best_score,
    ) = cursor.execute(query, (test_id,)).fetchone()

    test = Test_Results(
        comp_id,
        user_id,
        score,
        date_taken,
        admin_id,
        id,
        best_score,
    )

    return test


def view_test_results(id_num=None, test_id=None, email=None):
    query = """SELECT ar.test_id, ar.comp_id, cad.test_name, ar.user_id, u.full_name, ar.score, ar.date_taken, ar.admin_id, m.full_name, ar.best_score, u.email
    FROM Assessment_Results ar
    LEFT OUTER JOIN Users u
        ON ar.user_id = u.user_id 
    LEFT OUTER JOIN Users m 
        ON m.user_id = ar.admin_id
    LEFT OUTER JOIN Competency_Assessment_Data cad
        ON cad.comp_id = ar.comp_id"""
    while True:

        if admin:
            if not test_id and not id_num:

                rows = cursor.execute(query).fetchall()

                print(
                    f"{'Test ID':<8}{'Comp ID':<8}{'Test Name':<35}{'User ID':<8}{'Name':<20}{'Score':<30}{'Date':<11}{'Admin ID':<9}{'Admined By':<20}{'Best Score':}"
                )

                for row in rows:
                    row = [str(i) for i in row]
                    print(
                        f"{row[0]:<8}{row[1]:<8}{row[2]:<35}{row[3]:<8}{row[4]:<20}{row[5]:<30}{row[6]:<11}{row[7]:<9}{row[8]:<15}{row[9]:>10}"
                    )
                break

            elif id_num:
                query = f"{query} WHERE ar.user_id = ?;"
                rows = cursor.execute(query, (id_num,)).fetchall()
                if rows:
                    print(
                        f"{'Test ID':<8}{'Comp ID':<8}{'Test Name':<40}{'User ID':<8}{'Name':<20}{'Score':<30}{'Date':<11}{'Admin ID':<9}{'Admin Name':<20}{'Best Score':>}"
                    )

                    for row in rows:
                        row = [str(i) for i in row]
                        print(
                            f"{row[0]:<8}{row[1]:<8}{row[2]:<40}{row[3]:<8}{row[4]:<20}{row[5]:<30}{row[6]:<11}{row[7]:<9}{row[8]:<20}{row[9]:>10}"
                        )
                    break
                else:
                    wrapper(input_not_recognized)
                    return print(end="\r")

            elif test_id:
                test_id = f"{test_id}"
                query = f"{query} WHERE ar.test_id = ?;"
                selected_test = get_test(test_id)
                while True:
                    # print(query)
                    row = cursor.execute(query, (test_id,)).fetchone()
                    connection.commit()
                    print(
                        f"Test ID: {row[0]} \n[1] Competency ID: {row[1]} \n[2] Test Name: {row[2]} \n[3] User ID: {row[3]} \n[4] Name: {row[4]} \n[5] Score: {row[5]} \n[6] Date: {row[6]} \n[7] Manager ID: {row[7]} \n[8] Acting Test Admin (Manager): {row[8]} \n[9] Best Score: {row[9]} \n \n[D]elete Test Results \n"
                    )
                    inquiry = input(
                        "To make changes to any information, enter the number of the field. \n[TO RETURN TO MENU PRESS ENTER]\n > "
                    )
                    inquiry_range = (
                        "1",
                        "2",
                        "3",
                        "4",
                        "5",
                        "6",
                        "7",
                        "8",
                        "9",
                        "D",
                        "d",
                    )
                    if inquiry:
                        if inquiry not in inquiry_range:
                            inquiry = None
                            wrapper(input_not_recognized)
                            os.system("cls||clear")
                            continue
                        else:
                            if inquiry.upper() == "D":
                                confirmation = input(
                                    "Are you sure you would like to delete this assessment results? Doing so cannot be undone and information will have to be re-added! \n!!!! Warning !!!! \nDoing this is not recommended, especially for older scores \n[Y]es \n[N]o \n \n > "
                                )
                                os.system("cls||clear")

                                if confirmation.upper() == "Y":
                                    cursor.execute(
                                        "DELETE FROM Assessment_Results WHERE test_id = ?;",
                                        (test_id,),
                                    )
                                    os.system("cls||clear")
                                    connection.commit()
                                    return input(
                                        "ASSESSMENT RESULTS HAVE BEEN DELETED \n \nPRESS RETURN TO CONTINUE \n"
                                    )

                                elif confirmation.upper() == "N":
                                    os.system("cls||clear")

                                else:
                                    wrapper(input_not_recognized)
                                    os.system("cls||clear")

                            elif inquiry == "1" or inquiry == "2":
                                view_competencies()

                                if inquiry == "1":
                                    new_comp = input(
                                        "Input new competency ID \n[PRESS ENTER TO RETURN] \n > "
                                    )
                                    os.system("cls||clear")

                                elif inquiry == "2":
                                    new_comp = input(
                                        "Test Name changes according to Competency ID number. To change Test Name, input Competency ID of the desired Test Name \n[PRESS ENTER TO RETURN] \n >"
                                    )
                                    os.system("cls||clear")

                                if new_comp:
                                    selected_test.comp_id = new_comp
                                    selected_test.db_update()

                            elif inquiry == "3" or inquiry == "4":
                                os.system("cls||clear")
                                view_users(None, None, "user")
                                if inquiry == "3":
                                    new_user_id = input(
                                        "Input User ID of desired User \n[PRESS ENTER TO RETURN] \n > "
                                    )

                                elif inquiry == "4":
                                    new_user_id = input(
                                        "\nName of the test taker changes according to the User ID. Input User ID of desired User \n[PRESS ENTER TO RETURN] \n > "
                                    )

                                if new_user_id:
                                    selected_test.user_id = new_user_id
                                    selected_test.db_update()

                            elif inquiry == "5":
                                new_score = input(
                                    "Input New Score (0-4) \n[PRESS ENTER TO RETURN] \n > "
                                )
                                os.system("cls||clear")

                                while True:
                                    if not new_score:
                                        break
                                    else:
                                        score_range = ("0", "1", "2", "3", "4")
                                        if new_score not in score_range:
                                            new_score = input(
                                                "INVALID. NOT WITHIN SCORE RANGE \nInput New Score (0-4) \n[PRESS ENTER TO RETURN] \n > "
                                            )
                                            os.system("cls||clear")
                                            continue
                                        else:
                                            if new_score == "0":
                                                new_score = "0 (No competency)"

                                            elif new_score == "1":
                                                new_score = "1 (Basic Competency - Needs Ongoing Support)"

                                            elif new_score == "2":
                                                new_score = (
                                                    "2 (Intermediate Competency)"
                                                )

                                            elif new_score == "3":
                                                new_score = "3 (Advanced Competency)"

                                            elif new_score == "4":
                                                new_score = "4 (Expert Competency)"

                                            selected_test.score = new_score
                                            selected_test.db_update()
                                            break

                            elif inquiry == "6":
                                new_date = input(
                                    "Input date change for when test was taken \n[PRESS ENTER TO RETURN] \n  (MM/DD/YYYY) \n > "
                                )
                                os.system("cls||clear")
                                if new_date:
                                    selected_test.date_taken = new_date
                                    selected_test.db_update()

                            elif inquiry == "7" or inquiry == "8":
                                os.system("cls||clear")
                                view_users(None, None, "admin")
                                if inquiry == "7":
                                    new_admin_id = input(
                                        "Input Admin ID of desired Admin \n[PRESS ENTER TO RETURN] \n > "
                                    )
                                    os.system("cls||clear")

                                elif inquiry == "8":
                                    new_admin_id = input(
                                        "Name of the manager changes according to the Manager ID. Input Manager ID of desired Manager \n[PRESS ENTER TO RETURN] \n > "
                                    )
                                    os.system("cls||clear")

                                if new_admin_id:
                                    selected_test.admin_id = new_admin_id
                                    selected_test.db_update()

                            elif inquiry == "9":
                                if selected_test.best_score:
                                    selected_test.best_score = False
                                else:
                                    selected_test.best_score = True

                                os.system("cls||clear")
                                selected_test.db_update()

                    else:
                        return None

        elif admin == False:
            if id_num or email:
                if id_num:
                    query = f"{query} WHERE ar.user_id = ?;"
                elif email:
                    query = f"{query} WHERE u.email = ?;"
                rows = cursor.execute(query, (id_num,)).fetchall()
                print(
                    f"{'Test ID':<10}{'Test Name':<40}{'Score':<30}{'Date Taken':<14}{'Acting Admin':<20}{'Best Score':>}"
                )

                for row in rows:
                    row = [str(i) for i in row]
                    print(
                        f"{row[0]:<10}{row[2]:<40}{row[5]:<30}{row[6]:<14}{row[8]:<20}{row[9]:>10}"
                    )
                return None


class Comps:
    def __init__(
        self,
        comp_name,
        test_name,
        date_created,
        comp_id=None,
    ):
        self.comp_id = comp_id
        self.comp_name = comp_name
        self.test_name = test_name
        self.date_created = date_created
        self.attributes = [
            self.comp_name,
            self.test_name,
            self.date_created,
        ]

    def db_update(self):
        self.attributes = [
            self.comp_name,
            self.test_name,
            self.date_created,
            self.comp_id,
        ]

        query = "UPDATE Competency_Assessment_Data SET comp_name = ?, test_name = ?, date_created = ? WHERE comp_id = ?"

        cursor.execute(query, self.attributes)
        connection.commit()


def add_competency():
    comp_name_checkpoint = False
    test_name_checkpoint = False
    validate_checkpoint = False

    while True:
        if comp_name_checkpoint == False:
            comp_name = input(
                "Enter New Competency name (not the name of the test) \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING] \n > "
            )
            os.system("cls||clear")
        if not comp_name:
            return None
        comp_name_checkpoint = True

        if test_name_checkpoint == False:
            test_name = input(
                'Enter name of new test for new competency. (Please note some test names should be specific if they are done differently, for example the "Physical Computer Anatomy Test" is called that because it is a physical test) \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING] \n > '
            )
            os.system("cls||clear")
            if not test_name:
                return None
            test_name_checkpoint = True

        while (
            comp_name_checkpoint == True
            and test_name_checkpoint == True
            and validate_checkpoint == False
        ):
            while True:
                if validate_checkpoint == True:
                    break
                else:
                    validate_info = input(
                        f"Please review information \n [1] Competency Name: {comp_name} \n [2] Test Name: {test_name} \n [Q] Quit to menu without saving \n \nTo make changes to any fields, enter the fields corrisponding number. To enter created test results, press 'ENTER' \n > "
                    )
                    os.system("cls||clear")
                    if not validate_info:
                        validate_checkpoint = True
                        break
                    elif validate_info:
                        if validate_info.upper() == "Q":
                            return None
                        elif validate_info == "1":
                            comp_name_checkpoint = False
                            break
                        elif validate_info == "2":
                            test_name_checkpoint = False
                            break
                        else:
                            wrapper(input_not_recognized)
                            os.system("cls||clear")
                            break
        while validate_checkpoint:
            date_created = str(dt.strftime("%m/%d/%Y"))
            new_competency = Comps(comp_name, test_name, date_created)

            query = "INSERT INTO Competency_Assessment_Data (comp_name, test_name, date_created) VALUES (?,?,?)"

            cursor.execute(query, new_competency.attributes)
            connection.commit()
            return print("Competency has been added")


def get_competency(comp_id):
    query = "SELECT * FROM Competency_Assessment_Data WHERE comp_id = ?"
    (comp_id, comp_name, test_name, date_created) = cursor.execute(
        query, (comp_id,)
    ).fetchone()

    competency = Comps(comp_name, test_name, date_created, comp_id)

    return competency


def view_competencies(comp_id=None):
    os.system("cls||clear")
    query = "SELECT * FROM Competency_Assessment_Data"
    while True:
        if admin == True:
            if not comp_id:
                rows = cursor.execute(query).fetchall()

                print(
                    f"{'Comp ID':<8}{'Competency':<30}{'Test Name':<40}{'Date Added'}"
                )

                for row in rows:
                    row = [str(i) for i in row]
                    print(f"{row[0]:<8}{row[1]:<30}{row[2]:<40}{row[3]}")
                return None
            elif comp_id:
                comp = f"{comp_id}"
                query = f"{query} where comp_id = ?;"
                selected_comp = get_competency(comp_id)
                while True:
                    row = cursor.execute(query, (comp,)).fetchone()
                    connection.commit()
                    os.system("cls||clear")

                    print(
                        f"Comp ID : {row[0]} \n[1] Competency Name: {row[1]} \n[2] Test Name: {row[2]} \n[3] Date Created: {row[3]} \n"
                    )

                    inquiry = input(
                        "To make changes to any information, enter the number of the field. \n[TO RETURN TO MENU PRESS ENTER]\n > "
                    )
                    os.system("cls||clear")
                    inquiry_range = ("1", "2", "3")
                    if inquiry:
                        if inquiry not in inquiry_range:
                            inquiry = None
                            wrapper(input_not_recognized)
                            os.system("cls||clear")
                            continue

                        else:
                            if inquiry == "1":
                                new_comp_name = input(
                                    "Input new name for competency \n[PRESS ENTER TO RETURN] \n > "
                                )
                                os.system("cls||clear")
                                if new_comp_name:
                                    selected_comp.comp_name = new_comp_name
                                    selected_comp.db_update()

                            elif inquiry == "2":
                                new_test_name = input(
                                    "Input new name for test \n[PRESS ENTER TO RETURN] \n > "
                                )
                                os.system("cls||clear")
                                if new_test_name:
                                    selected_comp.test_name = new_test_name
                                    selected_comp.db_update()

                            elif inquiry == "3":
                                new_date = input(
                                    "Input new date \n[PRESS ENTER TO RETURN]\n  (MM/DD/YYYY) \n > "
                                )
                                os.system("cls||clear")
                                if new_date:
                                    selected_comp.date_created = new_date
                                    selected_comp.db_update()
                    else:
                        return None
        else:
            if not comp_id:
                rows = cursor.execute(query).fetchall()

                print(
                    f"{'Comp ID':<8}{'Competency':<30}{'Test Name':<40}{'Date Added to System'}"
                )

                for row in rows:
                    row = [str(i) for i in row]
                    print(f"{row[0]:<8}{row[1]:<30}{row[2]:<40}{row[3]:>20}")
                input("\nPress ENTER to return ")
                return None
            else:
                return print("ERROR: REMOVE COMP_ID AS ADMIN == FALSE")


def competency_summary_reports(summary_comp_id=None, summary_user_id=None):
    query = """SELECT ar.test_id, ar.comp_id, cad.test_name, ar.user_id, u.full_name, ar.score, ar.date_taken, ar.admin_id, m.full_name, ar.best_score
    FROM Assessment_Results ar
    LEFT OUTER JOIN Users u
        ON ar.user_id = u.user_id 
    LEFT OUTER JOIN Users m 
        ON m.user_id = ar.admin_id
    LEFT OUTER JOIN Competency_Assessment_Data cad
        ON cad.comp_id = ar.comp_id"""

    csv_export = False

    while True:
        if csv_export == False:
            if summary_comp_id:
                query = f"{query} WHERE ar.comp_id = ? AND ar.best_score = 1"
                count = 0
                score_count = 0

                rows = cursor.execute(query, (summary_comp_id,))
                description = rows.description
                rows = rows.fetchall()
                print(
                    f"{'Test ID':<8}{'Comp ID':<8}{'Test Name':<40}{'User ID':<8}{'Name':<20}{'Score':<30}{'Date':<11}{'Admin ID':<9}{'Admined By':<20}{'Best Score':>}"
                )

                for row in rows:
                    row = [str(i) for i in row]
                    count += 1
                    score_count += int(row[5][0])
                    print(
                        f"{row[0]:<8}{row[1]:<8}{row[2]:<40}{row[3]:<8}{row[4]:<20}{row[5]:<30}{row[6]:<11}{row[7]:<9}{row[8]:<20}{row[9]:>10}"
                    )
                final_math = score_count / count
                print(
                    f"Summary for all users best scores on competency {summary_comp_id} is {final_math}"
                )
                while admin:
                    inquiry_export = input(
                        "Would you like to export this information to a CSV File? \n [Y]es \n [N]o \n > "
                    )
                    if inquiry_export:
                        if inquiry_export.upper() == "Y":
                            csv_export = True
                            break
                        elif inquiry_export.upper() == "N":
                            return None
                        else:
                            wrapper(input_not_recognized)
                            os.system("cls||clear")
                            continue

            if summary_user_id:
                query = f"{query} WHERE ar.user_id = ? AND ar.best_score = 1;"
                count = 0
                score_count = 0

                rows = cursor.execute(query, (summary_user_id,))
                description = rows.description
                rows = rows.fetchall()
                if admin:
                    print(
                        f"{'Test ID':<8}{'Comp ID':<8}{'Test Name':<40}{'User ID':<8}{'Name':<20}{'Score':<30}{'Date':<11}{'Admin ID':<9}{'Admined By':<20}{'Best Score':>}"
                    )

                    for row in rows:
                        row = [str(i) for i in row]
                        count += 1
                        score_count += int(row[5][0])
                        print(
                            f"{row[0]:<8}{row[1]:<8}{row[2]:<40}{row[3]:<8}{row[4]:<20}{row[5]:<30}{row[6]:<11}{row[7]:<9}{row[8]:<20}{row[9]:>10}"
                        )
                    final_math = score_count / count
                    print(
                        f"Summary for User ID {summary_user_id} with best scores on all competencies is {final_math}"
                    )

                    while admin:
                        inquiry_export = input(
                            "Would you like to export this information to a CSV File? \n [Y]es \n [N]o \n > "
                        )
                        if inquiry_export:
                            if inquiry_export.upper() == "Y":
                                csv_export = True
                                break
                            elif inquiry_export.upper() == "N":
                                return None
                            else:
                                wrapper(input_not_recognized)
                                os.system("cls||clear")
                                continue

                elif admin == False:
                    print(
                        f"{'Test ID':<10}{'Comp ID':<10}{'Test Name':<40}{'Score':<30}{'Date':<15}{'Admined By':<20}{'Best Score':>}"
                    )

                    for row in rows:
                        row = [str(i) for i in row]
                        count += 1
                        score_count += int(row[5][0])
                        print(
                            f"{row[0]:<10}{row[1]:<10}{row[2]:<40}{row[5]:<30}{row[6]:<15}{row[8]:<20}{row[9]:>10}"
                        )
                    print("\n")
                    final_math = score_count / count

                    print(
                        f"Your summary with best scores on all competencies is {final_math} \n"
                    )
                    input("Press ENTER to continue ")
                    return None

        if not csv_export:
            return None
        elif csv_export:
            csv_name = input(
                "Input name for the csv output file \n!!!! RECOMENDATION !!!! \nGive this file a name that is self-explanatory \n > "
            )

            with open(f"{csv_name}.csv", "w", newline="") as csv_output:
                csv_writer = csv.writer(csv_output)
                csv_writer.writerow([i[0] for i in cursor.description])
                csv_writer.writerows(rows)
            break


admin = True

# view_users(20)

# search_users()


# view_test_results(test_id="34")


# add_user()

# add_test_results()

# add_competency()

# view_competencies(17)

# add_test_results()

# view_competencies()

# competency_summary_reports(summary_comp_id=1)

# competency_summary_reports(summary_user_id=21)

# view_test_results(None, 32)


os.system("cls||clear")
while True:
    make_table()
    import_mock_users()
    import_tests(list_of_lists_of_tests)
    import_mock_test_results()
    login_pass = False
    login = input("Enter user email to login \n[PRESS ENTER TO QUIT] \n > ")
    os.system("cls||clear")
    if not login:
        print("Goodbye")
        break
    else:
        try:
            login_user = get_user(None, login)
            if login_user.attributes[7] == False:
                print(
                    "LOGIN FAILED: USER SET AS INACTIVE \nIf you believe this was a mistake, please contact your supervisor \n"
                )
                continue
            if login_user.attributes[4] == "admin":
                admin = True
            else:
                admin = False
        except:
            print("\nERROR: EMAIL NOT FOUND \n")
            continue

        while True:
            pass_check = login_user.pass_check()

            if pass_check == True:
                login_pass = True
                break

            elif pass_check == None:
                break

            elif pass_check == False:
                input(
                    "ERROR: INCORRECT LOGIN INFORMATION. If you forgot your password, please contact your supervisor. \nPRESS ENTER TO RETURN"
                )
                continue
    login_pass = True
    if login_pass:
        loading_bar()
        if admin:
            print(f"Welcome, {login_user.attributes[0]}! \n")

            while True:
                menu_input = input(
                    "[1] View and edit users \n[2] Search for a user by name \n[3] View and edit Assessment Results \n[4] View and edit Competencies \n[5] View and export summary reports \n \n[U]ser Settings \n[S]ign Out \n[Q]uit \n \n > "
                )

                if menu_input:
                    if menu_input.upper() == "Q":
                        os.system("cls||clear")
                        quit("Goodbye")

                    elif menu_input == "1":
                        while True:
                            os.system("cls||clear")
                            view_users()
                            inquiry = input(
                                "\n[A]dd user \nOR To select a user to edit, enter their User ID \n[PRESS ENTER TO RETURN] \n > "
                            )
                            if inquiry:
                                os.system("cls||clear")
                                while True:
                                    if inquiry.upper() == "A":
                                        add_user()
                                        break
                                    else:
                                        try:
                                            view_users(inquiry, None)
                                            break
                                        except TypeError:
                                            wrapper(input_not_recognized)
                                            os.system("cls||clear")

                            else:
                                os.system("cls||clear")
                                break

                    elif menu_input == "2":
                        search_users()
                        os.system("cls||clear")

                    elif menu_input == "3":
                        while True:
                            os.system("cls||clear")
                            view_test_results()
                            inquiry = input(
                                "\nEnter Test ID to edit assessment results \n \n[V]iew tests from a specific user \n[PRESS ENTER TO RETURN] \n > "
                            )
                            if not inquiry:
                                os.system("cls||clear")
                                break
                            elif inquiry.upper() == "V":
                                while True:
                                    os.system("cls||clear")
                                    view_test_results()
                                    inquiry = input(
                                        "Enter Users ID # \n[PRESS ENTER TO RETURN] \n > "
                                    )
                                    if inquiry:
                                        os.system("cls||clear")
                                        view_test_results(inquiry, None)
                                        inquiry = input(
                                            "Enter Test ID to edit assessment results \n[PRESS ENTER TO RETURN] \n > "
                                        )
                                        if inquiry:
                                            view_test_results(None, inquiry)
                                            break
                                        else:
                                            os.system("cls||clear")
                                            break
                                    else:
                                        os.system("cls||clear")
                                        break
                            else:
                                os.system("cls||clear")
                                view_test_results(None, inquiry)

                    elif menu_input == "4":
                        while True:
                            view_competencies()
                            inquiry = input(
                                "\n[A]dd competency \nOR To select a competency to edit, enter Competency ID \n[PRESS ENTER TO RETURN] \n > "
                            )
                            if inquiry:
                                while True:
                                    if inquiry.upper() == "A":
                                        os.system("cls||clear")
                                        add_competency()
                                        break
                                    else:
                                        try:
                                            view_competencies(inquiry)
                                            break
                                        except TypeError:
                                            wrapper(input_not_recognized)
                                        break
                            else:
                                os.system("cls||clear")
                                break

                    elif menu_input == "5":
                        while True:
                            os.system("cls||clear")
                            inquiry = input(
                                "View summary of Assessments based on \n[1] Competency \n[2] User \n[PRESS ENTER TO RETURN] \n > "
                            )
                            os.system("cls||clear")
                            if not inquiry:
                                os.system("cls||clear")
                                break
                            elif inquiry:
                                while True:
                                    if inquiry == "1":
                                        view_competencies()
                                        inquiry = input(
                                            "Input Competency ID for the desired assessmentS \n[PRESS ENTER TO RETURN] \n > "
                                        )
                                        os.system("cls||clear")
                                        if inquiry:
                                            try:
                                                competency_summary_reports(inquiry)
                                            except ZeroDivisionError:
                                                os.system("cls||clear")
                                                input(
                                                    "ERROR: Competencies has no recoreded assessments taken. \n \nPRESS ENTER TO RETURN \n \n"
                                                )
                                                os.system("cls||clear")
                                                break
                                        else:
                                            break
                                    if inquiry == "2":
                                        view_users()
                                        inquiry = input(
                                            "Input User ID for their assessmentS \n[PRESS ENTER TO RETURN] \n > "
                                        )
                                        os.system("cls||clear")
                                        if inquiry:
                                            try:
                                                competency_summary_reports(
                                                    None, inquiry
                                                )
                                            except ZeroDivisionError:
                                                os.system("cls||clear")
                                                input(
                                                    "ERROR: User has no recoreded assessments. \n \nPRESS ENTER TO RETURN \n \n"
                                                )
                                                os.system("cls||clear")
                                                break
                                        else:
                                            break

                    elif menu_input.upper() == "U":
                        os.system("cls||clear")
                        view_users(login_user.attributes[8])

                    elif menu_input.upper() == "S":
                        os.system("cls||clear")
                        inquiry = input(
                            "Are you sure you would like to sign out? \n[Y]es \n[N]o \n > "
                        )
                        if inquiry:
                            if inquiry.upper() == "Y":
                                print("Goodbye!")
                                time.sleep(1)
                                os.system("cls||clear")
                                break
                            elif inquiry.upper() == "N":
                                os.system("cls||clear")
                            else:
                                os.system("cls||clear")
                                wrapper(input_not_recognized)

                    else:
                        os.system("cls||clear")
                        wrapper(input_not_recognized)

        else:
            print(f"Welcome, {login_user.attributes[0]}!", end="\r")
            time.sleep(0.20)
            print("\n")

            while True:
                os.system("cls||clear")
                menu_input = input(
                    "[1] View my Assessments \n[2] View competencies \n[U]ser Settings \n[S]ign Out\n[Q]uit \n > "
                )
                if menu_input:
                    os.system("cls||clear")
                    if menu_input.upper() == "Q":
                        os.system("cls||clear")
                        quit("Goodbye")

                    elif menu_input.upper() == "U":
                        os.system("cls||clear")
                        view_users(login_user.attributes[8])

                    elif menu_input == "1":
                        view_test_results(login_user.attributes[8])
                        inquiry = input(
                            "\n[1] View your summary of all your best assessment scores \n[PRESS ENTER TO RETURN] \n > "
                        )
                        if inquiry:
                            os.system("cls||clear")
                            while True:
                                if inquiry == "1":
                                    competency_summary_reports(
                                        None, login_user.attributes[8]
                                    )
                                    break
                                else:
                                    wrapper(input_not_recognized)
                                    os.system("cls||clear")
                                    break
                        else:
                            os.system("cls||clear")

                    elif menu_input == "2":
                        view_competencies()
                        os.system("cls||clear")

                    elif menu_input.upper() == "S":
                        inquiry = input(
                            "Are you sure you would like to sign out? \n[Y]es \n[N]o \n > "
                        )
                        os.system("cls||clear")
                        if inquiry:
                            if inquiry.upper() == "Y":
                                print("Goodbye!")
                                time.sleep(1)
                                os.system("cls||clear")
                                break
                            elif inquiry.upper() == "N":
                                os.system("cls||clear")
                            else:
                                os.system("cls||clear")
                                wrapper(input_not_recognized)

                    else:
                        os.system("cls||clear")
                        wrapper(input_not_recognized)
