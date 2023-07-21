from typing import Union
from toml import load
from util.path import conjoin
import openai

class Chat:
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'

    def __init__(self, session: str, config: Union[tuple, str] = ('toml', '/config.toml')) -> None:
        self.session = session
        self.conversation = []

        if type(config) == tuple: config = conjoin(*config)
        self.config = config

        with open(self.config, 'r') as file:
            self.attributes = load(file)
        
        self.api_key = self.attributes['openai']['api_key']
        openai.api_key = self.api_key
        
        self.model = self.attributes['openai']['model']
        self.max_tokens = self.attributes['openai']['max_tokens']

        self.system_statement = self.attributes['openai'][Chat.SYSTEM]['statement']
        self.__add__(role = Chat.SYSTEM, content = self.system_statement)
    
    def __add__(self, role: str, content: str) -> None:
        self.conversation.append({'role': role, 'content': content})

    def ask(self, user: str) -> tuple[str, int]:
        self.__add__(role = Chat.USER, content = user)
        response = openai.ChatCompletion.create(
            model = self.model,
            max_tokens = self.max_tokens,
            messages = self.conversation
        )
        assistant_content = response['choices'][-1]['message']['content']
        tokens = response['usage']['total_tokens']
        return (assistant_content, tokens)