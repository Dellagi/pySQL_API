import sqlite3


class orm:
	db_name = 'data.sql'
	def __init__(self, object_= None):
		if object_:
			self.table_ = object_.__tablename__
			# Ignore private (not in Python's sense) attributes, this is for attributes
			# You don't want to save in the database
			self.table_schema = {k: object_.__dict__[k] for k in object_.__dict__ if k[0]!="_"}
			self.buildTable()
		else:
			self.filterBy = self.filterByClass(self)

	def sql_run(self, cmd):
		sql = sqlite3.connect(self.db_name)
		sql_cursor = sql.cursor()
		sql_cursor.execute(cmd)
		dbmsg = 0
		try:
			dbmsg = sql_cursor.fetchall()
		except:
			dbmsg = sql_cursor.fetchone()
		sql.commit()
		sql_cursor.close()
		sql.close()
		return dbmsg


	def buildTable(self):
		createSQL = "CREATE TABLE IF NOT EXISTS {} ({})".format(self.table_, ''.join([' '.join([j, self.table_schema[j][1]]\
		 + [col for col, rules in self.table_schema[j][2].items() if rules==True])+"," for j in self.table_schema.keys()])[:-1])
		self.sql_run(createSQL)


	def add(self):
		addRow = "INSERT INTO {} ({}) VALUES {}".format(self.table_, \
		   ', '.join(map(str, list(self.table_schema.keys()))) , tuple([i[0] for i in self.table_schema.values()]))
		try:
			self.sql_run(addRow)
			return 0
		except Exception as e:
			return str(e)


	def update(self, pKey, **kwargs):
		condWhere, updatedVals = [', '.join(["{}='{}'".format(k, v) if not isinstance(v, int) else "{}={}".format(k, v) for k, v in data.items()])\
		 for data in [pKey, kwargs]]
		updateRow = "UPDATE {} SET {} WHERE {}".format(self.table_, updatedVals, condWhere)
		return self.sql_run(updateRow)


	class filterByClass:
		def __init__(self, daoObj):
			self.super_= daoObj

		def delete(self, tablename, **kwargs):
			condWhere = ''.join([" AND {}='{}'".format(k, v) if not isinstance(v, int) else " AND {}={}".format(k, v) for k, v in kwargs.items()])
			baseSQL = "DELETE FROM {} WHERE 1=1{}".format(tablename, condWhere)
			return self.super_.sql_run(baseSQL)


		def get(self, tablename, **kwargs):
			condWhere = ''.join([" AND {}='{}'".format(k, v) if not isinstance(v, int) else " AND {}={}".format(k, v) for k, v in kwargs.items()])
			baseSQL = "SELECT * FROM {} WHERE 1=1{}".format(tablename, condWhere)
			return self.super_.sql_run(baseSQL)
