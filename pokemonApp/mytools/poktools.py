import sys
from PyInquirer import prompt
from business_objects.user import utilisateur
from business_objects.pokemon import pokemon
from combat.combat import combat
from orm.simpleDB import orm
import hashlib
import time, ast, json
from prettytable import PrettyTable
from mytools.utils import updateObj
from random import randint
import os, pyfiglet


logo_ = pyfiglet.figlet_format("ORM Pokemon")


def resetBanner(*args):
	os.system('reset')
	if len(args):
		print(args[0])
	print(logo_)



def exit_func(*args):
	print('Au revoir')
	sys.exit(0)


def signup_func(*args):
	pyMenus = args[0]['signup']
	answers = prompt(pyMenus)
	userObj = utilisateur(answers['username'].lower(), answers['password'], coin=100, zone=randint(1, 11), xp=1, pokeball=1, berry=0, pokCollectionStr='[]',pokedex='[]')
	dbSession = orm(userObj)
	if not dbSession.add():
		return [1, "pass","L'inscription s'est terminée avec succès, essayez de vous connecter"]
	return [0, "pass", ""]


def logout_func(*args):
	return [1, "state_manager['connected']=False;state_manager['username']='';state_manager['currentMenu']='Menu1';"\
	, "[!] Déconnexion réussie"]


def myPokColl_func(*args):
	username = args[1]['username']
	dbSession = orm()
	usrSQL = dbSession.filterBy.get(tablename="user", username=username)[0]
	usrObj = utilisateur(*usrSQL)
	pokedexArr = ast.literal_eval(usrObj.pokCollection[0])
	if len(pokedexArr):
		pokObjArr = []
		for pokID in pokedexArr:
			pokSQL = dbSession.filterBy.get(tablename="pokemon", id=pokID)[0]
			pokObjArr.append(pokemon(*pokSQL))
		pyMenus = args[0]['pokedexMenu']
		pyMenus[0]['choices'] = [i.name[0] for i in pokObjArr]
		answers = prompt(pyMenus)
		showPok = [i for i in pokObjArr if answers['currentQ'] == i.name[0]][0]
		pokProfile_tree(showPok)
		input("Cliquez sur [Entrée] pour Go back to the main menu")
		return [1, "pass", ""]
	return [0, "pass", "Pokedex est vide"]



def signin_func(*args):
	for i in range(2):
		pyMenus = args[0]['signin']
		answers = prompt(pyMenus)
		hashed_pass_ = hashlib.sha1(answers['password'].encode('utf8')).hexdigest()
		dbSession = orm()
		usrSQL = dbSession.filterBy.get(tablename="user", username=answers['username'], hashed_pass_protected=hashed_pass_)
		if len(usrSQL):
			return [1, "state_manager['connected']=True;state_manager['username']='{}';state_manager['currentMenu']='Menu2';"\
			.format(answers['username']), "[+] Bienvenue {}, tu es dans zone: {}".format(answers['username'], usrSQL[0][3])]
		sys.stdout.write('\033[91m' + "\r" + "[-] Réessayer s'il vous plaît" + '\033[0m' + '\n')
	return [0, "pass", "Échec d'identification"]



def portfolio_func(*args):
	username = args[1]['username']
	dbSession = orm()
	usrSQL = dbSession.filterBy.get(tablename="user", username=username)[0]
	usrObj = utilisateur(*usrSQL)
	portTemplate = "{}\n├── Coins\n│       └── {}\n├── Pokeballs\n│       └── {}\n├── Experience\n│       └── {}\n├── Berries\n│       └── {}"
	print(portTemplate.format(username, usrObj.coin[0], usrObj.pokeball[0], usrObj.xp[0], usrObj.berry[0]))
	input("Cliquez sur [Entrée] pour Go back to the main menu")
	return [1, "pass", ""]



def pokProfile_tree(pokObj):
	pokProfileTemplate = "{}\n├── HP: {}\n├── Zone: {}\n├── Experience: {}\n├── Types\n│       └── {}\n├── Moves\n│"
	pokProfileTemplate = pokProfileTemplate.format(pokObj.name[0], pokObj.hp[0], pokObj.zone[0], pokObj.xp[0],\
	 ', '.join(ast.literal_eval(pokObj.type[0])))
	movesEval = ast.literal_eval(pokObj.moves[0])
	movesChunk = [movesEval[i:i+20] for i in range(0, len(movesEval), 20)]
	pokProfileTemplate_moves = ""
	print(pokProfileTemplate)
	for chunk in range(len(movesChunk)):
		for move_ in movesChunk[chunk]:
			pokProfileTemplate_moves += "       ├── {}\n".format(move_)
		print(pokProfileTemplate_moves)
		if chunk-1 == len(movesChunk):
			break
		input("Appuyez sur [Entrée] pour afficher plus de mouvements")




