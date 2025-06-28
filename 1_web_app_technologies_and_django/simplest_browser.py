import socket


# Make a phone
my_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)
# Make a phone call
# If the domain name or port will blow you up
my_socket.connect(
    # ('data.pr4e.org', 80)
    ('localhost', 9000)
)
# No so much error checking
# You have to encode the request into utf8
# More dense more compressed
# cmd = 'GET http://data.pr4e.org/page1.htm HTTP/1.0\r\n\r\n'.encode()
cmd = 'GET http://localhost/romeo.txt HTTP/1.0\r\n\r\n'.encode()
# Send the request out
my_socket.send(cmd)

# We suppose to receive data until the socket close.
while True:
    # recv is a blocking process and wait until 512 character
    data = my_socket.recv(512)
    # If data were less than 1 character we know that socket is 
    # closed by the server, because we do not received any character
    if len(data) < 1:
        break
    # Python needs to convert response, because it is utf8 but Python works with Unicode.
    print(data.decode(), end='')

my_socket.close()
