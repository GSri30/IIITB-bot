import os
from pathlib import Path
import sqlite3
from sqlite3.dbapi2 import Error

from settings import DATABASE_PATH,EXCEL_PATH

class SQLite:
    def __init__(self,conn=None):
        self.conn=conn

    def init(self):
        self.Connect()
        self.CreateTable()
        self.Close()

    def Connect(self,databasepath:str=DATABASE_PATH):
        try:
            conn=sqlite3.connect(databasepath)
            self.conn=conn
            return True
        except Error:
            print(Error)
            return False

    def CreateTable(self):
        cursor=self.conn.cursor()
        cursor.execute(f'''CREATE TABLE STUDENTS
                        (   ID INTEGER PRIMARY KEY,
                            USER TEXT NOT NULL,
                            DISCORDID TEXT NOT NULL,
                            EMAIL TEXT NOT NULL,
                            VERIFIED INT,
                            DISCORDHASH TEXT
                        );
                        ''')
        self.conn.commit()
        print("Table created successfully")

    def AddStudent(self,user:str,discordid:str,email:str,discordhash:str):
        if self.conn is not None:
            self.conn.execute(f'''INSERT INTO STUDENTS (USER,DISCORDID,EMAIL,VERIFIED,DISCORDHASH)\
                                VALUES ("{user}","{discordid}","{email}",0,"{discordhash}")
                            ''')
            self.conn.commit()
            return True
        return False

    #not necessary
    def CheckForId(self,id):
        if self.conn is not None:
            if self.conn.execute(f"SELECT * FROM STUDENTS WHERE DISCORDID = '{id}'"):
                return True
        return False

    def UpdateEmail(self):
        pass

    def VerifyUser(self,userID:str,hash:str):
        if self.conn is not None:
            user=self.conn.execute(f"SELECT * FROM STUDENTS WHERE DISCORDID = '{userID}'")
            if(user and str(user[6])==hash):
                self.conn.execute(f"UPDATE STUDENTS SET VERIFIED = 1 WHERE DISCORDHASH = '{hash}',DISCORDID = '{userID}'")
            self.conn.commit()
            return self.conn.cursor().rowcount == 1
        return False

    def RemoveUnverified(self):
        if self.conn is not None:
            self.conn.execute(f"DELETE FROM STUDENTS WHERE VERIFIED = 0")
            self.conn.commit()
            return True
        return False
    
    def EmptyDB(self):
        if self.conn is not None:
            self.conn.execute(f"DELETE FROM STUDENTS")

    def GenerateCSV(self,excelpath:str=EXCEL_PATH):
        if self.conn is not None:
            with open(excelpath,"a") as f:
                Students=self.conn.execute(f"SELECT * FROM STUDENTS")
                f.write(f"S.No;Student;DiscordID;Email;isVerified;UniqueHash\n")
                for student in Students:
                    f.write(f"{student[0]};{student[1]};{student[2]};{student[3]};{student[4]};{student[5]}\n")
            return True
        return False

    def verified(self):
        if self.conn is not None:
            Students=self.conn.execute(f"SELECT * FROM STUDENTS WHERE VERIFIED = 1")
            return [str(student[2]) for student in Students]
        return False

    #doubt
    def isVerified(self,memberID):
        student=self.conn.execute(f"SELECT * FROM STUDENTS WHERE DISCORDID = '{memberID}'")
        print(student[5])
        return (student and student[5])

    def DeleteCSV(self,excelpath:str=EXCEL_PATH):
        if os.path.exists(excelpath):
            os.remove(excelpath)
            return True
        return False

    def PrintDB(self):
        if self.conn is not None:
            students=self.conn.execute(f"SELECT * FROM STUDENTS")
            for student in students:
                print(f"{student[0]} {student[1]} {student[2]} {student[3]} {student[4]} {student[5]}")

    def Close(self):
        self.conn.close()