from .models import Topic, Folder
from string import punctuation

#Auth helper functions
def check_pw_conditions(pw):
    symbol = False
    capital = False 
    number = False
    symbols = list(punctuation)
    capitals = [chr(i) for i in range(65, 91)]
    numbers = [str(i) for i in range(0, 10)]
    for i in pw:
        if i in symbols:
            symbol = True 
        if i in capitals:
            capital = True 
        if i in numbers:
            number = True 
        
        if symbol and capital and number:
            return True 
    return False

def valid_email(email):
    if "@" not in email:
        return False 
    email = email.split("@")
    if len(email) != 2:
        return False
    
    if "." not in email[1]:
        return False 
    
    if not email[0] or not email[1]:
        return False 

    after_at = email[1].split(".")
    if not after_at[0] or not after_at[1]:
        return False
    return True

#Topic and folder helper functions
def check_user(userid, folderid=None, topic_id=None):
    if folderid:
        folder = Folder.query.filter_by(id=folderid).first()
        if not folder or folder.userid != userid:
            return False
    else:
        topic = Topic.query.filter_by(id=topic_id).first()
        folder = Folder.query.filter_by(id=topic.folderid).first()
        if not topic or not folder or folder.userid != userid:
            return False 
    return True

def verify_topic(userid, topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    folder = Folder.query.filter_by(id=topic.folderid).first()
    if not topic or not folder or folder.userid != userid:
        return False 
    return True