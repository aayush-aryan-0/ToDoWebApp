class Task:
    def __init__(self,text:str=None,id:int=None,done:bool=False):
        self.__id=id
        self.__text=text
        self.__done=done
    @property
    def id(self):
        return self.__id
    @property
    def text(self):
        return self.__text
    @property
    def done(self):
        return self.__done
    @done.setter
    def done(self,done):
        self.__done=done
    @text.setter
    def text(self,text):
        self.__text=text
    @id.setter
    def id(self,id):
        self.__id=id
    