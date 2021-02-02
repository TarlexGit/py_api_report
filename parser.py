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
        bytes_stream.write("{name} <{email}> {date}\n".format(name=str_name, email = str_email, date=str_date_time))
        
        all_tasks_values = get_tasks(user.id, tasks_data)
        compile_tasks = [x['title'] for x in all_tasks_values if x['completed'] == True] 
        not_compile_tasks = [x['title'] for x in all_tasks_values if x['completed'] == False] 
        
        bytes_stream.write("Всего задач: {done}\n\nЗавершённые задачи ({comp}):\n".format(done=len(all_tasks_values), comp=len(compile_tasks)))
        compile_tasks_list=[f'{x}\n' for x in compile_tasks]
        bytes_stream.write("".join(map(str, compile_tasks_list)))

        not_compile_tasks_list=[f'{x}\n' for x in not_compile_tasks]
        z="".join(map(str, not_compile_tasks_list))
        bytes_stream.write("\nОставшиеся задачи ({x}):\n{z}".format(x=len(not_compile_tasks), z=z))

        self.create_file(bytes_stream.getvalue())
        
        bytes_stream.close()

    def create_file(self, data):
        file_path='tasks/'+self.username+'.txt'  
        try:
            if os.path.isfile(file_path) == True:
                new_name_file = read_time(self.username)  
                print(file_path,' -> ' ,new_name_file)
                os.rename(file_path, new_name_file)
                print('---- rename done ')
            else: print('file doesnot exist')
            f = open('tasks/'+self.username+'.txt', 'w')
            print('create '+ self.username+'.txt', 'w')
            f.write(data)
            f.close() 
            print(' Create DONE ')
        except:
            # return state 
            print('!@(&!)@*$&!)@&)@# -------------- EXSEPT')
            new_name_file = read_time(self.username) 
            os.remove(file_path)
            os.rename(new_name_file, file_path) 

             
def read_time(username):
    file_path='tasks/'+ username +'.txt'
    check_file = os.path.isfile(file_path)
    data_form_file = open(file_path,'r')  
    line1, line2 = data_form_file.readline(), data_form_file.readline() 
    params = line2.split(' ')
    str_dt = '{data} {time}'.format(data = params[-1][:5],time =params[-2][:10])
    print(str_dt)
    
    dt = datetime.datetime.strptime(str_dt, "%H:%M %d.%m.%Y")

    new_name_file = 'tasks/old_{user_name}_{data}.txt'.format(user_name=username,
    data = dt.strftime("%Y-%m-%dT%H:%M")) 
    return new_name_file

def get_tasks(user_id, tasks_data):  
    count = [] 
    for item in tasks_data: 
        try:
            for key, value in item.items():
                if item['userId']==user_id and item not in count: 
                    count.append(item)  
                else:pass 
        except:pass 
    return count

          
if __name__ == "__main__":   
    print('api connection') 
    users_url = 'https://json.medrating.org/users'
    users_request = requests.get(url=users_url)
    users_data = users_request.json() # сохраняем от сбоев сети 
 
    tasks_url = 'https://json.medrating.org/todos'
    tasks_request = requests.get(url=tasks_url)
    tasks_data = tasks_request.json()

    print('reporting...')   
    for u in users_data: 
        try:
            user = UserHandler(u)
            user.make_data()
            print(' ')  
        except AttributeError: pass
    print('completed') 
        
