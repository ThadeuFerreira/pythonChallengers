# Tests adapted from `problem-specifications//canonical-data.json` @ v1.1.1
import json

class RestAPI:
    database = {}
    def __init__(self, database=None):
        self.database = database

    def get(self, url, payload=None):
        response = {"users":[]}
        if payload == None:
            response["users"] = self.database["users"]
            return json.dumps(response)
        users = json.loads(payload)[url[1:]]
        for user in users:
            for db_user in self.database["users"]:
                if db_user["name"] == user:
                    response["users"].append(db_user)
        return json.dumps(response)

    def post(self, url, payload=None):
        url = url[1:]
        local_payload = json.loads(payload)
        response = {}
        if url == "add":
            response["name"] = local_payload["user"]
            response["owes"] = {}
            response["owed_by"] = {}
            response["balance"] = 0.0
            if "users" not in self.database:
                self.database["users"] = []
                self.database["users"].append(response)
            else:
                self.database["users"].append(response)
        if url == "iou":
            response = {"users":[]}
            lender = local_payload["lender"]
            borrower = local_payload["borrower"]
            amount = local_payload["amount"]
            for user in self.database["users"]:
                if user["name"] == lender:
                    user["balance"] += amount
                    if borrower in user["owes"]:
                        balance = user["owes"][borrower] - amount
                        if balance > 0.0:
                            user["owes"][borrower] = balance
                        elif balance < 0.0:
                            user["owed_by"][borrower] = -balance
                            user["owes"].pop(borrower)
                        else:
                            user["owes"].pop(borrower)
                    elif borrower in user["owed_by"]:
                        user["owed_by"][borrower] += amount
                    else:
                        user["owed_by"][borrower] = amount
                    response["users"].append(user)
                if user["name"]== borrower:
                    user["balance"] -= amount
                    if lender in user["owed_by"]:
                        balance = user["owed_by"][lender] - amount
                        if balance > 0.0:
                            user["owed_by"][lender] = balance
                        elif balance < 0.0:
                            user["owes"][lender] = -balance
                            user["owed_by"].pop(lender)
                        else:
                            user["owed_by"].pop(lender)
                    elif lender in user["owes"]:
                        user["owes"][lender] += amount
                    else:
                        user["owes"][lender] = amount
                    response["users"].append(user)
        return json.dumps(response)