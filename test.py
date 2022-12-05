# "Computer Anatomy+Physical Computer Anatomy Test", "Data Types+Data Types Exam", "Variables+Variables Exam", "Functions+Functions Exam", "Boolean Logic+Building Block Boolean Logic Test", "Conditionals+Physical Conditionls Test", "Loops+Fruit Loops Test", "Data Structures+Data Structures Competency Measurement", "Lists+List Exam", "Dictionaries+Dictionaries Exam", "Working with Files+Working with Files Competency Exam", "Exception Handling+Exception Handling Exam", "Quality Assurance QA+Physical QA Exam", "Object-Oriented Programming+OOP Exam", "Recursion+Recursion Exam", "Databases+Databases Exam"


class User:
    def __init__(self, first, last, password, email):
        self.first_name = first
        self.last_last = last
        self.password = password
        self.email = email
        self.active = True

        self.attributes = (
            self.first_name,
            self.last_last,
            self.password,
            self.email,
            self.active,
        )

    def change_password(self, newpassword):
        self.password = newpassword
        print("Password Changed")


first_name = "James"
last_last = "Hales"
password = "sekret"
email = "fake@email.com"

my_user = User(first_name, last_last, password, email)

# print(my_user.password)

# new_pass = input("New pass: ")
# my_user.change_password(new_pass)

# print(my_user.password)

# # ------------------

print(
    f" Prints in a list/touple (depending on what type of brackets the perameters of self.attributes are surrounded by): \n{my_user.attributes}"
)

# # this will print it out in a list
print("\nPrints pretty like, with everything on their own line")
for attr in my_user.attributes:
    print(attr)


def pass_encryption(no_pass=None):
    salt = bcrypt.gensalt()
    if no_pass:
        while True:
            new_pass = input("No password found. Please enter first password \n > ")
            new_pass = new_pass.encode()
            check_pass = input("Confirm new password \n > ")
            check_pass = check_pass.encode()
            check_match = bcrypt.checkpw(new_pass, check_pass)
            if check_match == False:
                print("Passwords do not match. Please try again")
                continue
            else:
                break

    else:
        pass_check = input("Input current password \n (PRESS ENTER TO RETURN) \n > ")
        pass_check = pass_check.encode()
        while True:
            if pass_check:
                encoded_pass_check = row[4].encode()
                password_matches = bcrypt.checkpw(pass_check, encoded_pass_check)
                print(password_matches)
                if password_matches == True:
                    new_pass = input(
                        "Please input new password \n(PRESS ENTER TO RETURN) \n > "
                    )
                    if new_pass:
                        check_password = input(
                            "Type in the same password \n(PRESS ENTER TO RETURN) \n > "
                        )
                        if check_password:
                            if new_pass == check_password:
                                print("Password changed")
                                encoded_pass = new_pass.encode()
                                break
                            elif new_pass != check_password:
                                print("New passwords do not match \n")
                                continue
                        else:
                            return None
                    else:
                        return None
                else:
                    pass_check = input(
                        "Incorrect password. Please input correct password. \n (PRESS ENTER TO RETURN) \n > "
                    )
                    continue
            else:
                return None
    hashed_password = bcrypt.hashpw(encoded_pass, salt)
    hashed_password = hashed_password.decode()
    update_query = "UPDATE Users SET hashed_password = ? WHERE user_id = ?"
    values = (hashed_password, user_id)
    cursor.execute(update_query, values)
    connection.commit()

    def pass_check(self, id_num):
        selected_user = get_user(id_num)
        salt = bcrypt.gensalt()
        if self.attributes[3]:
            while True:
                current_pass = self.attributes[3]
                pass_check = input(
                    "Input current password \n[PRESS ENTER TO RETURN] \n > "
                )
                pass_check = pass_check.encode()
                if pass_check:
                    encoded_pass = current_pass.encode()
                    password_matches = bcrypt.checkpw(pass_check, encoded_pass)
                    if password_matches == True:
                        return True
                    else:
                        print("Password incorrect")
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
                        new_pass = bcrypt.hashpw(confirm_pass, salt)
                        new_pass = new_pass.decode()
                        selected_user.hashed_password = new_pass
                        selected_user.db_update()
                        return False
                else:
                    return None
