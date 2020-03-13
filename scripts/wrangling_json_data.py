import json


# Renvoie les données du JSON
def read_data(path):
    with open(path, "r") as f:
        data = json.load(f)
        data = data["contributions"]["data"]
        return data


# Ajoute une contribution à la suite des données JSON (une nouvelle valeur dans la liste dont la clé est Data).
def write_data(new_data, path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        data["contributions"]["data"].append(new_data)
    with open(path, "w") as write_file:
        json.dump(data, write_file, indent=3)


# Ecrit des nouvelles valeurs dans un champ déterminé
def update_data(category, new_data, path, data_number):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        tracker = False
        for i in range(len(data["contributions"]["data"])):
            if data["contributions"]["data"][i]["public_id"] == data_number:
                data["contributions"]["data"][i][category] = new_data
                print(data["contributions"]["data"][i][category])
                tracker = True
                break
            else:
                continue
        if tracker == True:
            with open(path, "w") as jsonFile:
                json.dump(data, jsonFile, indent=3)
        else:
            raise ValueError("wrong ID")



# Supprime une contribution de Data
def delete_data(data_number, path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        tracker = False
        for i in range(len(data["contributions"]["data"])):
            if data["contributions"]["data"][i]["public_id"] == data_number:
                data["contributions"]["data"].pop(i)
                tracker = True
                break
            else:
                continue
        if tracker == True:
            with open(path, "w") as jsonFile:
                json.dump(data, jsonFile, indent=3)
        else:
            raise ValueError("wrong ID")

def match_data(field, value, path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        tracker = False
        res = []
        for i in range(len(data["contributions"]["data"])):
            if data["contributions"]["data"][i][field] == value:
                res.append(data["contributions"]["data"][i])
                print(res)
                tracker = True
            else:
                continue
        if tracker == True:
            return res
        else:
            return None


# Chemin relatif vers la BD JSON
path_all = "../data/DONNEES_CLIENT.json"
# Liste des clés nécessaires au bon formatage des données JSON
required_write_keys = ['user_name', 'contrib_type', 'contrib_data', 'contrib_path', 'contrib_name', 'ntealan', 'validate', 'last_update']
# other 'public_id', , 'user_id', 'article_id',
required_update_keys = ["field", "data_number", "new_data"]
required_delete_keys = ["public_id"]

# ________________________________________TESTING________________________________

# ____TEST_READING

#db = read_data(path_all)

#sample = db[0]
#print(db[0])
#print(db[-1])


# ___TEST_WRITING

#write_data(sample, path_all)

#db_1 = read_data(path_all)
#print(db_1[-1])
# ___TEST_UPDATING

# update_data("user_name", "BARGIER", path_all, "885980e9-d559-4b9c-8878-4d63aed4cebb")

#__TEST_DELETING____

# delete_data("8ad93a62-9437-416f-93c6-948a2c15b45b", path_all)

#__TEST MATCHING__

match_data("user_name", "lko", path_all)