def pokedex_func(*args):
	username = args[1]['username']
	dbSession = orm()
	usrSQL = dbSession.filterBy.get(tablename="user", username=username)[0]
	usrObj = utilisateur(*usrSQL)
	pokedexArr = ast.literal_eval(usrObj.pokedex[0])
	if len(pokedexArr):
		pokObjArr = []
		for pokID in pokedexArr:
			pokSQL = dbSession.filterBy.get(tablename="pokemon", id=pokID)[0]
			pokObjArr.append(pokemon(*pokSQL))
		pyMenus = args[0]['pokedexMenu']
		pyMenus[0]['choices'] = [i.name[0] for i in pokObjArr]
		answers = prompt(pyMenus)
		showPok = [i for i in pokObjArr if answers['currentQ'] == i.name[0]][0]
		pokProfile_tree(showPok)
		input("Cliquez sur [Entrée] pour Go back to the main menu")
		return [1, "pass", ""]
	return [0, "pass", "Pokedex est vide"]



def pokeDetector_func(*args):
	username = args[1]['username']
	dbSession = orm()
	usrSQL = dbSession.filterBy.get(tablename="user", username=username)[0]
	usrObj = utilisateur(*usrSQL)
	myZone = int(usrObj.zone[0])
	pokSQLArr = dbSession.filterBy.get(tablename="pokemon", zone=myZone, state='Wild')

	options, pokObjArr = [], []
	pok_uuid = []
	for pok_ in pokSQLArr:
		pokObj_tmp = pokemon(*pok_)
		pokObjArr.append(pokObj_tmp)
		options.append(pokObj_tmp.name[0])
		pok_uuid.append(pokObj_tmp.id[0])

	usrObj.pokedex[0] = json.dumps(pok_uuid)
	updateObj(usrObj)

	pyMenus_pokArr = args[0]['targetpokeMenu']
	pyMenus_pokArr[0]['choices'] = options

	answers_1 = prompt(pyMenus_pokArr)

	pyMenus_action = args[0]['fightPok']
	answers_2 = prompt(pyMenus_action)
	if answers_2['currentQ'] == 'Info':
		targetPok_ = [i for i in pokObjArr if answers_1['currentQ'] == i.name[0]][0]
		pokProfile_tree(targetPok_)
		input("Cliquez sur [Entrée] pour Go back to the main menu")
		return [1, "pass", ""]

	elif answers_2['currentQ'] == 'Capture':
		targetPok_ = [i for i in pokObjArr if answers_1['currentQ'] == i.name[0]][0]
		usrObj.Capture(targetPok_)
		input("Cliquez sur [Entrée] pour Go back to the main menu")
		return [1, "pass", ""]

	elif answers_2['currentQ'] == 'Fight':
		targetPok_ = [i for i in pokObjArr if answers_1['currentQ'] == i.name[0]][0]

		combatObj = combat(userObj=usrObj, enemyPokObj=targetPok_)
		resp = [1, 'pass']
		while resp[0]:
			
			if resp[1] == 'Capture':
				usrObj.Capture(targetPok_)
				if targetPok_.state[0] == 'Not Wild':
					input("Cliquez sur [Entrée] pour Go back to the main menu")
					return [1, "pass", ""]
			elif resp[1] == 'Escape':
				return [1, "pass", "You run out of the fight"]
			elif resp[1] == 'Print':
				print(resp[2])
			elif resp[1] == 'Table':
				fightStats = PrettyTable()
				fightStats.field_names = ['Name', 'Experience', 'Health']
				_  = [fightStats.add_row(r) for r in resp[2]]
				print(fightStats)
			resp = combatObj.call_menus_and_controle_comabt_flow()

		input("Cliquez sur [Entrée] pour Go back to the main menu")
		return [1, "pass", ""]

	else:
		targetPok_ = [i for i in pokObjArr if answers_1['currentQ'] == i.name[0]][0]
		usrObj.Capture(targetPok_)
		input("Cliquez sur [Entrée] pour Go back to the main menu")
		return [1, "pass", ""]


