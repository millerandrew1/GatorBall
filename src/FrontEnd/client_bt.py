import socket

#Client side script for example with BT connection

def client_init():
    global client
    client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client.connect(("60:e9:aa:2c:92:ee", 4))

def client_send():
    try:
        while True:
            start = client.recv(1024)

            if not start:
                break
            elif (start.decode('utf-8') == "Go"):

                message = input("Enter Distance From A: ")
                client.send(message.encode('utf-8'))
            
                message2 = input("Enter Location: ")
                client.send(message2.encode('utf-8'))
            
                data = client.recv(1024)
                if not data:
                    break
                elif (int(data.decode('utf-8')) == 1):
                    continue
                else:
                    break
            else:
                continue
        
    except OSError as e:
        pass

def client_close():
    client.close()

client_init()
client_send()
client_close()
