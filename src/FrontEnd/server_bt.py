import socket

def server_init():
    global server 
    server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    server.bind(("60:e9:aa:2c:92:ee", 4)) #address of current machine should be used, this is for Josh's laptop as example
    server.listen(1) #number of ports to use for communication, for now just one but actual would use 2 for each anchor

    global client
    global addr

    client, addr = server.accept()
def recv_message(): # get a and b from client
    #global data
    global a 
    global b
    try:
        while True:
            #get a
            data = client.recv(1024)
            if not data:
                break
            print(f"Message: {data.decode('utf-8')}")
            a = int(data.decode('utf-8'))

            # again for b
            data = client.recv(1024)
            if not data:
                break
            print(f"Message: {data.decode('utf-8')}")
            b = int(data.decode('utf-8'))


            print(a, b)
            #message = input("Enter message: ")
            #client.send(message.encode('utf-8'))
    except OSError as e:
        pass
def close():
    client.close()
    server.close()

server_init()
recv_message()
close()
