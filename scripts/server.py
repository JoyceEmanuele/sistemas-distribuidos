# grpc and system needed imports
import sys
import time
import grpc
import project_pb2
import project_pb2_grpc

from cachetools import LRUCache
from concurrent import futures


import json
import random
import socket


global socketDB

def setReplica():
    numSocket = random.randint(10001,10003)

    try:
        hostName = socket.gethostname()

        socketDB = socket.socket()
        socketDB.settimeout(1)

        socketDB.connect((hostName, numSocket))

        print(f'Server started, connected to DB server on port {numSocket}')

    except:
        print('Erro na criacao das particoes')
        sys.exit()
        
    return socketDB


def timestamp_in_miliseconds():
    # Get timestamp in seconds
    timestamp_in_seconds = time.time()
    # Convert seconds in miliseconds
    timestamp_in_miliseconds = int(timestamp_in_seconds * 1000)
    return timestamp_in_miliseconds

class KeyValueStore(project_pb2_grpc.KeyValueStoreServicer):
    def __init__(self) -> None:
        self.socket = setReplica()

    def Put(self, request, context):
        chave = request.key
        valor = request.val
        print(request)

        socket = self.socket

        msg = json.dumps({'function':'read', 'key':chave, 'value':None})
        try:
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            resposta = json.loads(resposta.decode())
        except:
            print(f'Erro ao consultar chave')
            return None

        if resposta.get('data') is None:
            print(f'Erro ao inserir chave')
            return None 
        
        if resposta['data'] != '':
            valores = resposta['data']
            versao_request = timestamp_in_miliseconds()
            
            msg = json.dumps({'function':'delete', 'key':chave, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            msg = json.dumps({'function':'insert', 'key':chave, 'value': valores + [(valor, versao_request)]})
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            
            return project_pb2.PutReply(
                key=chave, old_val=valores[-1][0], old_ver= valores[-1][1], ver=versao_request
            )

        else:
            versao_request = timestamp_in_miliseconds()

            msg = json.dumps({'function':'insert', 'key':chave, 'value':[(valor, versao_request)]})
            socket.send(msg.encode())
            resposta = socket.recv(2048)

            return project_pb2.PutReply(
                key=chave, old_val='', old_ver=0, ver=versao_request
            )

    def Get(self, request, context):
        chave = request.key
        print(f'Get {chave} key')

        socket = None
        socket = self.socket
        
        msg = json.dumps({'function':'read', 'key':chave, 'value':None})
        try:
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            resposta = json.loads(resposta.decode())
        except:
            print(f'Erro ao consultar chave')
            return None
        
        print(resposta)

        if resposta.get('data') is None:
            print(f'Erro ao consultar chave')
            return None 
    
        if resposta['data'] == '':
            print(f'Chave \'{chave}\' não existe')
        else:
            valores = resposta['data']
            if(request.ver): 
                versao = int(request.ver)
                for valor, valor_versao in reversed(valores):
                    if int(valor_versao) <= versao:
                        valor_final = valor
                        versao = valor_versao
                        break
            else:
                versao = valores[-1][1]
                valor_final = valores[-1][0]
            return project_pb2.KeyValueVersionReply(
                key=chave, val=valor_final, ver=versao
            ) 

    def Del(self, request, context):
        chave = request.key
        print(f'Get {chave} key')

        socket = None
        socket = self.socket
        
        msg = json.dumps({'function':'read', 'key':chave, 'value':None})
        try:
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            resposta = json.loads(resposta.decode())
        except:
            print(f'Erro ao consultar chave')
            return None
            
        if resposta['data'] == '':
            print(f'Chave \'{chave}\' não existe')
            return project_pb2.KeyValueVersionReply(
                key='', val='', ver=0
            )
        else:
            valores = resposta['data']
            versao = valores[-1][1]
            valor = valores[-1][0]

            msg = json.dumps({'function':'delete', 'key':chave, 'value':None})
            socket.send(msg.encode())
            resposta = socket.recv(2048)

            return project_pb2.KeyValueVersionReply(
                key=chave, val=valor, ver=versao
            )

    def PutAll(self, request, context):
        print('PutAll')
        respostas = []
        for tupla in request:
            res = self.Put(tupla,context)
            respostas.append(res)
        return iter(respostas)
    
    def GetAll(self, request, context):
        print('GetAll')

        respostas = []

        maiorver = 0
        tuplas = []
        for tupla in request:
            if maiorver < tupla.ver:
                maiorver = tupla.ver
            tuplas.append(tupla)
        
        for tupla in tuplas:
            if tupla.ver:
                socket = None
                socket = self.socket
                msg = json.dumps({'function':'read', 'key':tupla.key, 'value':None})
                try:
                    socket.send(msg.encode())
                    resposta = socket.recv(2048)
                    resposta = json.loads(resposta.decode())
                except:
                    print(f'Erro ao consultar chave')
                    return None
                print(resposta)
                for valor, valor_versao in reversed(resposta['data']):
                        if valor_versao <= maiorver:
                            resposta = project_pb2.KeyValueVersionReply(
                            key=tupla.key, val=valor, ver=valor_versao
                            )
                            respostas.append(resposta)
            else:
                res = self.Get(tupla,context)
                respostas.append(res)
        return iter(respostas)
    
    def DelAll(self, request, context):
        print('DelAll')
        respostas = []
        for tupla in request:
            res = self.Del(tupla,context)
            respostas.append(res)
        return iter(respostas)
    
    def Trim(self, request, context):
        chave = request.key
        chaveresponse = project_pb2.KeyRequest(key=chave)
        res = self.Get(chaveresponse,context)
        if res != None:

            versao = res.ver
            valor = res.val

            self.Del(chaveresponse,context)

            socket = self.socket
            msg = json.dumps({'function':'insert', 'key':chave, 'value': [(valor, versao)]})
            socket.send(msg.encode())

            return res
        else: print(f'{chave} nao existe')
    
    def GetRange(self, request, context):
        print('GetRange')

        socket = None
        socket = self.socket
        
        msg = json.dumps({'function':'get_all_data', 'key':None, 'value':None})
        try:
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            respostabanco = json.loads(resposta.decode())
            print(respostabanco)
        except:
            print(f'Erro ao executar o getrange das chave')
            return None

        chavefr = request.fr.key
        chaveto = request.to.key
        versaofr = request.fr.ver
        versaoto = request.to.ver

        if versaofr >= versaoto: versao = versaofr
        else: versao = versaoto

        chaves_ordenadas = sorted(respostabanco['all_data'])

        respostas = []
        
        for chave in chaves_ordenadas:
            if chave >= chavefr and chave <= chaveto:
                valores = respostabanco['all_data'][chave]
                print(valores)
                if not versao: 
                    resposta = project_pb2.KeyValueVersionReply(
                    key=chave, val=valores[-1][0], ver=valores[-1][1]
                    )
                    respostas.append(resposta)
                else: 
                    for valor, valor_versao in reversed(valores):
                        if valor_versao <= versao:
                            resposta = project_pb2.KeyValueVersionReply(
                            key=chave, val=valor, ver=valor_versao
                            )
                            respostas.append(resposta)
        
        return iter(respostas)

    def DelRange(self, request, context):
        print('DelRange')

        socket = None
        socket = self.socket
        
        msg = json.dumps({'function':'get_all_keys', 'key':None, 'value':None})
        try:
            socket.send(msg.encode())
            resposta = socket.recv(2048)
            respostabanco = json.loads(resposta.decode())
            print(respostabanco)
        except:
            print(f'Erro ao executar o getrange das chave')
            return None

        chavefr = request.fr.key
        chaveto = request.to.key

        chaves_ordenadas = sorted(respostabanco['all_data'])
        print(chaves_ordenadas)

        respostas = []

        for chave in chaves_ordenadas:
            if chave >= chavefr and chave <= chaveto:
                mensagem = project_pb2.KeyRequest(key=chave)
                resposta = self.Del(mensagem,context)
                respostas.append(resposta)
        
        return iter(respostas)

def serve(port_):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    project_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStore(), server)
    server.add_insecure_port('[::]:' + port_)
    server.start()
    print('Server started, listening on '+ port_)
    return(server)
    

if __name__ == '__main__':

    port_ = '50051' if len(sys.argv) <= 1 else sys.argv[1]

    server = serve(port_)
    server.wait_for_termination()
