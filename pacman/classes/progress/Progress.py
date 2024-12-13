class Dir_Path:
    @staticmethod
    def get_base_path():
        if getattr(sys, 'frozen', False): # executable
            return sys._MEIPASS
        else:
            return os.path.dirname(__file__)
class Account: # Session Only Account Storage
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
        
    def register(self):
        pass
    
    def login(self):
        pass
    
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
        
    def get_score(self):
        pass
        
    def insert_score(self):
        pass
    
    def get_scoreboard_data(self):
        return self.local_data
    
class Achievement:
    def __init__(self):
        self.LOCAL_DATA={}
        self.DATA_PATH=os.path.join(Dir_Path.get_base_path(),'..','..','data','achievement.json')

class Save_Database:
    pass

class Load_Database:
    pass