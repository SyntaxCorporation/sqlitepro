
def __init__(self):
	self.input_text = "> "
	self.loop = True
	self.currentDB = ""
	self.hst_file = Path.home() / ".sqlite_history"

def close(self):
	if (self.input_text != "> "):
		self.conn.commit()
		self.conn.close()
		self.input_text = "> "
		self.currentDB = self.input_text.split(">")[0].strip()
		self.conn = ""
		
def use(self, file_name):
	if (len(file_name.split(".")) < 2 
		and fullmatch(r'^[^0-9][\w]*', file_name)):
		self.close()
		self.input_text =  f"{file_name}> "
		self.currentDB = self.input_text.split(">")[0].strip()
		file_name = db_dir / file_name
		self.conn = sqlite3.connect(f"{file_name}.db")
		self.cursor = self.conn.cursor()
		db_data()
	else:
		print("Do not use (spaces), (symbols except '_'), and (numbers in the starting) in collection name...")
		
def dropDatabase(self):
	if (self.currentDB != ""):
		database = db_dir / f"{self.currentDB}.db"
		self.close()
		database.unlink()
		db_data()
	else:
		print("Use a database first...")
	
def createCollection(self, table):
	if self.currentDB != "":
		if (fullmatch(r'^[^0-9][\w]*', table)):
			self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (data TEXT)")
		else:
			print("Do not use (spaces), (symbols except '_'), and (numbers in the starting) in collection name...")
	else:
		print("Please use a database first...")