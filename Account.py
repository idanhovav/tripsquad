import uuid
import time
import db

class Account:

	def __init__(self, name, email, password = None):
		self.AccountID = str(uuid.uuid4())
		self.timeStamp = time.time()
		self.name = name
		self.email = email
		self.password = password

		db.accountsByID[self.AccountID] = self
