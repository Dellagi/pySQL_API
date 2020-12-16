import requests, json


class ApiClass:

    def __init__(self, base_url="https://pokeapi.co/api/v2/"):
        self.base_url = base_url

    def loadDB(self, limit):
        r = requests.get(self.base_url + "/pokemon/?limit={}".format(limit))
        respDict = json.loads(r.content)['results']
        return respDict

    def get_move(self, move_name):
        req = requests.get(self.base_url + 'move/' + move_name + '/')
        m = req.json()
        i=0
        while 1:
            if move_json["names"][i]["language"]["name"]=="fr":
                break
            i+=1
        dict_move = {'name': move_json["names"][i]["name"], 'accuracy': m["accuracy"]}
        return dict_move

    def get_pokemon(self, pok_name):
        req = requests.get(self.base_url + 'pokemon/' + pok_name + '/')
        m = req.json()
        list_types=[]
        for i in range(len(m["types"])):
            list_types.append(m["types"][i]["type"]["name"])
        list_moves = []
        for i in range(len(m["moves"])):
            list_moves.append(m["moves"][i]["move"]["name"])
        dict_pok = { 'name': m["name"], 'types': list_types, 'moves': list_moves}
        return dict_pok
