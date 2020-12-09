import socket


def CreateServer(host, port):
    Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Server.bind((host, port))
    Server.listen(5);
    print('Listening at {}'.format(Server.getsockname()))
    return Server


def ReadRequest(Client):
    re = ""
    Client.settimeout(2)
    try:
        re = Client.recv(4096).decode()
        while (re):
            re = re + Client.recv(4096).decode()
    except socket.timeout:
        if not re:
            print("Didn't receive data[Time out]!")
    finally:
        return re


def ReadHTTPRequest(Server):
    re = ""
    while (re == ""):
        Client, address = Server.accept()
        print("Client: ", address, "da ket noi toi server")
        re = ReadRequest(Client)
    return Client, re


def SendFileIndex(Client):
    f = open("index.html", "rb")
    L = f.read()
    header = """HTTP/1.1.200 OK
Content-Length: %d

""" % len(L)
    print("-----------------HTTP Request index.html:")
    print(header)
    header += L.decode()
    Client.send(bytes(header, "utf-8"))


def MovePageIndex(Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http:127.0.0.1:8081/index.html

"""
    print("---------------HTTP respone move index.html: ")
    print(header)
    Client.send(bytes(header, "utf-8"))


def MoveHomePage(Server, Client, Request):
    if "GET /index.html HTTP/1.1" in Request:
        SendFileIndex(Client)
        Server.close()
        return True

    if "GET / HTTP/1.1" in Request:
        MovePageIndex(Client)
        Server.close()
        Server = CreateServer("localhost", 8081)
        Client, Request = ReadHTTPRequest(Server)
        print("---------------HTTP Request:")
        print("Request", Request)
        Server.close()
        MoveHomePage(Server, Client, Request)
        return True


# http://127.0.0.1:8080/index.html

def CheckPass(Request):
    if "Username=admin&Password=admin" in Request:
        return True
    else:
        return False


def Move404(Server, Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8082/404.html

"""
    print("HTTP respone: ")
    print(header)
    Client.send(bytes(header, "utf-8"))
    Server.close()


def SendFile404(Client):
    f = open("404.html", "rb")
    L = f.read()
    header = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
    print("HTTP respone file 404.html: ")
    print("header")
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))


def Send404(Server, Client):
    Server = CreateServer("localhost", 8082)
    Client, Request = ReadHTTPRequest(Server)
    print("HTTP Request:")
    print(Request)
    if "GET /404.html HTTP/1.1" in Request:
        SendFile404(Client)
    Server.close()


def MoveInfo(Server, Client):
    header = """HTTP/1.1 301 Moved Permanently
Location: http://127.0.0.1:8082/info.html

"""
    print("HTTP respone: ")
    print(header)
    Client.send(bytes(header, "utf-8"))
    Server.close()


def SendFileInfo(Client):
    f = open("info.html", "rb")
    L = f.read()
    header = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Encoding: UTF-8
Content-Length: %d

""" % len(L)
    print("--------------------HTTP respone Info.html: ")
    print(header)
    header += L.decode()
    Client.send(bytes(header, 'utf-8'))


def SendInfo(Server, Client):
    Server = CreateServer("localhost", 8082)
    Client, Request = ReadHTTPRequest(Server)
    print("HTTP Request:")
    print(Request)
    if "GET /info.html HTTP/1.1" in Request:
        SendFileInfo(Client)
    Server.close()


if __name__ == "__main__":
    Server = CreateServer("localhost", 8080)
    Client, Request = ReadHTTPRequest(Server)
    print("--------------HTTP request:")
    print(Request)

    MoveHomePage(Server, Client, Request)
    Server = CreateServer("localhost", 10000)
    Client, Request = ReadHTTPRequest(Server)
    print("--------------HTTP request:")
    print(Request)
    if CheckPass(Request) == True:
        MoveInfo(Server, Client))
    else:
        SendInfo(Server, Client
        Move404(Server, Client)
        Send404(Server, Client)