import uuid
import datetime as dt
import db

class Account:

    def __init__(self, name, email, password = None):
        self.AccountID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.name = name
        self.email = email
        self.password = password

        db.accountsByID[self.AccountID] = self

def getAccountByID(AccountID):

    if AccountID in db.accountsByID:
        return db.accountsByID[AccountID]
    else:
        return None

def validateAccount(AccountID, password):
    account = getAccountByID(AccountID)
    if account and account.password:
        return account.password == password

    return False
