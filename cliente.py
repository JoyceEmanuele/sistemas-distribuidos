import grpc
import project_pb2
import project_pb2_grpc

def Put(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = stub.Put(mensagem)
    return resposta

def Get(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = stub.Get(mensagem)
    return resposta

def Del(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = stub.Del(mensagem)
    return resposta

def PutAll(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = list(stub.PutAll(iter(mensagem)))
    return resposta

def GetAll(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = list(stub.GetAll(iter(mensagem)))
    return resposta

def DelAll(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = list(stub.DelAll(iter(mensagem)))
    return resposta

def Trim(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = stub.Trim(mensagem)
    return resposta

if __name__ == '__main__':
    mensagem = project_pb2.KeyValueRequest(key="chave", val="valor1")
    resposta = Put(mensagem)
    mensagem = project_pb2.KeyValueRequest(key="chave", val="valor2")
    resposta = Put(mensagem)
    mensagem = project_pb2.KeyValueRequest(key="chave", val="valor3")
    resposta = Put(mensagem)
    mensagem = project_pb2.KeyValueRequest(key="chave", val="valor4")
    resposta = Put(mensagem)
    mensagem = project_pb2.KeyValueRequest(key="chave1", val="valor1")
    resposta = Put(mensagem)
    mensagem = project_pb2.KeyRequest(key="chave")
    resposta = Get(mensagem)
    mensagem = project_pb2.KeyRequest(key="chave1")
    resposta = Del(mensagem)

    steamputall = [];
    mensagem = project_pb2.KeyValueRequest(key="chave5", val="valor1")
    steamputall.append(mensagem)
    mensagem1 = project_pb2.KeyValueRequest(key="chave5", val="valor2")
    steamputall.append(mensagem1)
    mensagem2 = project_pb2.KeyValueRequest(key="chave6", val="valor1")
    steamputall.append(mensagem2)

    resposta = PutAll(steamputall)

    steamgetall = [];
    mensagem = project_pb2.KeyRequest(key="chave")
    steamgetall.append(mensagem)
    mensagem1 = project_pb2.KeyRequest(key="chave5", ver=1)
    steamgetall.append(mensagem1)
    mensagem2 = project_pb2.KeyRequest(key="chave6", ver=2)
    steamgetall.append(mensagem2)

    resposta = GetAll(steamgetall)

    steamdellall = [];
    #mensagem = project_pb2.KeyRequest(key="chave")
    #steamdellall.append(mensagem)
    mensagem1 = project_pb2.KeyRequest(key="chave6")
    steamdellall.append(mensagem1)

    resposta = DelAll(steamdellall)

    mensagem = project_pb2.KeyRequest(key="chave")
    resposta = Trim(mensagem)

    print("Resposta do servidor: \n", resposta)


