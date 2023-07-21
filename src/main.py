from flask import Flask, request, jsonify
from server import Server, Boilerplate

server = Server()
app = Flask(__name__)

@app.route('/usage')
def usage() -> tuple:
    boilerplate = Boilerplate(request)
    user = boilerplate.address
    
    server.visit(user)
    usage = server.usage(user)
    boilerplate.add(usage=usage)
    return vars(boilerplate)

@app.route('/chat')
def chat() -> tuple:
    boilerplate = Boilerplate(request)
    user = boilerplate.address
    
    server.visit(user)
    usage = server.usage(user)
    boilerplate.add(usage=usage)
    
    query = request.args
    response = server.chat(boilerplate, query)
    boilerplate.add(**response)
    return vars(boilerplate)