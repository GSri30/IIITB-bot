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
from settings import DATABASE_PATH,EXCEL_PATH
#secrets
from dotenv import load_dotenv

load_dotenv()
DEVELOPMENT=os.getenv("DEVELOPMENT")


MYSQL_USER=os.getenv("MYSQL_USER")
MYSQL_ROOT_PASSWORD=os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")

MYSQL_HOST=os.getenv("MYSQL_HOST")
MYSQL_DATABASE=os.getenv("MYSQL_DATABASE")



#SQL class which contains various methods for database management
class SQL:
    def __init__(self,conn=None):
        self.conn=conn

    def init(self):
        self.Connect()
        self.CreateTable()
        self.Close()

    def Connect(self,databasepath:str=DATABASE_PATH):
        try:
            if (DEVELOPMENT == "OFF") and MYSQL_USER and MYSQL_ROOT_PASSWORD and MYSQL_PASSWORD and MYSQL_HOST and MYSQL_DATABASE:
                print("Using mysql")
                conn=mysql.connector.connect(
                    host=MYSQL_HOST,
                    user=MYSQL_USER,
                    password=MYSQL_ROOT_PASSWORD
                )
            else:
                print("Using sqlite")
                conn=sqlite3.connect(databasepath)

            self.conn=conn
            
            return True
        except Error:
            print(Error)
            return False

    # Remove
    # def CheckTableExists(self,tablename:str):
    #     cursor=self.conn.cursor()
    #     cursor.execute("""
    #                 SELECT name
    #                 FROM sqlite_master
    #                 WHERE type = 'table' AND 
    #                 name NOT LIKE 'sqlite_%';
    #                 """)
    #     existingtables=cursor.fetchone()
    #     if existingtables is None:
    #         print("Didn't find the required table.")
    #         cursor.close()
    #         return False
        
    #     if tablename in existingtables:
    #         cursor.close()
    #         return True

    #     cursor.close()
    #     return False

    # Remove
    # def CreateTable(self):
    #     cursor=self.conn.cursor()
    #     if not self.CheckTableExists("STUDENTS"):
    #         cursor.execute(f'''CREATE TABLE STUDENTS
    #                         (   ID INTEGER PRIMARY KEY,
    #                             USER TEXT,
    #                             DISCORDID TEXT,
    #                             EMAIL TEXT NOT NULL,
    #                             VERIFIED INT,
    #                             DISCORDHASH TEXT NOT NULL
    #                         );
    #                         ''')
    #         self.conn.commit()
    #         print("Table created successfully")
    #     else:
    #         print("Using existing table.")
    #     cursor.close()

    def CreateTable(self):
        cursor=self.conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS STUDENTS
                            (   ID INTEGER PRIMARY KEY,
                                USER TEXT,
                                DISCORDID TEXT,
                                EMAIL TEXT NOT NULL,
                                BATCH TEXT NOT NULL,
                                VERIFIED INT,
                                DISCORDHASH TEXT NOT NULL
                            );
                            ''')
        self.conn.commit()
        cursor.close()
        

    def AddUser(self,email:str,batch:str,discordhash:str):
        if self.conn is not None:
            self.conn.execute(f'''INSERT INTO STUDENTS (EMAIL,BATCH,VERIFIED,DISCORDHASH)\
                                VALUES (?,?,0,?)
                            ''',(email,batch,discordhash))
            self.conn.commit()

    def getBatch(self,email:str):
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"SELECT * FROM STUDENTS WHERE EMAIL = ?",(email,))
            results=cursor.fetchall()
            cursor.close()
            return results[0][4]
        return False


    def isPresent(self,email:str):
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"SELECT * FROM STUDENTS WHERE EMAIL = ?",(email,))
            results=cursor.fetchall()
            cursor.close()
            return len(results)>0
        return False

    def isVerified(self,memberID:str,mailID:str):
        if self.conn is not None:
            cursor=self.conn.cursor()
            if mailID is None:
                cursor.execute(f"SELECT * FROM STUDENTS WHERE DISCORDID = ?",(memberID,))    
            if memberID is None:
                cursor.execute(f"SELECT * FROM STUDENTS WHERE EMAIL = ?",(mailID,))
            
            results=cursor.fetchall()
            cursor.close()

            if results:
                for student in results:
                    if student[5]:
                        return True

        return False


    def RemoveUser(self,mailID:str=None,memberID:str=None):
        if self.conn is not None:
            cursor=self.conn.cursor()
            if mailID:
                cursor.execute(f"DELETE FROM STUDENTS WHERE EMAIL = ?",(mailID,))
            if memberID:
                cursor.execute(f"DELETE FROM STUDENTS WHERE DISCORDID = ?",(memberID,))
            self.conn.commit()
            cursor.close()


    def UpdateEmail(self):
        pass

    def VerifyUser(self,memberName:str,memberID:str,mailID:str,key:str):
        Found=False
        if self.conn is not None:
            cursor=self.conn.cursor()
            cursor.execute(f"SELECT * FROM STUDENTS WHERE EMAIL = ?",(mailID,))
            results=cursor.fetchall()
            if results is not None:
                for member in results:
                    FoundHash=member[6]
                    if Bcrypt.Match(key,FoundHash):
                        cursor.execute(f"UPDATE STUDENTS SET  USER = ?, DISCORDID = ?, VERIFIED = 1  WHERE EMAIL = ? AND DISCORDHASH = ?",(memberName,memberID,mailID,FoundHash))
                        self.conn.commit()
                        Found=True
                        break
            cursor.close()
        return Found
        

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
    
    def EmptyDB(self):
        if self.conn is not None:
            self.conn.execute(f"DELETE FROM STUDENTS")
            self.conn.commit()
            print("Emptied the database successfully!")
            

    def GenerateCSV(self,excelpath:str=EXCEL_PATH):
        if self.conn is not None:
            with open(excelpath,"a") as f:
                Students=self.conn.execute(f"SELECT * FROM STUDENTS")
                f.write(f"S.No;Student;DiscordID;Email;Batch;isVerified;UniqueHash\n")
                for student in Students:
                    f.write(f"{student[0]};{student[1]};'{student[2]}';{student[3]};{student[4]};{student[5]};{student[6]}\n")
            return True
        return False
    

    def DeleteCSV(self,excelpath:str=EXCEL_PATH):
        if os.path.exists(excelpath):
            os.remove(excelpath)
            

    def PrintDB(self):
        if self.conn is not None:
            students=self.conn.execute(f"SELECT * FROM STUDENTS")
            for student in students:
                print(f"{student[0]} {student[1]} {student[2]} {student[3]} {student[4]} {student[5]} {student[6]}")

    def Close(self):
        if self.conn is not None:
            self.conn.close()