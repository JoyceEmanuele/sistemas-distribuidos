
# **Projeto de Sistemas Distribuídos**
**Aluno 01: Huryel Souto Costa - 12011BCC022**
**Aluno 02: Joyce - XXXXXBCCYYY**

## **Especificação do Trabalho**
O projeto segue a seguinte especificação: [Especificação.](https://github.com/JoyceEmanuele/sistemas-distribuidos/blob/main/project-specifications.md)
Ademais, é um projeto desenvolvido pelos alunos supracitados como parte dos requisitos para a aprovação da disciplina de Sistemas Distribuídos da Graduação em Ciência da Computação da Universidade Federal de Uberlândia (UFU).

## **Etapa 01**
### **Instruções de compilação**
#### **Dependências**
O projeto foi desenvolvido utilizando a linguagem **Python** na versão **3.8.10**, utilizando o **pip** na versão **23.2.1** e o sistema operacional Linux Mint na versão **20.3**. Outrossim, foram necerrária a instalação de algumas bibliotecas para contruir o projeto, a seguir será descrito os comandos e as bibliotecas utilizadas no processo:
- **Cache Tools**
    ```
    $ pip install cachetools 
    ```
- **GRPC**
    ```
    $ pip install grpcio-tools
    ```
- **Paho MQTT**
    ```
    $ ppip3 install paho-mqtt
    ```
    Foi utilizado um broker gratúito, público e online para o MQTT: `broker.emqx.io`
#### **Inicialização e Uso de clientes e servidores.**
Importante: os servidores devem sempre ser iniciados antes dos clientes que se conectam a eles! Além disso, os servidores devem ser iniciados em portas diferentes, assim como os clientes!

##### **Servidores**
Há duas formas de iniciar os servidores. A primeira é executando o servidor na porta padrão, que é a **50051**. Para isso basta executar o seguinte comando na raiz do projeto:
```
$ python3 server.py
```
Caso seja de desejo do usuário executar um servidor em uma porta específica, basta executar o seguinte comando (substituindo "PORTA" pelo número da porta desejada):
```
$ python3 server.py PORTA
```
Após isso, os servidor(es) estadão disponíveis e oferecendo os serviços de acordo com as especificações do projeto.

##### **Clientes**
Há duas formas, também, de iniciar os clientes. A primeira é executando o cliente conectado no servidor da porta padrão, que é a **50051**. Para isso basta executar o seguinte comando na raiz do projeto:
```
$ python3 client.py
```
Caso seja de desejo do usuário executar um cliente que seja conectado a um outro servidor de uma porta específica, basta executar o seguinte comando (substituindo "PORTA" pelo número da porta do servidor desejado):
```
$ python3 client.py PORTA
```
Após isso, os clientes(es) estarão disponíveis e oferecendo os serviços de acordo com as especificações do projeto.

#### **Dificuldades é detalhamento dos requisitos implementados e não implementados**
Foram implementados todos os requisitos de acordo com as especificações do projeto. Além disso, pode-se citar como a principal dificuldade a gestão do dicionário que armazena as informações em cada servidor, em relação à sua atualização e consistência com o dos demais servidores. Em outras palavras, fazer vários servidores trabalharem com vários clientes e qualquer cliente conectado em qualquer servidor ser capaz de obter e manipular informações corretas, foi a principal adversidade do trabalho

#### **Formato dos Dicionários usados para armazenar os dados**
```
{
    'chave1': [(valor1, versão1), ..., (valorN, versãoN)],
    'chave2': [(valor1, versão1), ..., (valorM, versãoM)],
    ...
    'chaveK': [(valor1, versão1), ..., (valorP, versãoP)],
}
```
#### **Vídeo de exemplo do funcionamento do projeto**
...

#### **Refeências**
- [Web Article: GRPC Quick start
](https://grpc.io/docs/languages/python/quickstart/)
- [Video Tutorial: Create a gRPC Client and Server in Python](https://www.youtube.com/watch?v=WB37L7PjI5k)
- [Web Article: How to Use MQTT in Python with Paho Client](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)






