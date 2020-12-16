#-*- coding: utf-8 -*-#
from orm.simpleDB import orm
import uuid
import ast, itertools
from mytools.utils import updateAfterEvent



class pokemon(object):

	__tablename__ = "pokemon"
	__typesOrderArr__ = ['rock', 'fighting', 'ground', 'dark', 'steel', 'electric', 'ghost', 'grass', 'flying', 'fire', 'water', 'fairy', 'dragon', 'normal', 'poison', 'ice', 'bug', 'psychic']
	__typesOrder__ = {'rock': [1], 'fighting': [2], 'ground': [3], 'dark': [4], 'steel': [5], 'electric': [6], 'ghost': [7], 'grass': [8], 'flying': [9], 'fire': [10], 'water': [11], 'fairy': [12], 'dragon': [13], 'normal': [14], 'poison': [15], 'ice': [16], 'bug': [17], 'psychic': []}


	def __init__(self, uuid_=None,state="Wild", name=None, typeArrayStr=None, movesArrStr=None, xp=None, zone=None, hp=100):
		#  Seule la clé primaire est obligatoire, les autres éléments peuvent être ignorés et non définis
		self.id = [uuid_ if uuid_ else str(uuid.uuid4()), "VARCHAR(255)", {"PRIMARY KEY": True, "AUTOINCREMENT": False, "NOT NULL": True}]
		self.state=[state, "VARCHAR(255)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]
		self.name = [name, "VARCHAR(255)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]
		deSerial_typeArray = ast.literal_eval(typeArrayStr)

		if not [xType in self.__typesOrderArr__ for xType in deSerial_typeArray].count(False):
			self.type = [typeArrayStr, "TEXT", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": False}]
		else:
			raise "The type of pokemon doesn't exist"
		self.moves = [movesArrStr, "TEXT", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]
		self.xp = [xp, "INTEGER", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]
		self.zone = [zone, "INTEGER", {"PRIMARY KEY": False, "NOT NULL": False, "CHECK((zone BETWEEN 1 AND 11) OR (zone IS NULL))": True}]
		self.hp = [hp, "INTEGER", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True,\
		 "CHECK(hp BETWEEN 0 AND 100)": True}]

	@updateAfterEvent
	def attack(self, enemyObj):
		deSerial_Self = ast.literal_eval(self.type[0])
		deSerial_enemyObj = ast.literal_eval(enemyObj.type[0])
		superAgainst = list(set(itertools.chain(*[self.__typesOrder__[t] for t in deSerial_Self])))
		if len([self.__typesOrderArr__[i] for i in superAgainst if self.__typesOrderArr__[i] in deSerial_enemyObj]):
			enemyObj.hp[0] = max(enemyObj.hp[0]-10, 0)
		elif self.xp and enemyObj.xp:
			if self.xp[0] > enemyObj.xp[0]:
				enemyObj.hp[0] = max(enemyObj.hp[0]-7, 0)
			else:
				enemyObj.hp[0] = max(enemyObj.hp[0]-5, 0)
		return enemyObj


