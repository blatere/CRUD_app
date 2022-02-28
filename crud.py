import mysql.connector
import re
from datetime import datetime


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "fnb_crud"
)

mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    age INT NOT NULL,
    access_time DATETIME)""")



def get_user_id():
    while True:
        try:
            user_id = int(input("\nEnter User ID: "))
        except ValueError:
            print(" Invalid ID type ".center(30, "-"))
        else:
            # break
            mycursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
            myresult = mycursor.fetchone()
            if myresult is None:
                print(f" User ID {user_id} Not Found ".center(30, "*"))
            else:
                # print("Found")
                break

    (user_id, old_name, old_email, old_age, last_access) = myresult
    user = {
        "id": user_id,
        "name": old_name,
        "email": old_email,
        "age": old_age,
        "access_time": last_access
    }

    return user
    


def get_user_name():
    name = input("\nEnter user name: ")
    return name


def get_user_email():
    while True:
        email = input("\nEnter user email: ")
        if re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email) is None:
            print(" Invalid email ".center(30, "-"))
            print(" Please enter a valid email eg - abc@abc.xyz ".center(35, "*"))
        else:
            break

    return email


def get_user_age():
    while True:
        try:
            age = input("\nEnter user\'s age: ")
            if re.match(r"^[0-9]{1,3}$", age) is None:
                raise ValueError
                
        except ValueError:
            print(" Invalid age ".center(30, "-"))
            print(" Please enter a valid age eg - 19 ".center(35, "*"))

            
        else:
            break

    return int(age)



def modify_user_data(user_id, column, value):
    if type(value) == int:
        mycursor.execute(f"UPDATE users SET {column} = {value} WHERE id = {user_id}")
    else:
        mycursor.execute(f"UPDATE users SET {column} = '{value}' WHERE id = {user_id}")
    mydb.commit()
    print(f" Successfully updated User ID: {user_id}\'s {column}")
    print(f" {mycursor.rowcount} record(s) affected".center(30, "-"))




def get_user_details():
    name = get_user_name()
    email = get_user_email()
    age = get_user_age()
    
    
    access_time = None
    # print(name, email, age, access_time)
    user = {
        "name": name,
        "email": email,
        "age": age,
        "access_time": access_time
    }

    return user

def close_conns(mycursor, mydb):
    mycursor.close()
    mydb.close()



#create
def create_user(user):
    print(" Creating user ".center(30, "-"))
    mycursor.execute(f"INSERT INTO users (name, email, age) VALUES ('{user['name']}', '{user['email']}', {user['age']})")
    mydb.commit()
    print(" Created user successfully ".center(30, "-"))
    print(f" {mycursor.rowcount} record added ".center(30, "-"))
    user_id = mycursor.lastrowid
    print(f" User ID: {user_id}, keep safely, as it\'s needed to access user".center(30, "-"))


#read
def access_user():
    # date_format = "%d %b %Y, %I:%M:%S%p"
    date_format = "%d %m %Y, %H:%M:%S"
    user = get_user_id()

    date_str = datetime.now().strftime(date_format)
    date_obj = datetime.strptime(date_str, date_format)
    access_time = date_obj
    # print(myresult)
    # (user_id, name, email, age, last_access) = myresult
    print(f"User {user['id']} Details: ")
    print(f"""
    Name:  {user['name']}
    Email: {user['email']}
    Age:   {user['age']}
    last access time: {access_time}""".center(30, " "))
    

    # mycursor.execute(f"UPDATE users SET access_time = '{access_time}' WHERE id = {user_id}")
    # mydb.commit()
    # print(mycursor.rowcount, "record(s) affected".center(30, "-"))
    modify_user_data(user['id'], "access_time", access_time)

    
#update
def modify_user():
    user = get_user_id()
    # (user_id, old_name, old_email, old_age, last_access) = myresult
    while True:
        choice = int(input("""
        Which user data would you like to modify?
        1) Name
        2) Email
        3) Age
        4) Quit
        Input: """))

        if choice == 1:
            name = get_user_name()
            modify_user_data(user['id'], "name", name)
            print(f" Changed {user['name']} to {name}\n")
            break

        elif choice == 2:
            email = get_user_email()
            modify_user_data(user['id'], "email", email)
            print(f" Changed {user['email']} to {email}\n")
            break

            

        elif choice == 3:
            age = get_user_age()
            modify_user_data(user['id'], "age", age)
            print(f" Changed {user['age']} to {age}\n")
            break

        elif choice == 4:
            break

        else: 
            print(" Invalid Operation ".center(30, "-"))

    
#delete
def remove_user():
    user = get_user_id()
    while True:
        confirm = int(input(f"""
        Are you sure you want to delete User ID {user['id']}?
        1) Yes
        2) No
        Input: """))

        if confirm == 1:
            mycursor.execute(f"DELETE FROM users WHERE id = {user['id']}")
            mydb.commit()
            print(f" Successfully deleted User ID: {user['id']}")
            print(f" {mycursor.rowcount} record(s) affected ".center(30, "-"))
            break



        if confirm == 2:
            break

        else: 
            print(" Invalid operation ".center(30, "-"))

        
def main():
    while True:

        operation = int(input("""
        What operation would you like to perform?
        1) Create User
        2) Access User
        3) Modify User
        4) Delete User
        5) Exit
        Input: """))

        if operation == 1:
            user = get_user_details()
            create_user(user)

        elif operation == 2:
            access_user()

        elif operation == 3:
            modify_user()

        elif operation == 4:
            remove_user()

        elif operation == 5:
            close_conns(mycursor, mydb)
            print("")
            print(" Exiting ".center(30, "-"))
            break

        else:
            print(" Invalid Operation ".center(30, "-"))

if __name__ == "__main__":
    main()
    




