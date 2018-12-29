import uuid
import datetime as dt
import db

class Purchase:

    def __init__(self, AccountID, TripID, purchaseAmount, tag = "", description = ""):
        self.PurchaseID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
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

def getPurchasesByTripID(TripID):

    return [purchase for purchase in db.purchasesByID.values() if purchase.TripID == TripID]
