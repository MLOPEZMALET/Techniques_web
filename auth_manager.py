import json

path_users = "./data/AUTH_USERS.json"


def read_data(path):
    with open(path, "r") as f:
        data = json.load(f)
        return data


print(read_data(path_users))
