# grpc and system needed imports
import sys
import time
import grpc
import project_pb2
import project_pb2_grpc

from cachetools import LRUCache
from concurrent import futures


# mqtt needed imports
import random
import logging

from paho.mqtt import client as mqtt_client


# Create an MQTT Connection

broker = 'broker.emqx.io'
port = 1883
topic = 'python/key-vserions'
client_id = f'python-mqtt-{random.randint(0, 1000)}'

cache_dictionary = LRUCache(maxsize=100)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect, return code %d\n', rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def publish(client, msg):
    result = client.publish(topic, msg)
    status = result[0]

    if status == 0:
        print(f'Send `{msg}` to topic `{topic}`')
    else:
        print(f'Failed to send message to topic {topic}')

def subscribe(client: mqtt_client):    
    def on_message(client, userdata, msg):
        print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')
        
        mensagem = msg.payload.decode().split('-')
        key = mensagem[1]
        
        if mensagem[0] == 'UPDATE_KEY':
            value = mensagem[3]
            version = int(mensagem[6]) if str(mensagem[6]) != 'None' else None
            valuesList = valuesList = list(cache_dictionary[key]) if key in cache_dictionary else []
            valuesList.append((value, version)) 
            cache_dictionary[key] = valuesList
        if mensagem[0] == 'DELETE_KEY':
            del cache_dictionary[key]

        print('New cache')
        print(cache_dictionary)
    client.subscribe(topic)
    client.on_message = on_message


def timestamp_in_miliseconds():
    # Get timestamp in seconds
    timestamp_in_seconds = time.time()
    # Convert seconds in miliseconds
    timestamp_in_miliseconds = int(timestamp_in_seconds * 1000)
    return timestamp_in_miliseconds

class KeyValueStore(project_pb2_grpc.KeyValueStoreServicer):
    # def __init__(self):
    #     # Inicialize o cache de tabela hash (substitua o tamanho conforme necessário)
    #     self.cache = LRUCache(maxsize=100)

    def Put(self, request, context):
        chave = request.key
        valor = request.val
        print(request)

        if chave in cache_dictionary:
            print(f'{chave} is in cache')
            
            valores = cache_dictionary[chave]
            versao_request = timestamp_in_miliseconds()
            valor_request = valores[-1][0]


            resposta = project_pb2.PutReply(
                key=chave, old_val=valor_request, old_ver=versao_request, ver=versao_request
            )

            print(cache_dictionary)
        else:
            print(f'{chave} is not in cache')
            versao_request = timestamp_in_miliseconds()
            valores = []
            resposta = project_pb2.PutReply(
                key=chave, old_val='', old_ver=0, ver=versao_request
            )
            print(cache_dictionary)
        publish(client, f'UPDATE_KEY-{chave}-TO-{valor}-VALUE-IN-{versao_request}-VERSION') 
        return resposta
    
    def Get(self, request, context):
        chave = request.key
        print(f'Get {chave} key')

        if chave in cache_dictionary:
            valores = cache_dictionary[chave]
            if(request.ver): 
                versao = request.ver
                for valor, valor_versao in reversed(valores):
                    if valor_versao <= versao:
                        valor_final = valor
                        versao = valor_versao
                        break
            else:
                versao = valores[-1][1]
                valor_final = valores[-1][0]
            
            resposta = project_pb2.KeyValueVersionReply(
                key=chave, val=valor_final, ver=versao
            )
            
            return resposta
                
        else: print('chave não existe')

    def Del(self, request, context):
        chave = request.key
        print(f'Get {chave} key')

        if chave in cache_dictionary:
            valores = cache_dictionary[chave]
            versao = valores[-1][1]
            valor = valores[-1][0]
            resposta = project_pb2.KeyValueVersionReply(
                key=chave, val=valor, ver=versao
            )

            publish(client, f'DELETE_KEY-{chave}') 

            return resposta
        else: print(f'{chave} does not exist')

    def PutAll(self, request, context):
        print('PutAll')
        respostas = []
        for tupla in request:
            res = self.Put(tupla,context)
            respostas.append(res)
        print(cache_dictionary)
        return iter(respostas)
    
    def GetAll(self, request, context):
        print('GetAll')
        respostas = []
        for tupla in request:
            res = self.Get(tupla,context)
            respostas.append(res)
        print(cache_dictionary)
        return iter(respostas)
    
    def DelAll(self, request, context):
        print('DelAll')
        respostas = []
        for tupla in request:
            res = self.Del(tupla,context)
            respostas.append(res)
        print(cache_dictionary)
        return iter(respostas)
    
    def Trim(self, request, context):
        chave = request.key
        if chave in cache_dictionary:
            valores = cache_dictionary[chave]
            versao = None
            valor = valores[-1][0]
            self.Del(request,context)
            publish(client, f'UPDATE_KEY-{chave}-TO-{valor}-VALUE-IN-{versao}-VERSION')
            resposta = project_pb2.KeyValueVersionReply(
                    key=chave, val=valor, ver=versao
                )
            print(cache_dictionary)
            return resposta
        else: print(f'{chave} does not exist')
    
    def GetRange(self, request, context):
        print('GetRange')

        chavefr = request.fr.key
        chaveto = request.to.key
        versaofr = request.fr.ver
        versaoto = request.to.ver

        if versaofr >= versaoto: versao = versaofr
        else: versao = versaoto

        chaves_ordenadas = sorted(cache_dictionary.keys())
        print(chaves_ordenadas)

        respostas = []

        for chave in chaves_ordenadas:
            if chave >= chavefr and chave <= chaveto:
                valores = cache_dictionary[chave]
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

        chavefr = request.fr.key
        chaveto = request.to.key

        chaves_ordenadas = sorted(cache_dictionary.keys())
        print(chaves_ordenadas)

        respostas = []

        for chave in chaves_ordenadas:
            if chave >= chavefr and chave <= chaveto:
                mensagem = project_pb2.KeyRequest(key=chave)
                resposta = self.Del(mensagem,context)
                respostas.append(resposta)

        print(cache_dictionary)
        
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
    logging.basicConfig()

    port_ = '50051' if len(sys.argv) <= 1 else sys.argv[1]

    server = serve(port_)
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)

    server.wait_for_termination()
