import sys
import os
import json
class Dir_Path:
    @staticmethod
    def get_base_path():
        if getattr(sys, 'frozen', False): # executable
            return sys._MEIPASS
        else:
            return os.path.dirname(__file__)
        
class Save_Database:
    @staticmethod
    def save_data(instance):
        with open(instance.DATA_PATH,'w') as f:
            json.dump(instance.LOCAL_DATA, f, indent=2)
    
class Load_Database:
    @staticmethod
    def load_data(instance):
        if os.path.exists(instance.DATA_PATH):
            with open(instance.DATA_PATH, 'r') as f:
                instance.LOCAL_DATA = json.load(f)
        else:
            instance.LOCAL_DATA = {}

class Account(): # Session Only Account Storage
    """
    not an actual account but a Save Data to be precise
    user_data=[
        {
            "username":"admin",
            "score":0,
            "level":1,
            "difficulty":"easy",
            "current_level_data":{},
        },
        {
            "username":"admin",
            "score":0,
            "level":1,
            "difficulty":"easy",
            "current_level_data":{},
        }
    ]
    """
    def __init__(self):
        self.LOCAL_DATA={}
        self.DATA_PATH=os.path.join(Dir_Path.get_base_path(),'..','..','data','account.json')
        
    def register(self,username,data):
        self.LOCAL_DATA[username]={}
        self.LOCAL_DATA[username]['level']=data['level']
        self.LOCAL_DATA[username]['score']=0
        self.LOCAL_DATA[username]['difficulty']=data['difficulty'].__members__.keys()
        self.LOCAL_DATA[username]['current_level_data']=data
        Save_Database.save_data(self)
    
    def load(self,username):
        return self.LOCAL_DATA.get(username)
    
    def delete(self):
        pass
    
    def get_account_data(self):
        return self.LOCAL_DATA
    
class Scoreboard:
    """
    "User":{
        "level":1,
        "score":0,
    },
    "User2":{
        "level":3,
        "score":4044,
    }
    """
    def __init__(self):
        self.LOCAL_DATA={}
        self.DATA_PATH=os.path.join(Dir_Path.get_base_path(),'..','..','data','scoreboard.json')
        
    def get_scoreboard(self):
        ranking=[]
        for user in self.LOCAL_DATA:
            # print(f"User: {user} Level: {self.LOCAL_DATA[user]['level']} Score: {self.LOCAL_DATA[user]['score']}")
            ranking.append((str(user),self.LOCAL_DATA[user]['level'],self.LOCAL_DATA[user]['score']))
        ranking.sort(key=lambda x: x[2], reverse=True)
        return ranking[:5]
    
    def insert_score(self, username, score, level):
        self.LOCAL_DATA[username]={}
        self.LOCAL_DATA[username]['level']=level
        self.LOCAL_DATA[username]['score']=score
    
    def get_scoreboard_data(self):
        return self.local_data
    
class Achievement:
    def __init__(self):
        self.LOCAL_DATA={}
        self.DATA_PATH=os.path.join(Dir_Path.get_base_path(),'..','..','data','achievement.json')