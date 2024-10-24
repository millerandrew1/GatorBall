import socket

#Client side script for example with BT connection

def client_init():
    global client
    client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    client.connect(("60:e9:aa:2c:92:ee", 4))

def client_send():
    try:
        while True:
            message = input("Enter Location: ")
            client.send(message.encode('utf-8'))
            #data = client.recv(1024)
            #if not data:
                #break
            #print(f"Message: {data.decode('utf-8')}")
        
    except OSError as e:
        pass

def client_close():
    client.close()

client_init()
client_send()
client_close()
