import uuid
import datetime as dt
import db
import TripMember

class Trip:

    def __init__(self, AccountIDs, PurchaseIDs = [], tripName="", tripDescription=""):
        self.TripID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        tripMembers =  set([TripMember.TripMember(accountID, self.TripID) for accountID in AccountIDs])
        self.tripMemberIDs = [tripMember.TripMemberID for tripMember in tripMembers]
        self.PurchaseIDs = list(set(PurchaseIDs)) # no repeats
        self.tripName = tripName
        self.tripDescription = tripDescription

        db.tripsByID[self.TripID] = self

def getTripByID(TripID):

    if TripID in db.tripsByID:
        return db.tripsByID[TripID]
    else:
        return None
