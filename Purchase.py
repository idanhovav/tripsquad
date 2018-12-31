import uuid
import datetime as dt
import db
import utils
import TripMember

class Purchase:

    def __init__(self, TripMemberID, purchaseAmount, tag = "", description = ""):
        self.PurchaseID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.TripMemberID = TripMemberID
        [self.AccountID, self.TripID] = TripMember.getTripAndAccountIDs(TripMemberID)
        self.purchaseAmount = purchaseAmount
        self.tag = tag
        self.description = description

        db.purchasesByID[self.PurchaseID] = self
        db.tripMembersByID[self.TripMemberID].totalPurchaseAmount += self.purchaseAmount

def getPurchaseByID(PurchaseID):

    if PurchaseID in db.purchasesByID:
        return db.purchasesByID[PurchaseID]
    else:
        return None

def getPurchasesByTripID(TripID):

    return [purchase for purchase in db.purchasesByID.values() if purchase.TripID == TripID]
