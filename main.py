import sqlite3
import bcrypt
import csv
from datetime import datetime

connection = sqlite3.connect("assessments.db")
cursor = connection.cursor()

admin = False


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
        return print("\n !!!!!!!!!! MOCK USERS ALREADY ADDED !!!!!!!!!! \n")


def import_tests(test_list):
    try:
        with open("import_tests.csv", "w", newline="") as writing_csv:
            writer = csv.writer(writing_csv)
            writer.writerow(["comp_name", "test_name", "date_created"])
            for data in test_list:
                writer.writerow(data)

        insert_query = "INSERT INTO Competency_Assessment_Data (comp_name, test_name, date_created) VALUES(?, ?, ?);"

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
        # print("\n !!!!!!!!!! TESTS ALREADY ADDED !!!!!!!!!! \n")


list_of_lists_of_tests = [
    ["Computer Anatomy", "Physical Computer Anatomy Test", str(datetime.now())],
    ["Data Types", "Data Types Exam", str(datetime.now())],
    ["Variables", "Variables Exam", str(datetime.now())],
    ["Functions", "Functions Exam", str(datetime.now())],
    ["Boolean Logic", "Building Block Boolean Logic Test", str(datetime.now())],
    ["Conditionals", "Physical Conditionls Test", str(datetime.now())],
    ["Loops", "Fruit Loops Test", str(datetime.now())],
    ["Data Structures", "Data Structures Competency Measurement", str(datetime.now())],
    ["Lists", "List Exam", str(datetime.now())],
    ["Dictionaries", "Dictionaries Exam", str(datetime.now())],
    ["Working with Files", "Working with Files Competency Exam", str(datetime.now())],
    ["Exception Handling", "Exception Handling Exam", str(datetime.now())],
    ["Quality Assurance (QA)", "Physical QA Exam", str(datetime.now())],
    ["Object-Oriented Programming", "OOP Exam", str(datetime.now())],
    ["Recursion", "Recursion Exam", str(datetime.now())],
    ["Databases", "Databases Exam", str(datetime.now())],
]


def import_mock_test_results():
    try:
        insert_query = "INSERT INTO Assessment_Results (test_id, user_id, competency, assessment, score, date_taken, admined_by) VALUES(?, ?, ?, ?, ?, ?, ?);"

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
        return print("\n !!!!!!!!!! MOCK TEST RESULTS ALREADY ADDED !!!!!!!!!! \n")


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
        self.attributes = (
            self.name,
            self.phone,
            self.email,
            self.hashed_password,
            self.date_created,
            self.hire_date,
            self.active,
            self.id,
        )

    def db_update(self, pass_edit=None):

        query = "UPDATE Users SET full_name = ?, phone = ?, email = ?, hashed_password = ?, user_type = ?, date_created = ?, hire_date = ?, active = ? WHERE user_id = ?;"

        cursor.execute(query, self.attributes)
        print(self.id)
        connection.commit()

    def pass_check(self, id, pass_change=None):
        first_pass = False
        new_password = False
        selected_user = get_user(id)
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
                        password_matches = bcrypt.checkpw(new_pass, confirm_pass)
                        if password_matches == True:
                            new_password == True
                            break
                        else:
                            continue
                    else:
                        return None

        elif not self.attributes[3]:
            while True:
                new_pass = input(
                    "Password not found. Please enter first passwword \n[PRESS ENTER TO RETURN] \n > "
                )
                if new_pass:
                    new_pass = new_pass.encode()
                    confirm_pass = input("Confirm first password \n > ")
                    confirm_pass = confirm_pass.encode()
                    password_matches = bcrypt.checkpw(new_pass, confirm_pass)
                    if password_matches == True:
                        first_pass = True
                        break
                else:
                    return None

        new_pass = bcrypt.hashpw(confirm_pass, salt)
        new_pass = new_pass.decode()
        selected_user.hashed_password = new_pass
        selected_user.db_update()

        if new_password == True:
            return print("\n ///// Password has been changed ///// \n")

        if first_pass == True:
            print("\n ///// First password has been created ///// \n")
            return True


