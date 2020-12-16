# -*- coding: utf-8 -*-

from api.pokAPI import ApiClass
from business_objects.pokemon import pokemon
from business_objects.user import utilisateur
from orm.simpleDB import orm
from random import shuffle
from menu.menuClass import menu
from mytools.poktools import *



eval_answers = {'Exit': 'exit_func', 'Sign up': 'signup_func', 'Login': 'signin_func',\
'Check you PokeDex': 'pokedex_func', 'Go to the PokeCenter': 'pokecenter_func', 'Navigation': 'navigation_func',
'Show the pokemons in my zone': 'pokeDetector_func', 'Fight a trainer': 'dresseurFight_func', 'Check my portfolio': 'portfolio_func',
'Disconnect': 'logout_func', 'My pokemon collection': 'myPokColl_func'}


pokCenter = '\033[91m'+ " & Center" + '\033[0m'
pokCenterArr = ['', '', '', pokCenter, '', '', '', '', pokCenter, '', '']

state_manager = {'username': '', 'connected': False, 'currentMenu': 'Menu1', 'currentNotice': '', 'pokCenters': pokCenterArr}




def init_DB():
	from tqdm import tqdm
	sys.stdout.write('\033[92m' + "\r" + "[!] Loading ..." + '\033[0m' + '\n')

	APIsession = ApiClass()
	for pok_ in tqdm(APIsession.loadDB(120)):
		pokInfo = APIsession.get_pokemon(pok_['name'])
		pokObj = pokemon(name=pok_['name'], typeArrayStr=json.dumps(pokInfo['types']), movesArrStr=json.dumps(pokInfo['moves']), xp=randint(100, 2000), zone=randint(1, 11))
		dbSession = orm(pokObj)
		dbSession.add()
	print("[!] Pokemons were added to the database")

	dressNames = ['Michael', 'Christopher', 'Jessica', 'Matthew', 'Ashley', 'Jennifer', 'Joshua', 'Amanda', 'Daniel', 'David', 'James', 'Robert', 'John', 'Joseph', 'Andrew', 'Ryan', 'Brandon', 'Jason', 'Justin', 'Sarah', 'William', 'Jonathan', 'Stephanie', 'Brian', 'Nicole', 'Nicholas', 'Anthony', 'Heather', 'Eric', 'Elizabeth', 'Adam', 'Megan', 'Melissa', 'Kevin', 'Steven', 'Thomas']
	dbSession = orm()
	pokSQL = dbSession.filterBy.get(tablename="pokemon")[:len(dressNames)]
	shuffle(pokSQL)
	for d in range(len(dressNames)):
		pokCollectionStr = json.dumps([pokSQL[d][0]])
		userObj = utilisateur(dressNames[d].lower(), "fauxCompte", coin=100, zone=randint(1, 11), xp=1500, pokeball=randint(0, 20), berry=randint(0, 20), pokCollectionStr=pokCollectionStr,pokedex='[]')
		dbSession = orm(userObj)
		dbSession.add()

	print("[!] Fake trainers are added to the database")






resetBanner()
if not os.path.isfile(orm.db_name):
	init_DB()
	time.sleep(2)
	resetBanner()




menuObj = menu()

while True:
	print(state_manager['currentNotice'])
	pyMenus = menuObj.getMenus()
	answers = prompt(pyMenus[state_manager['currentMenu']])
	resp = eval(eval_answers[answers['currentQ']] + '(pyMenus, state_manager)')
	if resp[0]:
		state_manager['currentNotice'] = '\033[92m' + "\r" + resp[2] + '\033[0m' + '\n'
	elif len(resp[2]):
		state_manager['currentNotice'] = '\033[91m' + "\r" + resp[2] + '\033[0m' + '\n'
	else:
		state_manager['currentNotice'] = '\033[91m' + "\r" + "Failed operation" + '\033[0m' + '\n'
	exec(resp[1])
	resetBanner()

