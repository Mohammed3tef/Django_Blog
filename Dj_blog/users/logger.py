import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def log(msg):
    f=open(os.path.join(BASE_DIR,"logging/logging.info"),"a")
    f.write(msg+"\n")
    f.close()