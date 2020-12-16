#-*- coding: utf-8 -*-#
from orm.simpleDB import orm
import json
import ast
import hashlib, random
from mytools.utils import *




class utilisateur(object):
	"""
	La classe utilisateur définit les informations et les méthodes propres au joueur.
	Seule la clé primaire est obligatoire, les autres éléments peuvent être ignorés et non définis.
	"""

	__tablename__ = "user"
	__const_prices__ = {'pokeball':10, 'Baies': 10}

	def __init__(self, username, passwd, coin=100, zone=1, xp=0, pokeball=5, berry=2, pokCollectionStr='[]',pokedex='[]'):

		"""
		Attributs

		:param username: Pseudonyme du joueur
		:type username: str
		:param passwd : Mot de passe du joueur
		:type passwd: str
		:param coin : argent du joueur
		:type coin : int
		:param zone : zone dans laquelle se situe le joueur
		:type zone : int
		:param xp : expérience du joueur
		:type xp : int
		:param pokeball : nombre de pokeball du joueur
		:type pokeball : int
		:param berry : nombre de baies du joueur
		:type berry : int
		:param pokCollectionStr : liste des pokemons capturés par le joueur
		:type pokCollectionStr : list
		"""
		self.username = [username, "VARCHAR(255)", {"PRIMARY KEY": True, "AUTOINCREMENT": False, "NOT NULL": True}]
		self.hashed_pass_protected = [hashlib.sha1(passwd.encode('utf8')).hexdigest(), "VARCHAR(40)", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": True}]
		self.coin = [coin, "INTEGER", {"PRIMARY KEY": False, "NOT NULL": True,"CHECK(coin >= 0)": True}]
		self.zone = [zone, "INTEGER", {"PRIMARY KEY": False,"NOT NULL": True, "CHECK(zone BETWEEN 1 AND 11)": True}]
		self.xp = [xp, "INTEGER", {"PRIMARY KEY": False,"NOT NULL": True, "CHECK(xp BETWEEN 1 AND 2000)": True}]
		self.pokeball = [pokeball, "INTEGER", {"PRIMARY KEY": False,"NOT NULL": True, "CHECK(pokeball BETWEEN 0 AND 20)": True}]
		self.berry = [berry, "INTEGER", {"PRIMARY KEY": False,"NOT NULL": True, "CHECK(berry BETWEEN 0 AND 20)": True}]
		self.pokCollection = [pokCollectionStr, "TEXT", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": False}]
		self.pokedex=[pokedex, "TEXT", {"PRIMARY KEY": False, "AUTOINCREMENT": False, "NOT NULL": False}]



	def	setPokemon(self, pokemon_uuid):
		""" Méthode permettant de définir un identifiant unique universel (UUID) à chaque Pokemon.

		:param pokemon_uuid: UUID du Pokemon
		:type pokemon_uuid : str
		"""
		deSerial_pokArray = ast.literal_eval(self.pokCollection[0])
		if pokemon_uuid in deSerial_pokArray:
			self._setPokemon = pokemon_uuid


	@staticmethod
	def retirer(pokObj):
		""" Méthode permettant de retirer de la base un Pokemon.

		:param pokObj: objet Pokemon
		:type pokObj: str
		:return: table Pokemon filtrée du Pokemon retiré
		"""
		dbSession = orm()
		return dbSession.filterBy.delete(tablename="pokemon", id=pokObj.id[0])


	@updateAfterEvent
	def shop(self, num_pokebal=0, num_berry=0):
		""" Méthode permettant d'acheter des Pokeball et des baies

		:param num_pokebal: nombre de pokeball
		:type num_pokebal: int
		:param num_berry: nombre de baies
		:type num_berry: int
		:return: informations du joueur
		"""
		cost_ = num_pokebal*self.__const_prices__['pokeball'] + num_berry*self.__const_prices__['Baies']
		if cost_ <= self.coin[0]:
			self.coin[0] -= cost_
			self.pokeball[0] += num_pokebal
			self.berry[0] += num_berry
			print('Achat effectué')
		else:
			print('Solde insuffisant')
		return self


	@updateAfterEvent
	def Capture(self, pokeObj):
		""" Méthode permettant de Capture de nouveaux Pokemon

		:param pokeObj: objet Pokemon
		:type pokeObj: str
		:return: informations du joueur
		"""
		xp_diff = int((pokeObj.xp[0]-self.xp[0])/100)
		xp_diff = int(min((20-xp_diff)/20, 1) * 10)
		ifeelLucky = random.choice([False]*xp_diff+[True]*(10-xp_diff))
		ifeelLucky = True
		if self.pokeball[0]<=0:
			print("Vous n'avez plus de pokeballs")
		elif ifeelLucky:
			deSerial_pokArray = ast.literal_eval(self.pokCollection[0])
			deSerial_pokArray.append(pokeObj.id[0])
			self.pokCollection[0] = json.dumps(deSerial_pokArray)
			pokeObj.state[0] = 'Not Wild'
			self.pokeball[0] -= 1
			updateObj(pokeObj)
			print(pokeObj.name[0]+" est capturé")
		else:
			print(pokeObj.name[0]+"n'a pas été capturé")

		return self

	@updateAfterEvent
	def move(self, targetZone):
		""" Méthode permettant de naviguer dans les différentes zones du jeu

		:param targetZone: zone dans laquelle le joueur souhaite aller
		:type targetZone: int
		:return: informations du joueur
		"""
		self.zone[0] = targetZone
		return self


	@updateAfterEvent
	def heal(self,pokeObj):
		""" Méthode permettant de soigner des Pokemons

		:param pokeObj: objet Pokemon
		:type pokeObj: str
		:return: informations du joueur
		"""
		if self.berry[0]<=0:
			print("Vous n'avez plus de baies")
		else :
			pokeObj.hp[0] = 100
			self.berry[0] = max(1, self.berry[0]-1)
			print(pokeObj.name[0]+' est soigné')
		updateObj(pokeObj)
		return self
