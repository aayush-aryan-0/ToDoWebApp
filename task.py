class Task:
    __text=""
    __done=False
    def __init__(self,text,done):
        self.__text=text
        self.__done=done
    @property
    def text(self):
        return self.__text
    @property
    def done(self):
        return self.__done
    @done.setter
    def done(self,done):
        self.__done=done
    @done.setter
    def text(self,text):
        self.__text=text
    