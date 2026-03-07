if (usr == ""):
	pass
		
elif (usr.lower() in commands.keys()):
	getattr(dfCmnd, commands[usr.lower()])()
		
elif (len(usr.split(" ")) == 2
	and usr.split(" ")[0].lower() == "use"):
	db.use(usr.split(" ")[1].strip())
		
else:
	cmd_array = usr.split(".")
	if (len(cmd_array) == 2
		and hasattr(db, cmd_array[1].split("(")[0])):
		exec(usr)
			
	elif (len(cmd_array) == 3
		and hasattr(colCmnd, cmd_array[2].split("("[0])):
		setattr(db, cmd_array[1], collectionCmnd(db, cmd_array[1]))
		exec(usr)
	
else:
	print(f"'{usr}' is not a command...")
		