def navigation_func(*args):
	while True:
		username = args[1]['username']
		dbSession = orm()
		usrSQL = dbSession.filterBy.get(tablename="user", username=username)[0]
		usrObj = utilisateur(*usrSQL)
		myZone = int(usrObj.zone[0])
		pokSQLArr = dbSession.filterBy.get(tablename="pokemon")

		options = []
		for pok_ in pokSQLArr:
			pokObj_tmp = pokemon(*pok_)
			options.append(int(pokObj_tmp.zone[0]))

		pokMap = {str(i):str(options.count(i)) for i in range(1, 12)}
		pokMap[str(myZone)] = pokMap[str(myZone)] + '\033[92m'+ " & Me" + '\033[0m'
		baseMap = PrettyTable()

		pokCenter = args[1]['pokCenters']
		for j in range(1, 12 ,4):
			baseMap.add_row(["-----------"]*4)
			baseMap.add_row([pokMap[str(i)] + pokCenter[i-1]  if i<12 else "" for i in range(j, j+4)])
		baseMap = str(baseMap)
		baseMap = baseMap[[i for i, n in enumerate(baseMap) if n == '\n'][2]+1:]
		print(baseMap)


		pyMenus_nav = args[0]['NavigationMenu']
		answers = prompt(pyMenus_nav)
		navDict = {'up': max(myZone-4, 1), 'down': min(myZone+4, 11), 'left': max(1, myZone-1), 'right': min(11, myZone+1)}
		if answers['currentQ'] not in navDict.keys():
			return [1, "pass", ""]
		usrObj.move(navDict[answers['currentQ']])
		resetBanner()


def pokecenter_func(*args):
	username = args[1]['username']
	dbSession = orm()
	usrSQL = dbSession.filterBy.get(tablename="user", username=username)[0]
	usrObj = utilisateur(*usrSQL)
	myZone = int(usrObj.zone[0])

	pokCenter = args[1]['pokCenters']
	if len(pokCenter[myZone-1]):
		pyMenus = args[0]['pokeCenterMenu']
		answers = prompt(pyMenus)
		if answers['currentQ'] in ['Baies', 'pokeballs']:
			quantity_ = [{'type': 'input', 'name': 'purchase',
					'message': 'Enter le nombre de {}'.format(answers['currentQ'])}]
			ansQuantity = prompt(quantity_)
			if answers['currentQ']=='Baies':
				usrObj.shop(num_pokebal=0, num_berry=int(ansQuantity['purchase']))
			else:
				usrObj.shop(num_pokebal=int(ansQuantity['purchase']), num_berry=0)
			time.sleep(2)
		return [1, "pass", ""]
	return [0, "pass", "No Pokecenter is available in this zone"]



def dresseurFight_func(*args):
	username = args[1]['username']
	dbSession = orm()
	usrSQL = dbSession.filterBy.get(tablename="user", username=username)[0]
	usrObj = utilisateur(*usrSQL)
	myZone = int(usrObj.zone[0])

	usrSQLArr = dbSession.filterBy.get(tablename="user")
	dressDict = {}
	for usrSQL in usrSQLArr:
		usrObj = utilisateur(*usrSQL)
		if myZone == int(usrObj.zone[0]) and username != usrObj.username[0]:
			dressDict[usrObj.username[0]] = usrObj


	pyMenus_dressDict = args[0]['targetdressMenu']
	pyMenus_dressDict[0]['choices'] = dressDict.keys()

	answers = prompt(pyMenus_dressDict)

	pok_uuid = ast.literal_eval(dressDict[answers['currentQ']].pokCollection[0])[0]
	pokSQL = dbSession.filterBy.get(tablename="pokemon", id=pok_uuid)[0]
	targetPok_ = pokemon(*pokSQL)


	combatObj = combat(userObj=usrObj, enemyPokObj=targetPok_)
	resp = [1, 'pass']
	while resp[0]:
		
		if resp[1] == 'Capture':
			usrObj.Capture(targetPok_)
			if targetPok_.state[0] == 'Not Wild':
				input("Cliquez sur [Entrée] pour Go back to the main menu")
				return [1, "pass", ""]
		elif resp[1] == 'Escape':
			return [1, "pass", "You run out of the fight"]
		elif resp[1] == 'Print':
			print(resp[2])
		elif resp[1] == 'Table':
			fightStats = PrettyTable()
			fightStats.field_names = ['Name', 'Experience', 'Health']
			_  = [fightStats.add_row(r) for r in resp[2]]
			print(fightStats)
		resp = combatObj.call_menus_and_controle_comabt_flow()
		
	input("Cliquez sur [Entrée] pour Go back to the main menu")
	return [1, "pass", ""]