import json

path_users = "./data/AUTH_USERS.json"


def read_data(path):
    with open(path, "r") as f:
        data = json.load(f)
        return data

def add_user(new_data, path):
    #if new_data
    data = read_data(path)
    data.append(new_data)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)



print(read_data(path_users)["user_name"])
