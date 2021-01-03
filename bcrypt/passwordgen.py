#bcrypt is used for hashing

from secrets import token_hex
import string
import bcrypt

LENGTH=16

def hash(password):
    return bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

def match(password,hashed):
    return bcrypt.checkpw(password.encode("UTF-8"),hashed) 

def passgen():
    return str(token_hex(LENGTH))