import grpc
import project_pb2
import project_pb2_grpc

def Put(mensagem):
    channel = grpc.insecure_channel('localhost:50051')
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    #print(mensagem)
    resposta = stub.Put(mensagem)
    #print(resposta)
    return resposta

if __name__ == '__main__':
    mensagem = project_pb2.KeyValueRequest(key="chave1", val="valor6")
    resposta = Put(mensagem)
    print("Resposta do servidor: \n", resposta)

