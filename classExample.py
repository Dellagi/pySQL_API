#-*- coding: utf-8 -*-#
from pyORM import orm
import uuid, json
import ast, itertools
from functools import wraps



def updateAfterEvent(func):
	'''
	This decorator will detect the object-based table schema (PokemonClass, UserClass ...etc)
	 and will update the database after each return of the function or method
	'''
	@wraps(func)
	def wrapper(*args, **kw):
		dbSession = orm(object_= args[0])
		try:
			res = func(*args, **kw)
		finally:
			pKey = [k for k,v in res.__dict__.items() if k[0]!="_" and v[2]["PRIMARY KEY"]][0]
			updates_ = {k:v[0] for k, v in res.__dict__.items() if k[0]!="_" and '_protected' != k[-10:]}
			dbSession.update({pKey: getattr(res, pKey)[0]}, **updates_)
		return res
	return wrapper




class dummyPokemonClass(object):

	__tablename__ = "dummy"
	__typesOrderArr__ = ['paper', 'scisor', 'rock', 'some different type that loses in front of all others']
	__typesOrder__ = {'paper': [2, 3], 'scisor': [0, 3], 'rock': [1, 3], 'some different type that loses in front of all others': []}


	def __init__(self, uuid_=None, name=None, typeArrayStr=None, hp=100):
		#  It must be specified whether it is a primary key or not, the other elements can be ignored/undefined.
		# Order of the attributes must be same as args of __init__
		self.id = [uuid_ if uuid_ else str(uuid.uuid4()), "VARCHAR(255)", {"PRIMARY KEY": True, "AUTOINCREMENT": False, "NOT NULL": True, "FOREIGN KEY {} REFERENCES ...etc": False}]
		self.name = [name, "VARCHAR(255)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]

		deSerial_typeArray = ast.literal_eval(typeArrayStr)

		if not [xType in self.__typesOrderArr__ for xType in deSerial_typeArray].count(False):
			self.type = [typeArrayStr, "TEXT", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": False}]
		else:
			raise "The type of pokemon doesn't exist"

		self.hp = [hp, "INTEGER", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True,\
		 "CHECK(hp BETWEEN 0 AND 100)": True}]

	@updateAfterEvent
	def attack(self, enemyObj):
		deSerial_Self = ast.literal_eval(self.type[0])
		deSerial_enemyObj = ast.literal_eval(enemyObj.type[0])
		superAgainst = list(set(itertools.chain(*[self.__typesOrder__[t] for t in deSerial_Self])))
		if len([self.__typesOrderArr__[i] for i in superAgainst if self.__typesOrderArr__[i] in deSerial_enemyObj]):
			enemyObj.hp[0] = max(enemyObj.hp[0]-10, 0)
		return enemyObj









if __name__ == "__main__":

	pika = dummyPokemonClass(name="Pikachu", typeArrayStr=json.dumps(['paper', 'some different type that loses in front of all others']), hp=90)
	crocodil = dummyPokemonClass(name="Crocordil", typeArrayStr=json.dumps(['rock']), hp=85)


	dbSession = orm(pika)
	dbSession.add()

	dbSession = orm(crocodil)
	if not dbSession.add():
		print("{} Added successfully".format(crocodil.name[0]))



	#Attack example
	print(pika.hp[0], crocodil.hp[0])
	crocodil = pika.attack(crocodil)
	print(pika.hp[0], crocodil.hp[0])


	'''
	Extract pokemons attributes and instantiate pokemon object
	'''
	dbSession = orm()
	pokSQL = dbSession.filterBy.get(tablename="dummy", name="Pikachu")[0]
	print(pokSQL)
	pika = dummyPokemonClass(*pokSQL)

	pokSQL = dbSession.filterBy.get(tablename="dummy", name="Crocordil")[0]
	crocodil = dummyPokemonClass(*pokSQL)



	print(pika.name[0], crocodil.name[0])

	print(pika.hp[0], crocodil.hp[0])
	crocodil = pika.attack(crocodil)
	print(pika.hp[0], crocodil.hp[0])

