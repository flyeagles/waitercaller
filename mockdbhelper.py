MOCK_USERS=[{'email':'test@example.com', 'salt': 'abcdefg',
	 'hashed':'7fd373300aa31a001888b1e04c8a3fea8290e9ba088f5e3322d021b044b738639c833db79b7151db183e3cec5e3db27758a39a377a3e7997bf4f8e688bbe32fc'}]


class MockDBHelper:
	def get_user(self, email):
		users=[x for x in MOCK_USERS if x.get('email') == email]
		if len(users) > 0:
			return users[0]

		return None

	def add_user(self, email, salt, hashed):
		MOCK_USERS.append({'email':email, 'salt': salt, 'hashed':hashed})
		print(MOCK_USERS)
