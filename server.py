import grpc
from concurrent import futures
import project_pb2
import project_pb2_grpc
from cachetools import LRUCache

class KeyValueStore(project_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        # Inicialize o cache de tabela hash (substitua o tamanho conforme necessário)
        self.cache = LRUCache(maxsize=100)

    def Put(self, request, context):
        chave = request.key
        valor = request.val
        print(request)

        if chave in self.cache:
            print("ta em cache")
            
            valores = self.cache[chave]
            versao_request = valores[-1][1]
            valor_request = valores[-1][0]

            valores.append((valor, versao_request+1))

            self.cache[chave] = valores
            resposta = project_pb2.PutReply(
                key=chave, old_val=valor_request, old_ver=versao_request, ver=versao_request+1
            )

            print(self.cache)
        else:
            print("não ta em cache")
            
            valores = []
            valores.append((valor, 1))
            self.cache[chave] = valores
            resposta = project_pb2.PutReply(
                key=chave, old_val="", old_ver=0, ver=1
            )
            print(self.cache)

        return resposta
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    project_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStore(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
