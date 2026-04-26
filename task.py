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
    def id(self)->int:
        return self.__id
    @property
    def text(self)->str:
        return self.__text
    @property
    def done(self)->bool:
        return self.__done
    @property
    def reminderDatetime(self)->datetime:
        return self.__reminderDatetime
    @property
    def reminded(self)->bool:
        return self.__reminded
    @property
    def user_id(self)->int:
        return self.__user_id
   
    @done.setter
    def done(self,done:bool):
        self.__done=done
    @text.setter
    def text(self,text:str):
        self.__text=text
    @id.setter
    def id(self,id:int):
        self.__id=id
    @reminderDatetime.setter
    def reminderDatetime(self,reminderDatetime:datetime):
        self.__reminderDatetime=reminderDatetime
    @reminded.setter
    def reminded(self,reminded:bool):
        self.__reminded=reminded
    @user_id.setter
    def user_id(self,user_id:int):
        self.__user_id=user_id
 
    