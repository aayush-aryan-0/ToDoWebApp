class Task:
    __task=""
    __done=False
    def __init__(self,task,done):
        self.__task=task
        self.__done=done
    @property
    def task(self):
        return self.__task
    @property
    def done(self):
        return self.__done