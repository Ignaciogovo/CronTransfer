import connect_db
db=connect_db.DataBase()
print(db.select_log(3))

