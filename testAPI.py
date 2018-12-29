import requests
import unittest
from unittest import TestCase
import json
import subprocess
import time
import sys

global sleepTimer
sleepTimer = 2 # seconds

serverURL = "http://0.0.0.0:5000"

class TestAPI(TestCase):
    serverProcess = None

    @classmethod
    def setUpClass(cls):
        print("Starting API server")
        # start the API server
        TestAPI.serverProcess = subprocess.Popen("flask run --host=0.0.0.0".split())
        # wait for server to initialize before running tests
        time.sleep(sleepTimer)
        # check it's running
        print(requests.get(serverURL + "/").text)

    @classmethod
    def tearDownClass(cls):
        if TestAPI.serverProcess:
            print("Terminating API server")
            TestAPI.serverProcess.terminate()


    def testCreateAccount(self):
        params = {"name": "Idan", "emailAddress": "idan@hovav.com"}
        createAccountResponse = requests.post(serverURL + "/account/create", data=params)
        print(createAccountResponse.text)
        self.assertTrue(createAccountResponse.status_code == 200)
        createAccountJson = createAccountResponse.json()
        newAccountID = createAccountJson["accountID"]
        print("AccountID: %s " % newAccountID)
        self.assertTrue(newAccountID)

        getAccountInfoResponse = requests.get(serverURL + "/account/" + newAccountID + "/info")
        self.assertTrue(getAccountInfoResponse.status_code == 200)
        getAccountInfoJson = getAccountInfoResponse.json()
        expectedParams = ["name", "emailAddress", "accountID"]
        self.assertTrue(all([param in getAccountInfoJson for param in expectedParams]))
        self.assertTrue(getAccountInfoJson["name"] == params["name"])
        self.assertTrue(getAccountInfoJson["emailAddress"] == params["emailAddress"])

    def testCreateTrip(self):
        createOwnerParams = {"name": "Idan", "emailAddress": "idan@hovav.com", "password": "abcdef"}
        createAccountParams = {"name": "Bob", "emailAddress": "Bob@billy.com"}
        createOwnerResponse = requests.post(serverURL + "/account/create", data=createOwnerParams)
        createAccountResponse = requests.post(serverURL + "/account/create", data=createAccountParams)
        ownerAccountID = createOwnerResponse.json()["accountID"]
        accountID = createAccountResponse.json()["accountID"]

        createTripParams = {"creatorAccountID": ownerAccountID, "creatorAccountPassword": "abcdef", "tripName": "test", "tripMemberAccountIDs": [ownerAccountID, accountID]}
        createTripResponse = requests.post(serverURL + "/trip/create", data=createTripParams)
        self.assertTrue(createTripResponse.status_code == 200)
        tripID = createTripResponse.json()["tripID"]
        self.assertTrue(tripID)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        sleepTimer = int(sys.argv[1])
    unittest.main(argv=[sys.argv[0]])