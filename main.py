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
        insert_query = "INSERT INTO Assessment_Results (test_id, comp_id, user_id, score, date_taken, admin_id) VALUES(?, ?, ?, ?, ?, ?);"

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

        query = "UPDATE Users SET full_name = ?, phone = ?, email = ?, hashed_password = ?, user_type = ?, date_created = ?, hire_date = ?, active = ? WHERE user_id = ?;"

        cursor.execute(query, self.attributes)
        connection.commit()

    def pass_check(self, pass_change=None):
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


def search_users():
    name_for_search = input(
        "Enter name you would like to search. \n//Entering name partially will work as long as input is spelt correctly// \n[PRESS ENTER TO RETURN] \n > ")
    if name_for_search:
        while True:
            rows = cursor.execute('SELECT * FROM Users WHERE full_name like ?').fetchall()
            print(
                    f'{"User ID":<9}{"Full name":<19}{"Phone Number":<14}{"email":<31}{"Hashed Password":<18}{"User Type":<12}{"Date Added":<12}{"Hire Date":<12}{"Active":<}'
                )
                for row in rows:
                    row = [str(i) for i in row]
                    print(
                        f"{row[0]:<9}{row[1]:<19}{row[2]:<14}{row[3]:<31}{row[4]:<18}{row[5]:<12}{row[6]:<12}{row[7]:<12}{row[8]:<8}"
                    )
                inquiry = input(
                    "[1] To search again \n[2] To select a specific user above \n[PRESS ENTER TO RETURN] \n > "
                )
                if inquiry:
                    if inquiry == "1":
                        break
                    elif inquiry == "2":
                        inquiry_2 = input("Please enter the Users ID \n > ")
                        return view_users(inquiry_2)
                    else:
                        print("\n !!!!! Input not recognized !!!!! \n")
                else:
                    return None
        else:
            return None


