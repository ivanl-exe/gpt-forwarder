from typing import Union
from collections import defaultdict
from time import time
from os import urandom
from base58 import b58encode
from chat import Chat
from util.path import conjoin
from csv import writer

class Boilerplate:
    def __init__(self, request) -> None:
        self.address = request.remote_addr
        self.name = request.remote_user
        self.timestamp = int(time())
        self.response = {}
    
    def add(self, **kwargs) -> None:
        self.response.update(kwargs)

class Server:
    VISITS = 'cumulative_visits'
    TOKENS = 'cumulative_tokens'

    def __init__(self) -> None:
        self.users = defaultdict(lambda: defaultdict(int))
        self.sessions = []
    
    def __id__(prefix: str, n: int = 16) -> str:
        id = b58encode(urandom(n)).decode('UTF-8')
        return f'{prefix}-{id}'

    def new_session() -> str:
        return Server.__id__('s')

    def visit(self, user: str) -> None:
        self.users[user][Server.VISITS] += 1 
    
    def token(self, user: str, n: int) -> None:
        self.users[user][Server.TOKENS] += n

    def usage(self, user: str) -> int:
        return self.users[user]

    def chat(self, boilerplate: Boilerplate, query: dict, log: Union[tuple, str] = ('log', '/usage.csv')) -> dict:
        query = defaultdict(lambda: None, dict(query))
        response = {}

        user_content = query[Chat.USER]
        if query == None: return {}
        response.update({Chat.USER: user_content})

        session = query['session']
        if session == None:
            session = Server.new_session()
        response.update({'session': session})
        for instance in self.sessions:
            if instance.session == session:
                chat = instance
                break
        else:
            chat = Chat(session)
            self.sessions.append(chat)
        
        assistant_content, tokens = chat.ask(user_content)
        user = boilerplate.address
        self.token(user, tokens)
        timestamp = boilerplate.timestamp
        
        if type(log) == tuple: log = conjoin(*log)
        
        fields = [user, tokens, timestamp]
        with open(log, 'a', newline = '') as file:
            csv = writer(file)
            csv.writerow(fields)

        response.update({Chat.ASSISTANT: assistant_content})
        return response