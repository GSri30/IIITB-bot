import os
from pathlib import Path
import sqlite3
from sqlite3.dbapi2 import Error

from Bcrypt import Bcrypt

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

    def checkTableExists(self,tablename:str):
        cursor=self.conn.cursor()
        cursor.execute("""
                    SELECT name
                    FROM sqlite_master
                    WHERE type = 'table' AND 
                    name NOT LIKE 'sqlite_%';
                    """)
        existingtables=cursor.fetchone()
        if tablename in existingtables:
            cursor.close()
            return True

        cursor.close()
        return False

    def CreateTable(self):
        cursor=self.conn.cursor()
        if not self.checkTableExists("STUDENTS"):
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
        else:
            print("Using existing table.")
        cursor.close()
        

    def AddUser(self,user:str,discordid:str,email:str,discordhash:str):
        if self.conn is not None:
            self.conn.execute(f'''INSERT INTO STUDENTS (USER,DISCORDID,EMAIL,VERIFIED,DISCORDHASH)\
                                VALUES ("{user}","{discordid}","{email}",0,"{discordhash}")
                            ''')
            self.conn.commit()
            return True
        return False

    def isPresentUnverified(self,userID:str,mailID:str):
        if self.conn is not None:
            verifiedBools=self.conn.execute(f"SELECT VERIFIED FROM STUDENTS WHERE DISCORDID = '{userID}' AND EMAIL = '{mailID}'")
            if verifiedBools:
                for vbool in verifiedBools:
                    if not vbool:
                        return True
        return False

    def RemoveUser(self,userID:str,mailID:str):
        if self.conn is not None:
            self.conn.execute(f"DELETE FROM STUDENTS WHERE DISCORDID = '{userID}' AND EMAIL = '{mailID}'")
            self.conn.commit()
            return True
        return False

    def UpdateEmail(self):
        pass

    def VerifyUser(self,userID:str,key:str):
        found=False
        if self.conn is not None:
            users=self.conn.execute(f"SELECT * FROM STUDENTS WHERE DISCORDID = '{userID}'")
            for user in users:
                if Bcrypt.Match(key,user[5]):
                    self.conn.execute(f"UPDATE STUDENTS SET VERIFIED = 1 WHERE DISCORDHASH = '{user[5]}' AND DISCORDID = '{userID}'")
                    self.conn.commit()
                    found=True
                    break
            print(found)
            print(self.conn.cursor().rowcount)
        return found

    def RemoveUnverified(self):
        if self.conn is not None:
            unverified=self.conn.execute(f"SELECT DISCORDID FROM STUDENTS WHERE VERIFIED = 0")
            self.conn.execute(f"DELETE FROM STUDENTS WHERE VERIFIED = 0")
            self.conn.commit()
            if unverified is None:
                unverified=[]
            return list(unverified)
        return None
    
    def EmptyDB(self):
        if self.conn is not None:
            self.conn.execute(f"DELETE FROM STUDENTS")
            self.conn.commit()
            print("Emptied the database successfully!")
            return True
        return False

    def GenerateCSV(self,excelpath:str=EXCEL_PATH):
        if self.conn is not None:
            with open(excelpath,"a") as f:
                Students=self.conn.execute(f"SELECT * FROM STUDENTS")
                f.write(f"S.No;Student;DiscordID;Email;isVerified;UniqueHash\n")
                for student in Students:
                    f.write(f"{student[0]};{student[1]};{student[2]};{student[3]};{student[4]};{student[5]}\n")
            return True
        return False

    # def verified(self):
    #     if self.conn is not None:
    #         Students=self.conn.execute(f"SELECT * FROM STUDENTS WHERE VERIFIED = 1")
    #         return [str(student[2]) for student in Students]
    #     return False

    def isVerified(self,memberID:str,mailID:str=None):
        if mailID is None:
            students=self.conn.execute(f"SELECT * FROM STUDENTS WHERE DISCORDID = '{memberID}'")    
        else:
            students=self.conn.execute(f"SELECT * FROM STUDENTS WHERE DISCORDID = '{memberID}' AND EMAIL = '{mailID}'")
        if students:
            for student in students:
                if student[4]:
                    return True
        return False

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