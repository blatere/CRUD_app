import mysql.connector

#opens the database and returns a connection
mysql = mysql.connector.connect(
  host ="localhost",
  user ="root",
  password ="blatere",
  database = "gfg"
)
cursor = mysql.cursor()
#creating table
def create_table(cursor):
    sql = """CREATE TABLE DETAILS (
        Name VARCHAR(20) NOT NULL,
        Email VARCHAR(50),
        Age INT
        )"""
        
    #this function creates a table, we know we'll get an error if we try to create a
    # table that already exists, so we wraps it in a try/except block

    try:
        cursor.execute(sql)
    except:
        pass

#adding new accounts
def add_new_acct(cursor):

    Name = input("Enter name: ")
    Email = input("Enter email: ")
    Age = int(input("Enter age: "))

    sql = """INSERT INTO DETAILS (Name, Email, Age)\
        VALUES(%s, %s, %s)"""
    val = (Name, Email, Age)
    cursor.execute(sql,val)
    print("Record inserted successfully....")

#list users details
def list_acct(cursor):
    sql = """SELECT Name, Email, Age FROM DETAILS"""
    results = cursor.execute(sql)
    users = results.fetchall()
    print("Users details in the database system")
    for user in users:
        print(user[0], '-', user[1], '-', user[2])

#searching for an account
def find_acct(cursor, user):
    sql = """SELECT Name, Email, Agge FROM DETAILS WHERE Name= {user}"""
    sql = sql.format(user = user)
    results = cursor.execute(sql)
    users = cursor.fetchall()
    if len(user) == 0:
        print("Sorry, that user wasn't found!")
    else:
        for user in users:
            print(user[0], '-', user[1], '-', user[2])

#deleting a user
def del_acct(cursor, user):
    sql = """DELETE FROM DETAILS WHERE Name = {user}"""
    sql = sql.format(user=user)
    cursor.execute()

def menu():
    print("What do you want to do?")
    print("A - Add a user")
    print("S - Search for a user")
    print("L - List all users")
    print("D - Delete a user")
    print("Q - Quit")
    choice = input("Choice [A/S/L/Q]: ")
    return choice[0].lower()

#main function for the program, pulling all her functions together.
def main():
    while True:
        choice = menu()
        create_table(cursor)
        if choice == "a":
            add_new_acct(cursor)
        elif choice == "l":
            list_acct(cursor)
        elif choice == "s":
            user = input("Which user? ")
            find_acct(cursor=cursor, user=user)
        elif choice == "d":
            user = input("Which user? ")
            del_acct(cursor=cursor, user=user)
            print("Account deleted successfully..")
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Sorry, that's not valid")
    cursor.commit()
    cursor.close()
if __name__ == '__main__':
    main()
