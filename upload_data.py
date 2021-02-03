import json
import requests
import os
import errno


try:
    os.makedirs('data')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

response_users = requests.get(url="https://json.medrating.org/users")
response_todos = requests.get(url="https://json.medrating.org/todos") 

users_data = response_users.json()
todos_data = response_todos.json()
 
with open("data/users.json", "w") as data_file: 
    json.dump(users_data, data_file,indent=4)

with open("data/todos.json", "w") as data_file: 
    json.dump(todos_data, data_file, indent=4)

print('done')