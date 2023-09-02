# Servidor para una sala de chat

import socket
 

from threading import Thread


class Listener(Thread):
    '''Hilo que implementa un canal de comunicación con uno de los clientes
    conectados al servidor de la sala de chat'''

    DATA_SIZE = 1024    # 1 kilobyte para recibir datos

    def __init__(self, chat_server, conn, client_address):
        
        self.chat_server = chat_server
        self.sock = conn
        self.client = client_address
        Thread.__init__(self) # Inicializa el hilo

   
                
                
    def run(self):
        # Tendremos que utilizar la variable self.sock para recibir mensajes
        # del usuario conectado por dicho canal, y una vez que tengamos
        # un mensaje, difundirlo a todos los demás usuarios (implementando
        # el método broadcast de la clase ChatServer, ver más abajo)
        # Cuando ya esté recibiendo datos, habrá que encapsular la instrucción
        # dentro de un bloque try-except para sacar a ese usuario del
        # conjunto de usuarios conectados que tiene el servidde Seror
        while True:
            try:
                message = self.sock.recv(1024).decode()
                print(message)
                for sock in self.chat_server.client_socks:
                    print(sock + "\n")
                    print(self.sock + "\n")
                    if sock != self.sock:
                        try:
                            self.chat_server.broadcast(sock, message)
                        except:
                            # Se produjo una excepción al enviar el mensaje
                            # a uno de los clientes, por lo tanto, lo eliminamos
                            
                            self.chat_server.client_socks.remove(sock)
            
            except:
                print("Se ha desconectado el usuario " + str(self.client))
                sock.close()
                self.chat_server.client_socks.remove(self.sock)
                break
               
                

class ChatServer:
    '''Servidor de una sala de chat'''
    

    def __init__(self, address, port, max_users):
        self.address = address
        self.port = port
        self.max_users = max_users  # Cuantos clientes admite
        self.sock = socket.socket()
        self.client_socks = [] # Lista de sockets de los clientes conectados
        

    def setup_sock(self):
        '''Inicializa el socket creado en el constructor'''
        # La siguiente llamada nos permite reutilizar sock
        # para abrir más de una conexión sin tener que esperar a otra
        # que se haya abierto previamente mediante el mismo recurso
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.address,self.port))
        self.sock.listen(self.max_users)
    
   
        
    def broadcast(self, sock, msg):
        '''Difunde el mensaje recibido a todos los usuarios conectados'''
        
        #Compueba que el socket no esté vacío y que el mensaje no esté vacío, para evitar errores
        if sock != "" and msg != "":
            print("Enviando mensaje")
            sock.send(msg.encode())

    def run(self):
        '''Arranca el servicio y acepta conexiones de clientes indefinidamente'''
        self.setup_sock()
    
        while True:
            # Aceptar una conexión nueva
            conn, client_address = self.sock.accept()
            # Echar dicha conexión a la saca
            self.client_socks.append(conn)
            print("Se ha aceptado la conexion de " + str(client_address))
            # Lanzar un nuevo hilo instanciando la clase Listener
            listener = Listener(self, conn, client_address)
            listener.start()


if __name__ == '__main__':
    # Sugerencia: sustituir los siguientes valores hard-ooded por argumentos
    # que se pasen por la línea de órdenes (sys.argv) como aprendimos
    # al principio del curso
    address = '127.0.0.1'
    port = 8888
    max_users = 10
    server = ChatServer(address, port, max_users)
    server.run()

