import socket
import threading

host = '127.0.0.1'
port = 49999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

print("Servidor de Redes WOW!")
print(f"[Host : Puerto de ejecución] : {host}:{port}")

clients = []
usernames = []
# Función para enviar un mensaje a todos los clientes
def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                message_with_line=(message.decode('utf-8') + '\n').encode('utf-8')
                client.send(message_with_line)
            except:
                # Manejo de errores si no se puede enviar el mensaje
                client.close()
                remove_client(client)
                break;


# Función para manejar la desconexión del cliente
def remove_client(client):
    if client in clients:
        index = clients.index(client)
        username = usernames[index]
        broadcast(f"El usuario: {username} se ha desconectado.\n".encode('utf-8'))
        clients.remove(client)
        usernames.remove(username)
        client.close()



# Función para manejar los mensajes de cada cliente
def handle_messages(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            
            # Manejar comandos especiales
            if message.startswith('/listar'):
                send_user_list(client)
            elif message.startswith('/quitar'):
                remove_client(client)
                break
            else:
                broadcast( message.encode('utf-8'),client)
        except:
            remove_client(client)
            break

# Función para enviar la lista de usuarios conectados a un cliente
def send_user_list(client):
    user_list = "\n".join(usernames)
    client.send(f"Usuarios conectados:\n{user_list}\n".encode('utf-8'))


def receive_connections():
    while True:
        client, address = server.accept()

        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode('utf-8','replace')

        clients.append(client)  # Corregido: Se estaba añadiendo la lista 'clients' en lugar del 'client'
        usernames.append(username)

        print(f"{username} se ha unido a través de {str(address)}")

        message = f"El usuario: {username} se ha unido al chat".encode("utf-8")
        broadcast(message, client)
        client.send("Conexión exitosa al servidor".encode("utf-8"))

        thread = threading.Thread(target=handle_messages, args=(client,))
        thread.start()

receive_connections()
