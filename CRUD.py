import mysql.connector
from datetime import datetime

#u see my terminal?


mysqldb = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="",
  database = "fnb_crud"
)

mycursordb = mysqldb.cursor()

 # creating table
studentRecord = """CREATE TABLE STUDENT (
                   NAME  VARCHAR(20) NOT NULL,
                   EMAIL VARCHAR(50),
                   AGE INT
                   )"""


# table created
mycursordb.execute("DROP TABLE IF EXISTS STUDENT")
mycursordb.execute(studentRecord)

while True:
    acct = input("Create user, or quit: ")
    if (acct == "quit"): break
    else:
        try:
            NAME = input("Enter Name: ")
            EMAIL = input("Enter email: ")
            AGE = input("Enter age: ")

            sql = "INSERT INTO STUDENT (NAME, EMAIL, AGE)\
            VALUES (%s, %s, %s)"
            val = (NAME, EMAIL, AGE)

            mycursordb.execute(sql, val)
            mycursordb.commit()

        except:
            mysqldb.rollback()

    print("Record inserted successfully ......")


    access = input("Access user data or quit: ")
    if (access == "quit"): break
    else:
        try:
            query = "SELECT * FROM STUDENT"
            mycursordb.execute(query)
            result = mycursordb.fetchall()
            for x in result:
                NAME = x[0]
                EMAIL = x[1]
                AGE = x[2]
            print(NAME, EMAIL, AGE)

            def print_time():
                time = datetime.now()
                time_template = "Date/time: {M}/{D}/{Y} {H}:{Min}"
                return time_template.format(M=time.month,
                    D=time.day,
                    Y=time.year,
                    H=time.hour,
                    Min=time.minute)

            access_time = print_time()
            print(access_time)
        except:
            print("Error: Unable to fetch data.")

    print("Deleting user datails from database.....")
    try:
        delete = "DELETE FROM STUDENT *"
        mysqldb.commit(delete)
    except:
        mysqldb.rollback()

    print("Record deleted successfully....")

print("Operation terminated...")


mycursordb.close()
