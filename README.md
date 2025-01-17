
# **Projeto de Sistemas Distribuídos**

**Aluno 01: Huryel Souto Costa - 12011BCC022**

**Aluno 02: Joyce Emanuele Oliveira Silva - 11721BCC010**

## **Especificação do Trabalho**
O projeto segue a seguinte especificação: [especificação.](https://github.com/JoyceEmanuele/sistemas-distribuidos/blob/main/project-specifications.md)
Ademais, é um projeto desenvolvido pelos alunos supracitados como parte dos requisitos para a aprovação da disciplina de Sistemas Distribuídos da Graduação em Ciência da Computação da Universidade Federal de Uberlândia (UFU).

# **Etapa 01**
## **Instruções de compilação**
### **Dependências**
O projeto foi desenvolvido utilizando a linguagem **Python** na versão **3.8.10**, utilizando o **pip** na versão **23.2.1** e o sistema operacional Linux Mint na versão **20.3**. É necessário, então, que você tenha uma versão similar o mais atualizada para conseguir rodar o projeto. Outrossim, foi necerrária a instalação de algumas bibliotecas para contruir o projeto, a seguir será descrito os comandos e as bibliotecas utilizadas no processo:
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

**ATENÇÃO:** é possível instalar o pip e as demais dependências apenas executando o `compile.sh`, na raiz do projeto, através do comando:
```
sh compile.sh
```

### **Inicialização e Uso de clientes e servidores.**
Importante: os servidores devem sempre ser iniciados antes dos clientes que se conectam a eles! Além disso, os servidores devem ser iniciados em portas diferentes, assim como os clientes!

#### **Servidores**
Há duas formas de iniciar os servidores. A primeira é executando o servidor na porta padrão, que é a **50051**. Para isso basta executar o seguinte comando na raiz do projeto:
```
$ sh server.sh
```
Caso seja de desejo do usuário executar um servidor em uma porta específica, basta executar o seguinte comando (substituindo "PORTA" pelo número da porta desejada):
```
$ sh server.sh PORTA
```
Após isso, os servidor(es) estadão disponíveis e oferecendo os serviços de acordo com as especificações do projeto.

#### **Clientes**
Há duas formas, também, de iniciar os clientes. A primeira é executando o cliente conectado no servidor da porta padrão, que é a **50051**. Para isso basta executar o seguinte comando na raiz do projeto:
```
$ sh client.sh
```
Caso seja de desejo do usuário executar um cliente que seja conectado a um outro servidor de uma porta específica, basta executar o seguinte comando (substituindo "PORTA" pelo número da porta do servidor desejado):
```
$ sh client.sh PORTA
```
Após isso, os clientes(es) estarão disponíveis e oferecendo os serviços de acordo com as especificações do projeto.

### **Dificuldades e detalhamento dos requisitos implementados e não implementados**
Foram implementados todos os requisitos de acordo com as especificações do projeto. Além disso, pode-se citar como a principal dificuldade a gestão do dicionário que armazena as informações em cada servidor, em relação à sua atualização e consistência com o dos demais servidores. Em outras palavras, fazer vários servidores trabalharem com vários clientes e qualquer cliente conectado em qualquer servidor ser capaz de obter e manipular informações corretas, foi a principal adversidade do trabalho

### **Formato dos Dicionários usados para armazenar os dados**
```
{
    'chave1': [(valor1, versão1), ..., (valorN, versãoN)],
    'chave2': [(valor1, versão1), ..., (valorM, versãoM)],
    ...
    'chaveK': [(valor1, versão1), ..., (valorP, versãoP)],
}
```
### **Vídeo do funcionamento do projeto e documento de testes**
Para assistir ao vídeo mostrando o funcionamento do projeto e o atendimento dos requisitos basta [clicar aqui](https://www.youtube.com/watch?v=v-qcq7t14eU). Para acessar o documento contendo os testes realizados no projeto basta [clicar aqui](https://github.com/JoyceEmanuele/sistemas-distribuidos/blob/main/testes-projeto-sd.pdf) ou acessar o PDF na raiz do projeto.

### **Refeências**
- [Web Article: GRPC Quick start
](https://grpc.io/docs/languages/python/quickstart/)
- [Video Tutorial: Create a gRPC Client and Server in Python](https://www.youtube.com/watch?v=WB37L7PjI5k)
- [Web Article: How to Use MQTT in Python with Paho Client](https://www.emqx.com/en/blog/how-to-use-mqtt-in-python)


# **Etapa 02**
## **Instruções de compilação**
### **Dependências**
O projeto foi desenvolvido utilizando a linguagem **Python** na versão **3.8.10**, utilizando o **pip** na versão **23.2.1** e o sistema operacional Linux Mint na versão **20.3**. É necessário, então, que você tenha uma versão similar o mais atualizada para conseguir rodar o projeto. Outrossim, foi necerrária a instalação de algumas bibliotecas para contruir o projeto, a seguir será descrito os comandos e as bibliotecas utilizadas no processo:
- **Plyvel interface to LevelDB**
    ```
    $ pip install plyvel 
    ```
- **PySyncObj**
    ```
    $ pip install pysyncobj
    ```

**ATENÇÃO:** é possível instalar o pip e as demais dependências apenas executando o `compile.sh`, na raiz do projeto, através do comando:
```
sh compile.sh
```

### **Inicialização e Uso de Clientes, Servidores e os Bancos de Dados.**
Importante: Os bancos de Dados devem ser os primeiros a serem iniciados e os servidores devem sempre ser iniciados antes dos clientes que se conectam a eles! Além disso, os servidores devem ser iniciados em portas diferentes, assim como os clientes!

#### **Bancos de Dados**
Para executar os bancos basta rodar o segunte comando:

```
$ sh database.sh NUM_DATABASE
```
Há três réplicas do banco de dados que podem ser iniciadas, dessa forma o argumento **"NUM_DATABASE"** pode possuir os valores 1, 2 e 3 (que correspondem, respectivamente à replica do banco de dados a ser inicializada).

#### **Servidores**
Há duas formas de iniciar os servidores. A primeira é executando o servidor na porta padrão, que é a **50051**. Para isso basta executar o seguinte comando na raiz do projeto:
```
$ sh server.sh
```
Caso seja de desejo do usuário executar um servidor em uma porta específica, basta executar o seguinte comando (substituindo "PORTA" pelo número da porta desejada):
```
$ sh server.sh PORTA
```
Após isso, os servidor(es) estadão disponíveis e oferecendo os serviços de acordo com as especificações do projeto.

#### **Clientes**
Há duas formas, também, de iniciar os clientes. A primeira é executando o cliente conectado no servidor da porta padrão, que é a **50051**. Para isso basta executar o seguinte comando na raiz do projeto:
```
$ sh client.sh
```
Caso seja de desejo do usuário executar um cliente que seja conectado a um outro servidor de uma porta específica, basta executar o seguinte comando (substituindo "PORTA" pelo número da porta do servidor desejado):
```
$ sh client.sh PORTA
```
Após isso, os clientes(es) estarão disponíveis e oferecendo os serviços de acordo com as especificações do projeto.

### **Dificuldades e detalhamento dos requisitos implementados e não implementados**
Foram implementados todos os requisitos de acordo com as especificações do projeto. Além disso, pode-se citar como a principal dificuldade a implementação do banco de dados distribuído, uma vez que sincronizar as réplicas foi uma advercidade inicial que, posteriormente, foi superada.

### **Formato dos Dicionários usados para armazenar os dados**
```
{
    'chave1': [(valor1, versão1), ..., (valorN, versãoN)],
    'chave2': [(valor1, versão1), ..., (valorM, versãoM)],
    ...
    'chaveK': [(valor1, versão1), ..., (valorP, versãoP)],
}
```
### **Vídeo do funcionamento do projeto e documento de testes**
Para assistir ao vídeo mostrando o funcionamento do projeto e o atendimento dos requisitos basta [clicar aqui](https://drive.google.com/file/d/1sLpBK0MYKQdR0Dlm_ge1SvTlE2DWu-zx/view?usp=sharing). Para acessar o documento contendo os testes realizados no projeto basta [clicar aqui](https://github.com/JoyceEmanuele/sistemas-distribuidos/blob/main/Sistemas-distribuídos-parte2.pdf) ou acessar o PDF na raiz do projeto.

### **Refeências**
- [Web Article: GRPC Quick start
](https://grpc.io/docs/languages/python/quickstart/)
- [Video Tutorial: Create a gRPC Client and Server in Python](https://www.youtube.com/watch?v=WB37L7PjI5k)
- [Plyvel User Guide](https://plyvel.readthedocs.io/en/latest/user.html#getting-started)
- [PySyncObj Documentation](https://github.com/bakwc/PySyncObj/tree/master)





