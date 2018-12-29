import uuid
import time
import db

class Trip:

    def __init__(self, AccountIDs, PurchaseIDs = [], tripName="", tripDescription=""):
        self.TripID = str(uuid.uuid4())
        self.timeStamp = time.time()
        self.AccountIDs = list(set(AccountIDs)) # no repeats
        self.PurchaseIDs = list(set(PurchaseIDs)) # no repeats
        self.tripName = tripName
        self.tripDescription = tripDescription

        db.tripsByID[self.TripID] = self

def getTripByID(TripID):

    if TripID in db.tripsByID:
        return db.tripsByID[TripID]
    else:
        return None
