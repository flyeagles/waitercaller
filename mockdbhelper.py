import datetime

MOCK_USERS=[{'email':'test@example.com', 'salt': 'abcdefg',
	 'hashed':'7fd373300aa31a001888b1e04c8a3fea8290e9ba088f5e3322d021b044b738639c833db79b7151db183e3cec5e3db27758a39a377a3e7997bf4f8e688bbe32fc'}]

MOCK_TABLES=[{"_id":"1", "number":"1", "owner":"test@example.com", "url":"mockurl"}]

MOCK_REQUESTS = [{"table_number":"1", "table_id": "1", "time": datetime.datetime.now()} ]


class MockDBHelper:
	def get_user(self, email):
		users=[x for x in MOCK_USERS if x.get('email') == email]
		if len(users) > 0:
			return users[0]

		return None

	def add_user(self, email, salt, hashed):
		MOCK_USERS.append({'email':email, 'salt': salt, 'hashed':hashed})
		print(MOCK_USERS)

	def add_table(self, number, owner):
		MOCK_TABLES.append({"_id":str(number), "number":number, "owner":owner})
		return number

	def update_table(self, _id, url):
		for table in MOCK_TABLES:
			if table.get("_id") == _id:
				table["url"] = url
				break

	def get_tables(self, owner_id):
		return MOCK_TABLES

	def delete_table(self, table_id):
		for i, table in enumerate(MOCK_TABLES):
			if table.get("_id") == table_id:
				del MOCK_TABLES[i]
				break


	def add_request(self, tid, request_time):
		for table in MOCK_TABLES:
			if table["_id"] == tid:
				MOCK_REQUESTS.append({"table_id":str(tid), "table_number":table['number'], "time":request_time})
				break
		return MOCK_REQUESTS


	def get_requests(self, owner_id):
		return MOCK_REQUESTS


	def delete_request(self, request_id):
		print(MOCK_REQUESTS)
		for i, request in enumerate(MOCK_REQUESTS):
			if request.get("table_id") == request_id:
				del MOCK_REQUESTS[i]
				break



