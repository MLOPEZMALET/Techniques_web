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
def update_data(category, new_data, path, data_number=None):
    with open(path, "r") as read_file:
        data = json.load(read_file)

        if data_number is None:
            for i in data["contributions"]["data"]:
                i[category] = new_data
        else:
            data["contributions"]["data"][data_number][category] = new_data
    with open(path, "w") as jsonFile:
        json.dump(data, jsonFile, indent=3)


# Supprime une contribution de Data
def delete_data(data_number, path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        del data["contributions"]["data"][data_number]
    with open(path, "w") as jsonFile:
        json.dump(data, jsonFile, indent=3)


# Chemin relatif vers la BD JSON
path_all = "../Data/DONNEES_CLIENT.json"
# Liste des clés nécessaires au bon formatage des données JSON
required_write_keys = ['public_id', 'dico_id', 'user_id', 'user_name', 'article_id', 'contrib_type', 'contrib_data', 'contrib_path', 'contrib_name', 'ntealan', 'validate', 'last_update']
required_update_keys = ["field", "data_number", "new_data"]
required_delete_keys = ["data_number"]

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

#update_data("user_name", "BARGIER", path_read, path_write, -1)

#__TEST_DELETING____

#delete_data(path_all, 1)
