import sys
import grpc
import project_pb2
import project_pb2_grpc

def Put(message, port):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    response = stub.Put(message)
    return response

def Get(message, port):
    try:
        channel = grpc.insecure_channel('localhost:' + port)
        stub = project_pb2_grpc.KeyValueStoreStub(channel)
        response = stub.Get(message)
        return response
    except Exception as erro:
        print(f'Erro: {erro}')
        return []


def Del(message, port):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    response = stub.Del(message)
    return response

def PutAll(message, port):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    response = list(stub.PutAll(iter(message)))
    return response

def GetAll(message, port):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    response = list(stub.GetAll(iter(message)))
    return response

def DelAll(message, port):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    response = list(stub.DelAll(iter(message)))
    return response

def Trim(message, port):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    response = stub.Trim(message)
    return response

def GetRange(message, port):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    response = list(stub.GetRange(message))
    return response

def DelRange(message, port):
    channel = grpc.insecure_channel('localhost:' + port)
    stub = project_pb2_grpc.KeyValueStoreStub(channel)
    response = list(stub.DelRange(message))
    return response

def getKeyAndValueFromUser():
    key = input('Input the key: ')
    value = input('Input the value: ')
    return (key, value)

def getKeyFromUser():
    key = input('Input the key: ')
    return key

def getManyKeysFromUser():
    key = input('Input the keys separated by space: ')
    return list(key.split(' '))

def getManyKeysAndVersionsFromUser():
    keys = input('Input the keys separated by space: ')
    keys = list(keys.split(' '))
    version = input('Input the versions separated by space (use -1 to last version): ')
    version = list(version.split(' '))
    
    if(len(keys) != len(version)):
        raise ValueError('Number of keys must be equal number of version.')
    
    for value in version:
        try:
            int_value = int(value)
            if int_value < -1 or int_value == 0:
                raise ValueError('Number of versions must be -1 to last version or an natural number')
        except ValueError:
            print("One or more versions inputed are not numbers")

    
    keysAndVersion = list(zip(keys, list(map(lambda e: int(e), version))))
    return keysAndVersion

def getManyKeysAndValuesFromUser():
    keys = input('Input the keys separated by space: ')
    keys = list(keys.split(' '))
    values = input('Input the values separated by space: ')
    values = list(values.split(' '))
    
    if(len(keys) != len(values)):
        raise ValueError('Number of keys must be equal number of values.')
    
    keysAndValues = list(zip(keys, values))
    return keysAndValues

if __name__ == '__main__':
    port_ = '50051' if len(sys.argv) <= 1 else sys.argv[1]
    print('Client started, conected to '+ port_+' port')
    
    client_request = '-1'
    while client_request != '10':
        print('\n ------------------------------------ ')
        print('|            CLIENT PORTAL             |')
        print(' ------------------------------------- ')
        print('|  1. Get                              |')
        print('|  2. Get Range                        |')
        print('|  3. Get All                          |')
        print('|  4. Put                              |')
        print('|  5. Put All                          |')
        print('|  6. Del                              |')
        print('|  7. Del Range                        |')
        print('|  8. Del All                          |')
        print('|  9. Trim                             |')
        print('|  10. Exit                            |')
        print(' ------------------------------------- ')
        print('\nChoose an option: ', end='')
        client_request = input()
        
        print()

        if client_request == '1': # Get
            key = getKeyFromUser()
            message = project_pb2.KeyRequest(key=key)
            response = Get(message, port_)
            print()
            print(response)
        
        elif client_request == '2': # GetRange
            try:
                print('Input two keys and values ​​below')
                keysAndVersions = getManyKeysAndVersionsFromUser()
                if(len(keysAndVersions) != 2):
                    print('Number of keys and velues must be 2! OPERATION ABORTED!')
                    break
                
                messageFromTo = []
                for key, version in keysAndVersions:
                    if version == -1:
                        messageFromTo.append(project_pb2.KeyRequest(key=key))
                    else:
                        messageFromTo.append(project_pb2.KeyRequest(key=key, ver=version))
                message = project_pb2.KeyRange(fr=messageFromTo[0], to=messageFromTo[1])
                response = GetRange(message, port_)
                print(response)
            except ValueError as err:
                print(f'Error: {err}')
                print('OPERATION ABORTED!')

        elif client_request == '3': # GetAll
            steamgetall = [];
            try:
                keysAndVersions = getManyKeysAndVersionsFromUser()
                for key, version in keysAndVersions:
                    if version == -1:
                        message = project_pb2.KeyRequest(key=key)
                    else:
                        message = project_pb2.KeyRequest(key=key, ver=version)
                    steamgetall.append(message)
                response = GetAll(steamgetall, port_)
                print(response)
            except ValueError as err:
                print(f'Error: {err}')
                print('OPERATION ABORTED!')
        
        elif client_request == '4': # Put
            key, value = getKeyAndValueFromUser()
            message = project_pb2.KeyValueRequest(key=key, val=value)
            response = Put(message, port_)
            print()
            print(response)
        
        elif client_request == '5': # PutAll
            steamputall = []
            try:
                keysAndValues = getManyKeysAndValuesFromUser()
                for key, value in keysAndValues:
                    message = project_pb2.KeyValueRequest(key=key, val=value)
                    steamputall.append(message)
                response = PutAll(steamputall, port_)
                print(response)
            except ValueError as err:
                print(f'Error: {err}')
                print('OPERATION ABORTED!')
        
        elif client_request == '6': # Del
            key = getKeyFromUser()
            message = project_pb2.KeyRequest(key=key)
            response = Del(message, port_)
            print()
            print(response)
        
        elif client_request == '7': # Del Range
            try:
                print('Input two keys and values ​​below')
                keysAndVersions = getManyKeysAndVersionsFromUser()
                if(len(keysAndVersions) != 2):
                    print('Number of keys and velues must be 2! OPERATION ABORTED!')
                    break
                
                messageFromTo = []
                for key, version in keysAndVersions:
                    if version == -1:
                        messageFromTo.append(project_pb2.KeyRequest(key=key))
                    else:
                        messageFromTo.append(project_pb2.KeyRequest(key=key, ver=version))
                message = project_pb2.KeyRange(fr=messageFromTo[0], to=messageFromTo[1])
                response = DelRange(message, port_)
                print(response)
            except ValueError as err:
                print(f'Error: {err}')
                print('OPERATION ABORTED!')
        
        elif client_request == '8': # Del All
            steamdelall = []
            try:
                keys = getManyKeysFromUser()
                for key in keys:
                    message = project_pb2.KeyRequest(key=key)
                    steamdelall.append(message)
                response = DelAll(steamdelall, port_)
                print(response)
            except ValueError as err:
                print(f'Error: {err}')
                print('OPERATION ABORTED!')
        
        elif client_request == '9': # Trim
            key = getKeyFromUser()
            message = project_pb2.KeyRequest(key=key)
            response = Trim(message, port_)
            print()
            print(response)
        
        elif client_request == '10': # Sair
            exit()
