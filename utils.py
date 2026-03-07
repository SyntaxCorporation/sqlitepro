from colorama import init, Fore, Back, Style

init(autoreset = True)

def pretty_print(data, depth = 0, indent = 2, sdepth = False, comma = False):
	if isinstance(data, list):
		if not sdepth:
			print(depth * (" " * indent), end = "")
		print(Fore.BLUE + Style.BRIGHT + "[" + Style.RESET_ALL)
		for i in data:
			if comma:
				print(",")
			else:
				comma = True
			if isinstance(i, bool) or i is None:
				print((depth + 1) * (" " * indent), end = "")
				print(Fore.BLUE + str(i), end = "")
			elif isinstance(i, int) or isinstance(i, float):
				print((depth + 1) * (" " * indent), end = "")
				print(Fore.CYAN + str(i) + Style.RESET_ALL, end = "")
			elif isinstance(i, str):
				print((depth + 1) * (" " * indent), end = "")
				print(Fore.MAGENTA + f'\"{i}\"', end = "")
			else:
				pretty_print(i, depth + 1)
		print("\n" + (depth * (" " * indent)), end = "")
		print(Fore.BLUE + Style.BRIGHT + "]" + Style.RESET_ALL, end = "")
	elif isinstance(data, dict):
		if not sdepth:
			print(depth * (" " * indent), end = "")
		print(Fore.BLUE + Style.BRIGHT + "{" + Style.RESET_ALL)
		for k, v in zip(data.keys(), data.values()):
			if comma:
				print(",")
			else:
				comma = True
			print((depth + 1) * (" " * indent) , end = "")
			if isinstance(k, int) or isinstance(k, float):
				print(Fore.YELLOW + Style.DIM + str(k) + Style.RESET_ALL + ": ", end = "")
			else:
				print(Fore.YELLOW + f'\"{k}\"' + Fore.RESET + ": ", end = "")
			if isinstance(v, bool) or v is None:
				print(Fore.BLUE + str(v), end = "")
			elif isinstance(v, int) or isinstance(v, float):
				print(Fore.CYAN + str(v) + Style.RESET_ALL, end = "")
			elif isinstance(v, str):
				print(Fore.MAGENTA + f'\"{v}\"', end = "")
			else:
				pretty_print(v, depth + 1, sdepth = True)
			
		print("\n" + (depth * (" " * indent)), end = "")
		print(Fore.BLUE + Style.BRIGHT + "}" + Style.RESET_ALL, end = "")
	
	if depth == 0:
		print("")
		


db_fields = ["*"]
placeholder = [" "]
values = []
elements = []
def query_generator(query, fields = {}, OR = False, kwd = "="):
	def placeholder_maker(kwd, isand = True):
		if kwd == "$in":
			placeholder[-1] += f" WHERE EXISTS (SELECT 1 FROM json_each(data.{".".join(elements)}) WHERE value = ?)"
			placeholder[-1] += f" WHERE EXISTS (SELECT 1 FROM json_each(data.{".".join(elements)}) WHERE value = ?)"
		elif kwd == "$and":
			placeholder[-1] += f" json_extract(data, $.{".".join(elements)}) = ?"
			isand = False
		elif kwd in keywords:
			placeholder[-1] += f" json_extract(data, $.{".".join(elements)} {keyword_converter(kwd)} ?"
		else:
			placeholder[-1] += f" json_extract(data, $.{".".join(elements)}) = ?"
		if isand:
			placeholder[-1] += " AND "
	def keyword_converter(kwd):
		if kwd == "$eq":
			return "="
		elif kwd == "$gt":
			return ">"
		elif kwd == "$lt":
			return "<"
		elif kwd == "$le":
			return "<="
		elif kwd == "$ge":
			return ">="
			
	keywords = ["$gt", "$lt", "$ge", "$le", "$eq", "$and", "$in"]
	
	print("\n", query, "\n")
	for k, v in zip(query.keys(), query.values()):
		if k in keywords:
			if k == "$and":
				if isinstance(v, list):
					for i in v:
						if OR:
							placeholder[-1] += " OR "
						else:
							OR = True
						query_generator(i, kwd = k)
				else:
					print(Fore.WHITE + Style.RED + "Invalid Value...\nUse Array datatype with '$in'..." + Style.RESET_ALL)
					return 1
			elif k == "$in":
				if isinstance(v, list):
					values.append(tuple(v))
				else:
					print(Fore.WHITE + Style.RED + "Invalid Value...\nUse Array datatype with '$in'..." + Style.RESET_ALL)
					return 1
			else:
				if isinstance(v, dict):
					query_generator(v, kwd = k)
				else:
					placeholder[-1] = placeholder[-1].rstrip("= ?") + " " + keyword_converter(k) + " ?"
					values.append(v)
		else:
			elements.append(k)
			placeholder_maker(kwd)
			if isinstance(v, dict):
				query_generator(v)
			else:
				values.append(v)
			elements.pop()
			
				
			
	if len(fields) > 0:
		db_fields.clear()
		if len(fields) == 1 or len(fields) == 2 and "_id" in fields.keys():
			for k, v in zip(fields.keys(), fields.values()):
				if isinstance(v, int) and v:
					db_fields.append(f" json_extract(data, $.{k})")
		else:
			print("Invalid Placeholder...")
			return 1
	
	print("\n", ",".join(db_fields))
	print("\n", " AND ".join(placeholder))
	print("\n", tuple(values))
	return ",".join(db_fields), " AND ".join(placeholder), tuple(values)
