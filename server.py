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
    
    def Get(self, request, context):
        print("get")
        chave = request.key
        if chave in self.cache:
            valores = self.cache[chave]
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
                
        else: print("chave não existe")

    def Del(self, request, context):
        print("get")
        chave = request.key
        if chave in self.cache:
            valores = self.cache[chave]
            versao = valores[-1][1]
            valor = valores[-1][0]
            resposta = project_pb2.KeyValueVersionReply(
                key=chave, val=valor, ver=versao
            )
            del self.cache[chave]
            print(self.cache)
            return resposta
        else: print("chave não existe")

    def PutAll(self, request, context):
        print("PutAll")
        respostas = []
        for tupla in request:
            res = self.Put(tupla,context)
            respostas.append(res)
        print(self.cache)
        return iter(respostas)
    
    def GetAll(self, request, context):
        print("GetAll")
        respostas = []
        for tupla in request:
            res = self.Get(tupla,context)
            respostas.append(res)
        print(self.cache)
        return iter(respostas)
    
    def DelAll(self, request, context):
        print("DelAll")
        respostas = []
        for tupla in request:
            res = self.Del(tupla,context)
            respostas.append(res)
        print(self.cache)
        return iter(respostas)
    
    def Trim(self, request, context):
        chave = request.key
        if chave in self.cache:
            valores = self.cache[chave]
            self.cache[chave] = [valores[-1]]
            versao = valores[-1][1]
            valor = valores[-1][0]
            resposta = project_pb2.KeyValueVersionReply(
                    key=chave, val=valor, ver=versao
                )
            print(self.cache)
            return resposta
        else: print("chave não existe")
    
    def GetRange(self, request, context):
        print("GetRange")

        chavefr = request.fr.key
        chaveto = request.to.key
        versaofr = request.fr.ver
        versaoto = request.to.ver

        if versaofr >= versaoto: versao = versaofr
        else: versao = versaoto

        chaves_ordenadas = sorted(self.cache.keys())
        print(chaves_ordenadas)

        respostas = []

        for chave in chaves_ordenadas:
            if chave >= chavefr and chave <= chaveto:
                valores = self.cache[chave]
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
        print("DelRange")

        chavefr = request.fr.key
        chaveto = request.to.key

        chaves_ordenadas = sorted(self.cache.keys())
        print(chaves_ordenadas)

        respostas = []

        for chave in chaves_ordenadas:
            if chave >= chavefr and chave <= chaveto:
                mensagem = project_pb2.KeyRequest(key=chave)
                resposta = self.Del(mensagem,context)
                respostas.append(resposta)

        print(self.cache)
        
        return iter(respostas)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    project_pb2_grpc.add_KeyValueStoreServicer_to_server(
        KeyValueStore(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
