import uuid
import datetime as dt
import db
import TripMember

class Trip:

    def __init__(self, accountIDs, tripName="", tripDescription=""):
        self.ID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        tripMembers =  set([TripMember.TripMember(accountID, self.ID) for accountID in accountIDs])
        self.tripMemberIDs = [tripMember.ID for tripMember in tripMembers]
        self.tripName = tripName
        self.tripDescription = tripDescription

        db.tripsByID[self.ID] = self

def getTripByID(tripID):

    if tripID in db.tripsByID:
        return db.tripsByID[tripID]
    else:
        return None
