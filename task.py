from datetime import datetime
class Task:
    def __init__(self,id:int=None,text:str="",reminderDatetime:datetime="",done:bool=False,reminded:bool=False,username:str=""):
        self.__id=id
        self.__text=text
        self.__reminderDatetime=reminderDatetime
        self.__reminded=reminded
        self.__done=done
        self.__username=username
    @property
    def id(self):
        return self.__id
    @property
    def text(self):
        return self.__text
    @property
    def done(self):
        return self.__done
    @property
    def reminderDatetime(self):
        return self.__reminderDatetime
    @property
    def reminded(self):
        return self.__reminded
    @property
    def username(self):
        return self.__username
   
    @done.setter
    def done(self,done):
        self.__done=done
    @text.setter
    def text(self,text):
        self.__text=text
    @id.setter
    def id(self,id):
        self.__id=id
    @reminderDatetime.setter
    def reminderDatetime(self,reminderDatetime):
        self.__reminderDatetime=reminderDatetime
    @reminded.setter
    def reminded(self,reminded):
        self.__reminded=reminded
    @username.setter
    def username(self,username):
        self.__username=username
 
    