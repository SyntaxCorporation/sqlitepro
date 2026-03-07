class collectionCmnd:
	def __init__(self, new_instance, table):
		self.db_self = new_instance
		self.table = table
		
	def drop(self):
		try:
			self.db_self.cursor.execute(f"DROP TABLE {self.table}")
		except:
			print("Collection does not exists...")
		
	def insertOne(self, data):
		unq_id = ""
		for i in range(10):
			if choice([True, False]):
				unq_id += str(randint(0, 9))
			else:
				unq_id += choice(ascii_letters)
		data_str = dumps({"_id": unq_id, **data})
		self.db_self.cursor.execute(f'''
			INSERT INTO {self.table} (data) VALUES (?)
		''', (data_str,))
		
	def insertMany(self, data):
		def unq_id_generator():
			unq_id = ""
			for i in range(10):
				if choice([True, False]):
					unq_id += str(randint(0, 9))
				else:
					unq_id += choice(ascii_letters)
			return unq_id
		tupled_data = [(dumps({"_id": unq_id_generator(), **d}),) for d in data]
		self.db_self.cursor.executemany(f"""
			INSERT INTO {self.table} (data) VALUES (?)
		""", tupled_data)
		
	def find(self, query = {}, fields = {}):
		def pretty():
			pass
		if len(query) > 0:
			clauses = []
			db_fields = []
			placeholder = []
			values = []
			f, p, v = query_generator(query, fields)
			
			"""raw_data = self.db_self.cursor.execute(f'''
				SELECT 
				{",".join(f)}
				FROM
				{self.table}
				WHERE
				{p}
			''', v).fetchall()"""
			
		else:
			raw_data = self.db_self.cursor.execute(f"SELECT data FROM {self.table}").fetchall()
			data = [loads(row[0]) for row in raw_data]
			pretty_print(data)