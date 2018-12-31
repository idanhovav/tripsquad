import uuid
import datetime as dt
import db

class Account:

    def __init__(self, name, email, password):
        self.ID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.name = name
        self.email = email
        self.password = password

    # Returns true on successful insertion
    # dbFunction
    def writeToDB(self):
        db.accountsByID[self.ID] = self
        success = getAccountByID(self.ID) != None

        return success

    def isPassword(self, givenPassword):

        return self.hasPassword() and self.password == givenPassword

    def hasPassword(self):

        return self.password != None


# dbFunction
def getAccountByID(accountID):
    if accountID in db.accountsByID:
        return db.accountsByID[accountID]
    else:
        return None

def validateAccount(accountID, password):
    account = getAccountByID(accountID)

    return account.isPassword(password)

def createAccount(name, email, password):
    newAccount = Account(name, email, password)

    return newAccount if newAccount.writeToDB() else None