def add_user():
    name_checkpoint = False
    phone_checkpoint = False
    email_checkpoint = False
    date_checkpoint = False
    valid_checkpoint = False

    while True:
        if name_checkpoint == False:
            full_name = input("Enter new users full name (first and last): \n > ")
            if not full_name:
                full_name = input(
                    "Full name is required to add a new user. Please add in full name of new user: \n[TO GO BACK TO MENU WITHOUT SAVING, HIT ENTER] \n > "
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
            email = input("Enter users email: \n > ")
            if email:
                print(
                    "!!!!! REMINDER !!!!! \nEmail entered, please remind user they can create the password to their login when they first login \n"
                )
            elif not email:
                email = input(
                    "Email is required for user login. Please enter users email: \n[TO GO BACK TO MENU WITHOUT SAVING, HIT ENTER] \n > "
                )
                if not email:
                    return None
            email_checkpoint = True

        if date_checkpoint == False:
            hire_date = input("Please enter users hire date: \n  (MM\DD\YY) \n > ")
            if not hire_date:
                hire_date = input(
                    'Hire date is required. Hire date is the day the user had completed their paper work (Form W-4, Form I-9, state forms, and other payroll withholding forms) \nIf Hire date is currently unkown, undecided, or the information is currently unavailable at this time, please enter "N/A" \n[TO QUIT TO THE MENU WITHOUT SAVING, HIT ENTER] \n > '
                )
                if hire_date.upper() == "N/A" or hire_date.upper() == "N\A":
                    hire_date = "INFO REQUIRED"
                if not hire_date:
                    return None
            date_checkpoint = True

        while (
            name_checkpoint
            and phone_checkpoint
            and email_checkpoint
            and date_checkpoint
        ):
            validate_info = input(
                f'Please validate the following information has been entered correctly. \n[1] Full name: {full_name} \n[2] Phone: {phone} \n[3] Email: {email} \n[4] Hire date: {hire_date} \n \nIf all entered information is correct, please hit "ENTER" \nIf any information is incorrect, please enter the corrisponding number to the field that requires changing. \nTo quit without saving any information, please enter "Q" \n > '
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
                    break
            else:
                valid_checkpoint = True

                break

        while valid_checkpoint == True:
            date_created = str(datetime.now())
            new_user = Users(full_name, phone, email, hire_date, date_created)

            query = "INSERT INTO Users (full_name, phone, email, hashed_password, date_created, hire_date, active) VALUES (?,?,?,?,?,?,?)"

            cursor.execute(query, new_user.attributes)
            connection.commit()
            return print("User added")


def get_user(user_id):

    query = "SELECT * FROM Users WHERE user_id = ?"

    (
        id,
        name,
        phone,
        email,
        hashed_password,
        user_type,
        date_created,
        hire_date,
        active,
    ) = cursor.execute(query, (user_id,)).fetchone()

    user = Users(
        name,
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


def view_users(id_num=None):
    while True:
        if admin == True:
            if not id_num:
                rows = cursor.execute("SELECT * FROM Users").fetchall()
                print(
                    f'{"User ID":<9}{"full_name":<19}{"Phone Number":<14}{"email":<31}{"Hashed Password":<18}{"User Type":<12}{"Date Added":<12}{"Hire Date":<12}{"Active":<}'
                )
                for row in rows:
                    row = [str(i) for i in row]
                    print(
                        f"{row[0]:<9}{row[1]:<19}{row[2]:<14}{row[3]:<31}{row[4]:<18}{row[5]:<12}{row[6]:<12}{row[7]:<12}{row[8]:<8}"
                    )
                    return None
            elif id_num:
                id_num = f"{id_num}"
                selected_user = get_user(id_num)
                while True:
                    row = cursor.execute(
                        "SELECT * FROM Users WHERE user_id = ?", (id_num,)
                    ).fetchone()
                    print(
                        f"{'User ID: '} {row[0]} \n{'[1] Name: '} {row[1]} \n{'[2] Phone: '} {row[2]} \n{'[3] Email: '}{row[3]} \n{'[4] Hashed Password: '} {row[4]} \n{'[5] User Type: '} {row[5]} \n{'[6] Date Created: '} {row[6]} \n{'[7] Hire Date: '} {row[7]} \n{'[8] Active: '} {row[8]} \n"
                    )

                    inquiry = input(
                        "To make changes to any information, enter the number of the field. \n[TO GO BACK TO MENU PRESS ENTER]\n > "
                    )
                    if inquiry:
                        if inquiry == "1":
                            name_change = input(
                                "Enter new full name for User \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n > "
                            )
                            if name_change:
                                selected_user.name = name_change
                                selected_user.db_update()

                        elif inquiry == "2":
                            phone_change = input(
                                "Enter new phone number for User \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n[###-###-####] \n > "
                            )
                            if phone_change:
                                selected_user.phone = phone_change
                                selected_user.db_update()

                        elif inquiry == "3":
                            email_change = input(
                                "Enter new email for User \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n > "
                            )
                            if email_change:
                                selected_user.email = email_change
                                selected_user.db_update()

                        elif inquiry == "4":
                            Users.pass_check(id_num, pass_change=True)

                        elif inquiry == "5":
                            if selected_user.user_type == "user":
                                selected_user.user_type = "admin"
                            else:
                                selected_user.user_type = "user"
                            selected_user.db_update()

                        elif inquiry == "6":
                            validate_change = input(
                                "!!!!! WARNING !!!!! \nCreated date represents when user was added into the system. Changing this requires supervisor permission! \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \nTo make changes, enter new created date for User \n  (MM/DD/YYYY) \n > "
                            )
                            if validate_change:
                                selected_user.date_created = validate_change
                                selected_user.date_created
                                selected_user.db_update()

                        elif inquiry == "7":
                            validate_change = input(
                                "!!!!! WARNING, HIRE DATE HAS BEEN SELECTED FOR CHANGE !!!!! \nHire date represents the date user has submitted legal forms (Form W-4, Form I-9, state forms, and other payroll withholding forms) \nMAKING THIS CHANGE REQUIRES SUPERVISOR PERMISSION \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \nTo make changes to Hire Date, enter new hire date for User \n  (MM/DD/YYYY) \n >  "
                            )
                            if validate_change:
                                selected_user.hire_date = validate_change
                                selected_user.hire_date
                                selected_user.db_update()

                        elif inquiry == "8":
                            if selected_user.active:
                                selected_user.active = False
                            else:
                                selected_user.active = True
                            selected_user.active
                            selected_user.db_update()

                        else:
                            inquiry = input(
                                "Input not recognized. Please enter the corrisponding number to the field you would like changes to. \n[TO GO BACK TO MENU PRESS ENTER]\n > "
                            )
                    else:
                        return None

        elif admin == False:
            id_num = f"{id_num}"
            selected_user = get_user(id_num)
            while True:
                row = cursor.execute(
                    "SELECT * FROM Users WHERE user_id = ?", (id_num,)
                ).fetchone()

                print(
                    f"\n{'Name: '} {row[1]} \n{'Phone: '} {row[2]} \n{'Email: '}{row[3]} \n{'Hashed Password: '} {row[4]}\n{'Hire Date: '} {row[7]} \n"
                )

                inquiry = input(
                    "[1] Change full name (first and last) \n[2] Change Phone \n[3] Change password \n[TO GO BACK TO MENU PRESS ENTER] \n \n(FOR OTHER INFORMATION THAT YOU WISH TO BE CHANGED, PLEASE SPEAK WITH A SUPERVISOR) \n > "
                )

                if inquiry:
                    if inquiry == "1":
                        new_name = input(
                            "Enter your new Full Name \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n > "
                        )
                        if new_name:
                            selected_user.name = new_name
                            selected_user.db_update()
                    elif inquiry == "2":
                        new_phone = input(
                            "Enter your new phone number \n[ONLY PRESS ENTER TO GO BACK AND NOT MAKE CHANGES] \n > "
                        )
                        if new_phone:
                            selected_user.phone = new_phone
                            selected_user.db_update()
                    elif inquiry == "3":
                        pass
                else:
                    return None


make_table()


import_mock_users()


import_tests(list_of_lists_of_tests)

import_mock_test_results()


# add_user()

admin = True
view_users("14")
