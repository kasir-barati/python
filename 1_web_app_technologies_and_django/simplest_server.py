from socket import AF_INET
from socket import socket
from socket import SOCK_STREAM
from socket import SHUT_WR

def create_server():
    # Make the phone
    server_socket = socket(AF_INET, SOCK_STREAM)
    try:
        # You say that I wanna have phone calls on port 9000
        server_socket.bind(('localhost', 9000))
        # You ask OS to queue the incoming request if server is busy up to 5
        server_socket.listen(5)
        while True:
            # I am at the phone an it waits forever to have a phone call received
            # .accept is a blocking method
            (client_socket, address) = server_socket.accept()
            rd = client_socket.recv(5000).decode()
            pieces = rd.split('\n')
            if len(pieces) > 0:
                print(pieces[0])

            data = 'HTTP/1.1 200 OK\r\n'
            data += 'Content-Type: text/html; charset=utf-8\r\n'
            # This is necessary to be. It indicates were our body ends
            data += '\r\n'
            data += '<html><body>Hello World</body></html>\r\n'
            # This is necessary to be. It indicates were our body ends
            data += '\r\n'
            client_socket.sendall(data.encode())
            client_socket.shutdown(SHUT_WR)

    except KeyboardInterrupt:
        print('\nShutting down ...\n')
    except Exception as exc:
        print('Error:\n')
        print(exc)

    server_socket.close()


print('localhost:9000')
create_server()

