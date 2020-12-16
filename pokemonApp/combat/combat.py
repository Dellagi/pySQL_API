#-*- coding: utf-8 -*-#
from orm.simpleDB import orm
import uuid, random
import ast
from business_objects.pokemon import pokemon
from business_objects.user import utilisateur
from PyInquirer import prompt
from api.pokAPI import ApiClass


class combat(object):
	__tablename__ = "combat"

	def __init__(self, userObj=None, enemyPokObj=None, combat_id=None):
		#self.finished = [[True, False][0 if combat_id else 1], "BOOLEAN",  {"PRIMARY KEY": False, "NOT NULL": True}]
		if combat_id:
			# this for recontructing objects in case of the user try to continue a started match
			dbSession = orm()
			resSQL = dbSession.filterBy.get(tablename="combat", id=combat_id)[0]
			userIDSql, pok1IDSql, pok2IDSql = resSQL[1], resSQL[2], resSQL[3]

			userSQL = dbSession.filterBy.get(tablename="user", username=userIDSql)[0]
			userObj = utilisateur(*userSQL)
			userObj.setPokemon(pok1IDSql)

			pokSQL = dbSession.filterBy.get(tablename="pokemon", id=pok2IDSql)[0]
			enemyPokObj = pokemon(*pokSQL)

			self.__init__(userObj, enemyPokObj)
			
		else:
			if not('_utilisateur__setPokemon' in userObj.__dict__.keys()):
				self.combatPokemon(userObj)
			self.id = [combat_id if combat_id else str(uuid.uuid4()), "VARCHAR(255)", {"PRIMARY KEY": True, "AUTOINCREMENT": False, "NOT NULL": True}]
			self.stateCombat=["ON","VARCHAR(255)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]			
			self.userID = [userObj.username[0], "VARCHAR(255)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]
			self.userPokID = [userObj._setPokemon,"VARCHAR(255)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]
			self.enemyPokId=[enemyPokObj.id[0],"VARCHAR(255)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]
			###Private attributes###
			self._userObj = userObj
			self._enemyPokObj = enemyPokObj



	@staticmethod
	def combatPokemon(userObj):
		deSerial_pokArray = ast.literal_eval(userObj.pokCollection[0])

		dbSession = orm()
		pokSQLArr = []
		for pokUUID in deSerial_pokArray:
			pokSQL = dbSession.filterBy.get(tablename="pokemon", id=pokUUID)[0]
			myPokObj = pokemon(*pokSQL)
			pokSQLArr.append(myPokObj)

		if len(pokSQLArr):
			options=['{} : {}'.format(p.name[0],p.id[0]) for p in pokSQLArr]
			form=[{"name": "choosePok", "type": "list", "message": "Pick a pokemon","choices": options}]
			answer = prompt(form)	
			pokemon_uuid=answer["choosePok"].split(':')[1][1:]

		userObj.setPokemon(pokemon_uuid)
		
		pokSQL = dbSession.filterBy.get(tablename="pokemon", id=pokemon_uuid)[0]
		newPokObj = pokemon(*pokSQL)

		return userObj, newPokObj


	def call_menus_and_controle_comabt_flow(self):
		apiObj = ApiClass()
		options = ['Escape' , 'Change your pokemon', 'Capture', 'Attack']
		dbSession = orm()
		pokSQL = dbSession.filterBy.get(tablename="pokemon", id=self.userPokID[0])[0]
		PokObj = pokemon(*pokSQL)

		if PokObj.hp[0]<=0:
			return [0, 'Print', "You lost"]
		elif self._enemyPokObj.hp[0]<=0:
			return [0, 'Print', "You won"]

		pokMoves_1 = ast.literal_eval(PokObj.moves[0])
		pokMoves_2 = ast.literal_eval(self._enemyPokObj.moves[0])
		pokMovesFinal = {}
		for m in pokMoves_1+pokMoves_2:
			if m not in pokMovesFinal.keys():
				#pokMovesFinal[m] = apiObj.get_move(m)['accuracy']
				pokMovesFinal[m] = 100
			if len(pokMovesFinal.keys())>10:
				break

		form=[{"name": "currentQ", "type": "list", "message": "Choose","choices": options}]
		answer = prompt(form)

		if answer['currentQ'] == 'Change your pokemon':
			self._userObj, PokObj = self.combatPokemon(self._userObj)
			self.userPokID[0] = self._userObj._setPokemon
			return [1, 'pass']

		elif answer['currentQ'] == 'Escape':
			return [0, 'pass']

		elif answer['currentQ'] == 'Capture':
			return [1, 'Capture']

		else:
			
			moves_ = [i for i in pokMoves_1 if i in pokMovesFinal.keys()]

			options = [i for i in moves_]
			form=[{"name": "currentQ", "type": "list", "message": "Choose a move","choices": options}]
			answers = prompt(form)
			
			bias_ = pokMovesFinal[answers['currentQ']]
			bias_Arr = [True]*bias_ + [False]*(100-bias_)
			if random.choice(bias_Arr) or 1:
				PokObj.attack(self._enemyPokObj)
				self._enemyPokObj.attack(PokObj)
				return [1, 'Table', [[PokObj.name[0], PokObj.xp[0], PokObj.hp[0]],\
				 [self._enemyPokObj.name[0], self._enemyPokObj.xp[0], self._enemyPokObj.hp[0]]]]



