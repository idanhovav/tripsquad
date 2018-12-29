import uuid
import time
import db

class Purchase:

    def __init__(self, AccountID, TripID, purchaseAmount, tag = "", description = ""):
        self.PurchaseID = str(uuid.uuid4())
        self.timeStamp = time.time()
        self.AccountID = AccountID
        self.TripID = TripID
        self.purchaseAmount = purchaseAmount
        self.tag = tag
        self.description = description

        db.purchasesByID[self.PurchaseID] = self

def getPurchaseByID(PurchaseID):

    if PurchaseID in db.purchasesByID:
        return db.purchasesByID[PurchaseID]
    else:
        return None
