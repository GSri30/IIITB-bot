from secrets import token_hex
import bcrypt
from __constants import LENGTH

def Hash(password:str):
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

def Match(password:str,hashed:str):
    return bcrypt.checkpw(password.encode("UTF-8"),hashed) 

def GeneratePassword():
    return str(token_hex(LENGTH))