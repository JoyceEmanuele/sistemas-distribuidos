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

def GetRange(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = list(stub.GetRange(mensagem))
    return resposta

def DelRange(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    resposta = list(stub.DelRange(mensagem))
    return resposta

if __name__ == '__main__':
    
    ''' exemplo para testar o get, put, del, putall, getall, delall e trim
    
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
    '''

 #   ''' exemplo para testar o getrange e delrange

    steamputall = [];
    mensagem9 = project_pb2.KeyValueRequest(key="chave", val="valor1")
    steamputall.append(mensagem9)
    mensagem10 = project_pb2.KeyValueRequest(key="chave", val="valor2")
    steamputall.append(mensagem10)
    mensagem = project_pb2.KeyValueRequest(key="chave1", val="valor1")
    steamputall.append(mensagem)
    mensagem1 = project_pb2.KeyValueRequest(key="chave1", val="valor2")
    steamputall.append(mensagem1)
    mensagem2 = project_pb2.KeyValueRequest(key="chave1", val="valor3")
    steamputall.append(mensagem2)
    mensagem3 = project_pb2.KeyValueRequest(key="chave2", val="valor1")
    steamputall.append(mensagem3)
    mensagem4 = project_pb2.KeyValueRequest(key="chave2", val="valor2")
    steamputall.append(mensagem4)
    mensagem7 = project_pb2.KeyValueRequest(key="chave4", val="valor1")
    steamputall.append(mensagem7)
    mensagem8 = project_pb2.KeyValueRequest(key="chave4", val="valor2")
    steamputall.append(mensagem8)
    mensagem5 = project_pb2.KeyValueRequest(key="chave3", val="valor1")
    steamputall.append(mensagem5)
    mensagem6 = project_pb2.KeyValueRequest(key="chave3", val="valor2")
    steamputall.append(mensagem6)

    resposta = PutAll(steamputall)

    #mensagemfrom = project_pb2.KeyRequest(key="chave1", ver=2)
    #mensagemto = project_pb2.KeyRequest(key="chave3")

    mensagemfrom = project_pb2.KeyRequest(key="chave1")
    mensagemto = project_pb2.KeyRequest(key="chave3")

    mensagem = project_pb2.KeyRange(fr=mensagemfrom, to=mensagemto)

    #resposta = GetRange(mensagem)
    resposta = DelRange(mensagem)


    print("Resposta do servidor: \n", resposta)
#   '''
