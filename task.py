from datetime import datetime
class Task:
    def __init__(self,id:int=None,text:str="",reminderDatetime:datetime="",done:bool=False,reminded:bool=False,user_id:int=None):
        self.__id=id
        self.__text=text
        self.__reminderDatetime=reminderDatetime
        self.__reminded=reminded
        self.__done=done
        self.__user_id=user_id
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
    def user_id(self):
        return self.__user_id
   
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
    @user_id.setter
    def user_id(self,user_id):
        self.__user_id=user_id
 
    