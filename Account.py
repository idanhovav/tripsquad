import uuid
import datetime as dt
import db
import hashlib
import os
import binascii

hashIterations = 10000
saltLength = 64
hashFunctionName = 'sha256'

class Account:
    def __init__(self, name, email, password):
        self.ID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.name = name
        self.email = email
        self.passwordSalt = os.urandom(saltLength)
        self.passwordHash = generateCryptographicHash(password, self.passwordSalt)

    # Returns true on successful insertion
    # dbFunction
    def writeToDB(self):
        db.accountsByID[self.ID] = self
        success = getAccountByID(self.ID) != None

        return success

    def isPassword(self, givenPassword):
        givenPasswordHash = generateCryptographicHash(givenPassword, self.passwordSalt)
        return givenPasswordHash == self.passwordHash

def generateCryptographicHash(password, salt):
    generatedHash = hashlib.pbkdf2_hmac(hashFunctionName, bytearray(password, 'utf8'), salt, hashIterations)

    return str(binascii.hexlify(generatedHash))

# dbFunction
def getAccountByID(accountID):
    if accountID in db.accountsByID:
        return db.accountsByID[accountID]
    else:
        return None

def validateAccount(accountID, password):
    account = getAccountByID(accountID)

    return account != None and account.isPassword(password)

def createAccount(name, email, password):
    newAccount = Account(name, email, password)

    return newAccount if newAccount.writeToDB() else None
