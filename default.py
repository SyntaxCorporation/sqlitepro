import readline
from .utils import pretty_print

class defaultCmnd:
	def __init__(self, new_instance):
		self.db_self = new_instance
		
	def close(self):
		print("Closing the database...")
		readline.write_history_file(self.db_self.hst_file)
		self.db_self.loop = False
		self.db_self.close()
		print("Database closed successfully...\n")
			
	def show_dbs(self):
		for db_name in db_names:
			print(db_name.split(".")[0])
									
	def clear(self):
		system("clear")
									
	def show_cols(self):
		if self.db_self.currentDB != "":
			cols = self.db_self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table'").fetchall()
			if len(cols) > 0:
				for col in cols:
					print(col[0])
			else:
				pretty_print({"Object": 0})
				
		else:
			print("Use a database first to see its collections...")
			
	def show_crnt_db(self):
		if (self.db_self.currentDB != ""):
			print(self.db_self.currentDB)
		else:
			pretty_print({"Object": 0})
