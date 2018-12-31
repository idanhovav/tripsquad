import uuid
import datetime as dt
import db

class Account:

    def __init__(self, name, email, password = None):
        self.ID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.name = name
        self.email = email
        self.password = password

        db.accountsByID[self.ID] = self

def getAccountByID(accountID):

    if accountID in db.accountsByID:
        return db.accountsByID[accountID]
    else:
        return None

def validateAccount(accountID, password):
    account = getAccountByID(accountID)
    if account and account.password:
        return account.password == password

    return False
