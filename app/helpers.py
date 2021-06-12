from .models import Topic, Folder
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