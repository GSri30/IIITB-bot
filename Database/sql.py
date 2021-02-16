#os
import os
#sql
#sqlite
import sqlite3
from sqlite3.dbapi2 import Cursor, Error
#mysql
import mysql.connector
#encryption
from Bcrypt import Bcrypt
#settings
from settings import DATABASE_PATH,EXCEL_PATH,DEVELOPMENT,DELTA_YEAR
#secrets
from secret import MYSQL_DATABASE,MYSQL_HOST,MYSQL_ROOT_USER,MYSQL_ROOT_PASSWORD,MYSQL_USER,MYSQL_PASSWORD,PRODUCTION

#SQL class which contains various methods for database management
class SQL:
    def __init__(self,conn=None):
        self.conn=conn

    def init(self):
        self.Connect()
        self.CreateTable()
        self.Close()

    # Connect to sql (Either mysql or sqlite) and establish a connection
    def Connect(self,databasepath:str=DATABASE_PATH):
        try:
            if ((PRODUCTION is not None and PRODUCTION=='True') or (not DEVELOPMENT)):
                print("Using mysql")
                self.marker='%s'
                conn=mysql.connector.connect(
                    host=MYSQL_HOST,
                    user=MYSQL_ROOT_USER,
                    password=MYSQL_ROOT_PASSWORD,
                )
                cursor=conn.cursor()
                cursor.execute("SET GLOBAL sql_mode=''")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE}")
                cursor.execute(f"USE {MYSQL_DATABASE}")
                cursor.close()
            else:
                print("Using sqlite")
                self.marker='?'
                conn=sqlite3.connect(databasepath)

            self.conn=conn

            return True
        except Error:
            print(Error)
            return False

    # Create a table (if not exists)
    def CreateTable(self):
        cursor=self.conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS STUDENTS
                            (   ID INTEGER PRIMARY KEY,
                                USER TEXT,
                                DISCORDID TEXT,
                                EMAIL TEXT NOT NULL,
                                BATCH TEXT NOT NULL,
                                VERIFIED INT,
                                REGISTRATION_YEAR TEXT,
                                DISCORDHASH TEXT NOT NULL
                            );
                            ''')

        self.conn.commit()
        cursor.close()
        

    # Add a user into the database (register)
    def AddUser(self,email:str,batch:str,regyear:str,discordhash:str):
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f'''INSERT INTO STUDENTS (EMAIL,BATCH,VERIFIED,REGISTRATION_YEAR,DISCORDHASH)\
                                VALUES ({self.marker},{self.marker},0,{self.marker},{self.marker})
                            ''',(email,batch,regyear,discordhash))
            self.conn.commit()
            cursor.close()

    # Get batch to which a user belongs to from email
    def getBatch(self,email:str):
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"SELECT * FROM STUDENTS WHERE EMAIL = {self.marker}",(email,))
            results=cursor.fetchall()
            cursor.close()
            if results:
                return results[0][4]
            return None
        return False

    # Remove all users whose registration year and current year difference is below 'DELTA_YEAR'
    def filterOldAlumni(self,curryear:str):
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"SELECT * FROM STUDENTS WHERE REGISTRATION_YEAR <= {curryear-DELTA_YEAR}")
            results=cursor.fetchall()
            cursor.execute(f"DELETE FROM STUDENTS WHERE REGISTRATION_YEAR <= {curryear-DELTA_YEAR}")
            cursor.close()
            return [row[2] for row in results]
        return False

    # Check if a user with specified email exists or not
    def isPresent(self,email:str):
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"SELECT * FROM STUDENTS WHERE EMAIL = {self.marker}",(email,))
            results=cursor.fetchall()
            cursor.close()
            return len(results)>0
        return False

    # Check if a user with specified discord ID and email ID is verified
    def isVerified(self,memberID:str,mailID:str):
        if self.conn is not None:
            cursor=self.conn.cursor()
            if mailID is None:
                cursor.execute(f"SELECT * FROM STUDENTS WHERE DISCORDID = {self.marker}",(memberID,))    
            if memberID is None:
                cursor.execute(f"SELECT * FROM STUDENTS WHERE EMAIL = {self.marker}",(mailID,))
            
            results=cursor.fetchall()
            cursor.close()

            if results:
                for student in results:
                    if student[5]:
                        return True

        return False


    # Remove a user using either mail ID or Discord ID
    def RemoveUser(self,mailID:str=None,memberID:str=None):
        if self.conn is not None:
            cursor=self.conn.cursor()
            if mailID:
                cursor.execute(f"DELETE FROM STUDENTS WHERE EMAIL = {self.marker}",(mailID,))
            if memberID:
                cursor.execute(f"DELETE FROM STUDENTS WHERE DISCORDID = {self.marker}",(memberID,))
            self.conn.commit()
            cursor.close()


    # Update a user mail ID
    def UpdateEmail(self):
        pass

    # Verify a user using the provided Key and map the discord ID with email ID if its a match
    def VerifyUser(self,memberName:str,memberID:str,mailID:str,key:str):
        Found=False
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"SELECT * FROM STUDENTS WHERE EMAIL = {self.marker}",(mailID,))
            results=cursor.fetchall()
            if results is not None:
                for member in results:
                    FoundHash=member[7]
                    if Bcrypt.Match(str(key),FoundHash):
                        cursor.execute(f"UPDATE STUDENTS SET  USER = {self.marker}, DISCORDID = {self.marker}, VERIFIED = 1  WHERE EMAIL = {self.marker} AND DISCORDHASH = {self.marker}",(memberName,memberID,mailID,FoundHash))
                        self.conn.commit()
                        Found=True
                        break
            cursor.close()
        return Found
        

    # Remove all the unverified users
    def RemoveUnverified(self):
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"SELECT DISCORDID FROM STUDENTS WHERE VERIFIED = 0")
            results=cursor.fetchall()
            cursor.execute(f"DELETE FROM STUDENTS WHERE VERIFIED = 0")
            self.conn.commit()
            cursor.close()
            return results
        return None
    
    #! Empty the entire DB
    def EmptyDB(self):
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"DELETE FROM STUDENTS")
            self.conn.commit()
            cursor.close()
            print("Emptied the database successfully!")
            
    # Generate a CSV from the DB
    def GenerateCSV(self,excelpath:str=EXCEL_PATH):
        if self.conn is not None:
            with open(excelpath,"a") as f:
                cursor=self.conn.cursor()
                cursor.execute(f"SELECT * FROM STUDENTS")
                Students=cursor.fetchall()
                f.write(f"S.No;Student;DiscordID;Email;Batch;isVerified;VerificationYear;UniqueHash\n")
                if Students is not None:
                    for student in Students:
                        f.write(f"{student[0]};{student[1]};'{student[2]}';{student[3]};{student[4]};{student[5]};{student[6]};{student[7]}\n")
                cursor.close()
            return True
        return False
    
    # Delete the generated CSV
    def DeleteCSV(self,excelpath:str=EXCEL_PATH):
        if os.path.exists(excelpath):
            os.remove(excelpath)
            
    # Print the DB (Helper function)
    def PrintDB(self):
        if self.conn is not None:
            cursor=self.conn.cursor()
            students=cursor.execute(f"SELECT * FROM STUDENTS")
            for student in students:
                print(f"{student[0]} {student[1]} {student[2]} {student[3]} {student[4]} {student[5]} {student[6]} {student[7]}")
            cursor.close()

    # Close the connection
    def Close(self):
        if self.conn is not None:
            self.conn.close()