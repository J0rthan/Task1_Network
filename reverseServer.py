import threading
from Common import *
from socket import *


# 处理所有的server请求
def handle_client(connectionSocket):
    while True: # 不断循环检测是否有新的消息过来
        msg = connectionSocket.recv(1024)  # 包含数字，不能用decode
        if len(msg) == 6:  # 握手请求
            t, n = unpack_initialization(msg)
            if t == TYPE_INIT:
                print("收到握手请求。")
                ack = pack_agree()
                connectionSocket.send(ack)
            else:
                print("没有收到握手请求，握手失败。")

        else:  # 处理其他请求
            header, content = unpack_reverse_request(msg)
            result = content[::-1]  # reverse
            pack_reverse_answer(result)


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))  # serverSocket will be the welcoming socket
    serverSocket.listen(
        10)  # Let the server listen for TCP connection requests(handshake). Parameter specifies the maximum number of queued connections(at least 1).

    while True:
        connectionSocket, addr = serverSocket.accept()  # Creates a new socket in the server, called connectionSocket and complete the handshaking then creating a TCP connection between the client's clientSocket and the server's connectionSocket.

        thread = threading.Thread(target=handle_client, args=(connectionSocket, ))  # 先处理握手
        thread.start()


if __name__ == '__main__':
    main()