import requests
import json
import os
import errno 
import datetime
import io 
from collections import Counter


try:
    os.makedirs('tasks')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

class UserHandler:
    def __init__( self, dict ):
        vars(self).update( dict )  

    def make_data(self):
        bytes_stream = io.StringIO()

        str_company = self.company
        str_name = self.name
        str_email = self.email
        today = datetime.datetime.now()
        str_date_time = today.strftime("%d.%m.%Y %H:%M")

        bytes_stream.write("Отчёт для {company}.\n".format(company=str_company["name"]))
        bytes_stream.write("{name} <{email}> {date}".format(name=str_name, email = str_email, date=str_date_time))
        
        tasks_values = get_tasks(user.id, tasks_data)
        print(tasks_values)

        self.create_file(bytes_stream.getvalue())
        
        bytes_stream.close()

    def create_file(self, data):
        f = open('tasks/'+self.username+'.txt', 'w')
        f.write(data)
        f.close() 
             
def get_tasks(user_id, tasks_data):  
    count = [] 
    for item in tasks_data: 
        for key, value in item.items():
            if key=='userId' and value==user_id: 
                count.append(item['completed'] ) 
    return Counter(count)

          
if __name__ == "__main__":    
    users_url = 'https://json.medrating.org/users'
    users_request = requests.get(url=users_url)
    users_data = users_request.json() # сохраняем от сбоев сети 
 
    tasks_url = 'https://json.medrating.org/todos'
    tasks_request = requests.get(url=tasks_url)
    tasks_data = tasks_request.json()

    for u in users_data: 
        try:
            user = UserHandler(u)
            print(user.username)   
            user.make_data()
            
        except AttributeError: pass
        
