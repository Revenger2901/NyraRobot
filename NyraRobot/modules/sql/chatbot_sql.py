import threading

from sqlalchemy import Column, String

from NyraRobot.modules.sql import BASE, SESSION



class NyraChats(BASE):
    __tablename__ = "nyra_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

NyraChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_nyra(chat_id):
    try:
        chat = SESSION.query(NyraChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()

def set_nyra(chat_id):
    with INSERTION_LOCK:
        nyrachat = SESSION.query(NyraChats).get(str(chat_id))
        if not nyrachat:
            nyrachat = NyraChats(str(chat_id))
        SESSION.add(nyrachat)
        SESSION.commit()

def rem_nyra(chat_id):
    with INSERTION_LOCK:
        nyrachat = SESSION.query(NyraChats).get(str(chat_id))
        if nyrachat:
            SESSION.delete(nyrachat)
        SESSION.commit()
