import db

class TripMember:
    def __init__(self, accountID, tripID):
        self.TripMemberID = str(uuid.uuid4())
        self.timeStamp = str(dt.datetime.today())
        self.accountID = accountID
        self.tripID = tripID
        self.totalPurchaseAmount = 0
        db.tripMemberByID[self.TripMemberID] = self
