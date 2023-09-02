# Cliente para una sala de chat
import socket
import sys
import time
from threading import Thread

class Listener(Thread):
    '''Hilo que implementa un canal de comunicación entre el servidor
    que proporciona el servicio de una sala de chat y el cliente actual'''

    DATA_SIZE = 1024    # 1 kilobyte para recibir datos

    def __init__(self, sock):
        self.sock = sock  # Este es el socket que se conecta al servidor
        Thread.__init__(self) # Inicializa el hilo

    def run(self):
        while True:
            # Tendremos que utilizar la variable self.sock para recibir mensajes
            # del servidor (correspondientes a otros usuarios) y sacarlos por pantalla
            
            #Primero recibimos los datos del servidor del tamaño de DATA_SIZE usando el socket
            #self.sock.recv(self.DATA_SIZE) 
            
            while True:
                #Bucle para esperar los mensajes del servidor
                try:
                    data = self.sock.recv(self.DATA_SIZE).decode() 
                
                #imprimimos los datos recibidos solo cuando no estén vacíos
                    
                        
                    if data != "":
                        #imprimimos un salto de línea para que no se mezclen los mensajes
                        print("\n")
                        print(data)
                        print("\n")
                        print("Introduzca un mensaje para enviar: ")
                    
                    
                except:
                    print("Se ha salido de la conexion")
                    break
                  
              
                

            #Imprimimos los datos recibidos
            #print("Mensaje recibido: " + self.DATA_SIZE)
            

class ChatClient:
    '''Cliente para el servidor de una sala de chat'''

    def __init__(self, address, port, nickname):
        self.address = address
        self.port = port
        self.nickname = nickname
        self.sock = socket.socket()

    def setup_sock(self):
        '''Inicializa el socket creado en el constructor'''
        # Aquí se debe utilizar el socket creado arriba para conectarse al servidor
        # Completar...

        #Conectamos el socket al servidor
        try:
            self.sock.connect((address, port))
        except:
            print("No se pudo conectar al servidor")
            #Si no se puede conectar, salimos del programa controlando la excepción
            

        print("Conectado al servidor, escriba un mensaje para enviarlo")

        hilo = Listener(self.sock)  # Creamos el hilo para escuchar al servidor
        hilo.start()  # Iniciamos el hilo
       

    def run(self):
        self.setup_sock()
        while True:
            # En este lazo vamos a hacer lo siguiente de forma indefinida;
            #   1) Pedir al usuario del programa que introduzca texto por teclado
            #   2) Utilizar el socket para enviar el texto al servidor (no olvidar el alias)
            #   3) Contemplar la salida del programa (ctrl + c, teclear 'exit', etc.)
            # Si se sale del lazo, cerrar el socket

            try:

                mensaje_a_enviar = input("Introduzca un mensaje para enviar: \n")
            
            #Comprobar que el mensaje no es mayor de 1024 bytes
            # while len(mensaje_a_enviar) > 8192: # 1024 * 8 
            #     print("El mensaje es demasiado largo, no se puede enviar")
            #     mensaje_a_enviar = input("Introduzca un mensaje para enviar de menor tamaño: ")
                
                mensaje = self.nickname + " - " + time.strftime("%d/%m/%Y %H:%M:%S") + " :" + mensaje_a_enviar
            #Usar el socket para enviar el mensaje al servidor incluyendo la fecha y hora usando time.strftime
                self.sock.send(mensaje.encode())

            #Si el mensaje es exit, salimos del programa
                if mensaje_a_enviar == "exit":
                    print("Saliendo del programa")
                    self.sock.close()
                    break
                    

            except KeyboardInterrupt:
                #si se pulsa ctrl + c, desconectamos el socket
                self.sock.close()
                break

 
                
        
             
                


if __name__ == '__main__':
    # Sugerencia: sustituir los siguientes valores hard-ooded por argumentos
    # que se pasen por la línea de órdenes (sys.argv) como aprendimos
    # al principio del curso
    print("------------- Bienvenido al chat -------------")
    address = '127.0.0.1'
    port = 8888
    nickname = input("Introduzca su nickname: ")
    client = ChatClient(address, port, nickname)
    client.run()
