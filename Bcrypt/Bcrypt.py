from secrets import token_hex
import bcrypt
from __constants import LENGTH

def Hash(password:str):
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt()).decode("UTF-8")

def Match(password:str,hashed:str):
    return bcrypt.checkpw(password.encode("UTF-8"),hashed.encode("UTF-8")) 

def GeneratePassword(len=LENGTH):
    return str(token_hex(len))