def view_users(id_num=None):
    while True:
        if admin_filter:
            row = cursor.execute(
                "SELECT * FROM Users WHERE user_type = admin"
            ).fetchall()

            print(
                f'{"User ID":<9}{"Full name":<19}{"Phone Number":<14}{"email":<31}{"Hashed Password":<18}{"User Type":<12}{"Date Added":<12}{"Hire Date":<12}{"Active":<}'
            )
            for row in rows:
                row = [str(i) for i in row]
                print(
                    f"{row[0]:<9}{row[1]:<19}{row[2]:<14}{row[3]:<31}{row[4]:<18}{row[5]:<12}{row[6]:<12}{row[7]:<12}{row[8]:<8}"
                )
            return None

        if admin == True:
            if not id_num:
                rows = cursor.execute("SELECT * FROM Users").fetchall()
                print(
                    f'{"User ID":<9}{"Full name":<19}{"Phone Number":<14}{"email":<31}{"Hashed Password":<18}{"User Type":<12}{"Date Added":<12}{"Hire Date":<12}{"Active":<}'
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


class Test_Results:
    def __init__(
        self,
        test_id,
        comp_id,
        user_id,
        score,
        date_taken,
        admin_id,
        best_score=False,
    ):
        self.test_id = test_id
        self.comp_id = comp_id
        self.user_id = user_id
        self.score = score
        self.date_taken = date_taken
        self.admin_id = admin_id
        self.best_score = best_score
        self.attributes = [
            comp_id,
            user_id,
            score,
            date_taken,
            admin_id,
            best_score,
            test_id,
        ]

    def db_test_update(self, check_scores=False):

        query = "UPDATE Assessment_Results SET comp_id = ?, user_id = ?, score = ?, date_taken = ?, admin_id = ?, best_score = ?, WHERE test_id = ?;"

        cursor.execute(query, self.attributes)
        connection.commit()


def add_test_results():
    comp_id_checkpoint = False
    user_id_checkpoint = False
    score_checkpoint = False
    date_checkpoint = False
    admin_checkpoint = False
    best_score_checkpoint = False

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
                    else:
                        if score == "0":
                            score = "0 (No competency- Needs training and direction)"

                        elif score == "1":
                            new_score = "1 (Basic Competency - Needs Ongoing Support)"

                        elif score == "2":
                            score = (
                                "2 (Intermediate Competency - Needs Occasional Support)"
                            )

                        elif score == "3":
                            score = (
                                "3 (Advanced Competency - Completes Task Independently)"
                            )

                        elif score == "4":
                            score = "4 (Expert Competency - Can Effectively pass on this knowledge and can initiate optimizations)"

        if date_checkpoint == False:
            date = input(
                "Input Date test was taken \n[HIT ENTER TO RETURN TO MENU WITHOUT SAVING] \n > "
            )

        if admin_checkpoint == False:
            view_users(admin_filter=True)
            admin_id = input(
                "Input ID Manager that monitored the test \n[IF NO MANAGER MONITORED TEST, HIT ENTER. HOWEVER SOME TESTS LIKE FOR COMPETENCY 1 REQUIRE A MANAGER TO MONITOR TEST] \n > ")
            if not admin_id:
                admin_id = 'N/A'
            elif admin_id:
                

        if best_score_checkpoint == False:
            pass


def get_test(test_id):

    query = "SELECT * FROM Assessment_Results WHERE test_id = ?"

    (
        test_id,
        comp_id,
        user_id,
        score,
        date_taken,
        admin_id,
        best_score,
    ) = cursor.execute(query, (test_id,)).fetchone()

    test = Test_Results(
        test_id,
        comp_id,
        user_id,
        score,
        date_taken,
        admin_id,
        best_score,
    )

    return test


def view_test_results(id_num=None, test_id=None):
        query = """SELECT ar.test_id, ar.comp_id, cad.test_name, ar.user_id, u.full_name, ar.score, ar.date_taken, ar.admin_id, m.full_name, ar.best_score
        FROM Assessment_Results ar
        LEFT OUTER JOIN Users u
            ON ar.user_id = u.user_id 
    LEFT OUTER JOIN Users m 
        ON m.user_id = ar.admin_id
    LEFT OUTER JOIN Competency_Assessment_Data cad
        ON cad.comp_id = ar.comp_id"""
    while True:

        if admin:
            if not test_id:
                    # query = f"{query} ORDER BY ar.test_id;"
                    rows = cursor.execute(
                        query,
                    ).fetchall()
                print(
                    f"{'Test ID':<8}{'Comp ID':<8}{'Test Name':<40}{'User ID':<8}{'Name':<20}{'Score':<7}{'Date':<11}{'Admin ID':<9}{'Admin Name':<15}{'Best Score':<11}"
                )
                for row in rows:
                    row = [str(i) for i in row]
                    print("test")
                        print(
                            f"{row[0]:<8}{row[1]:<8}{row[2]:<40}{row[3]:<8}{row[4]:<20}{row[5]:<7}{row[6]:<11}{row[7]:<9}{row[8]:<15}{row[9]:<11}"
                        )
                    break

                elif test_id:
                    while True:
                        query = """SELECT ar.test_id, ar.comp_id, cad.test_name, ar.user_id, u.full_name, ar.score, ar.date_taken, ar.admin_id, m.full_name, ar.best_score
                        FROM Assessment_Results ar
                        LEFT OUTER JOIN Users u
                            ON ar.user_id = u.user_id 
                    JOIN Competency_Assessment_Data cad
                        ON cad.comp_id = ar.comp_id
                        WHERE ar.test_id = ?"""
                        rows = cursor.execute(query, (id_num,)).fetchall()
                    print(
                        f"{'Test ID':<8}{'Comp ID':<8}{'Test Name':<40}{'User ID':<8}{'Name':<20}{'Score':<7}{'Date':<11}{'Admin ID':<9}{'Admin Name':<15}{'Best Score':<11}"
                    )

                        for row in rows:
                            row = [str(i) for i in row]
                            print(
                            f"{row[0]:<8}{row[1]:<8}{row[2]:<40}{row[3]:<8}{row[4]:<20}{row[5]:<7}{row[6]:<11}{row[7]:<9}{row[8]:<15}{row[9]:<11}"
                        )
                    break

            elif test_id:
                test_id = f"{test_id}"
                selected_test = get_test(test_id)
                query = f"{query} WHERE ar.test_id = ?;"
                while True:
                    print(query)
                    row = cursor.execute(query, (test_id,)).fetchone()
                    connection.commit()
                    print(
                        f"Test ID: {row[0]} \n[1] Competency ID: {row[1]} \n[2] Test Name: {row[2]} \n[3] User ID: {row[3]} \n[4] Name: {row[4]} \n[5] Score: {row[5]} \n[6] Date: {row[6]} \n[7] Manager ID: {row[7]} \n[8] Acting Test Admin (Manager): {row[8]} \n[9] Best Score: {row[9]} \n"
                    )
                    inquiry = input(
                        "To make changes to any information, enter the number of the field. \n[TO GO BACK TO MENU PRESS ENTER]\n > "
                    )
                    if inquiry:

                        if inquiry == "1" or inquiry == '2':
                            print(
                                "//// CHANGES NEED TO BE MADE. SEE NOTES ON LINE 649 ////\n"
                            )
                            # view competencies with their comp_id, comp_name, and test name
                            # prompt admin to input a comp_id and then according to that, change the info of the test result to state the competency id and test name

                            if inquiry == "1":
                                new_comp = input(
                                    "Input new competency ID \n[PRESS ENTER TO RETURN] \n > "
                                )

                            # view competencies with their comp_id, comp_name, and test name
                            new_comp = input(
                                "Test Name changes according to Competency ID number. To change Test Name, input Competency ID of the desired Test Name \n[PRESS ENTER TO RETURN] \n >"
                            )
                            if new_comp:
                                selected_test.comp_id = new_comp
                                selected_test.db_update()

                        elif inquiry == "3" or inquiry =='4':
                            if inquiry == '3':
                                new_user_id = input(
                                    "Input User ID of desired User \n[PRESS ENTER TO RETURN] \n > "
                                )

                            elif inquiry == "4":
                            pass
                        elif inquiry == "5":
                            pass
                        elif inquiry == "6":
                            pass
                        elif inquiry == "7":
                            pass
                        elif inquiry == "8":
                                new_admin_id = input(
                                    "Name of the manager changes according to the Manager ID. Input Manager ID of desired Manager \n[PRESS ENTER TO RETURN] \n > "
                                )

                            if new_admin_id:
                                selected_test.admin_id = new_admin_id
                                selected_test.db_test_update()

                        elif inquiry == "9":
                            pass
                        else:
                            inquiry = input(
                                "Input not recognized. Please enter corrisponding number to field you would like to make changes to \n[PRESS ENTER TO RETURN] \n > "
                            )

                    else:
                        return None

        else:
            pass


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

def get_competency(comp_id):
    query = "SELECT * FROM Competency_Assessment_Data WHERE test_id = ?"
    (comp_id, comp_name, test_name, date_created) = cursor.execute(
        query, (comp_id,)
    ).fetchone()

    competency = Comps(comp_name, test_name, date_created, comp_id)

    return competency


def view_competencies(comp_id=None):
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
        else:
            pass


make_table()


import_mock_users()


import_tests(list_of_lists_of_tests)

import_mock_test_results()


admin = True
# view_users("14")

# search_users()

view_test_results()

# while True:
#     if admin == True:
#         pass
