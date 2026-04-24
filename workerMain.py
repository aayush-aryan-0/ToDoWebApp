from threading import Thread
from reminder import reminder

Thread(target=reminder,daemon=True).start()