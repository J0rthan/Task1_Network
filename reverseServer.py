import threading
from Common import *
from socket import *


# 处理所有的server请求
def handle_client(connectionSocket):
    thread_name = threading.current_thread().name
    print(f"[{thread_name}] 客户端已连接")

    while True:  # 不断循环检测是否有新的消息过来
        try:
            header = recv_exact(connectionSocket, 6)  # 先接受header
            print(f"[{thread_name}] 收到 header: {header}")
            if not header:
                print("连接失败。")
                break

            # 判断是否为握手请求
            type, length = struct.unpack("!HI", header)
            if type == TYPE_INIT:
                print("收到握手请求。")
                ack = pack_agree()  # 包装ACK
                connectionSocket.sendall(ack)
                continue  # 等待下一个消息

            # 不是握手请求，接收data
            content_bytes = recv_exact(connectionSocket, length)
            content = content_bytes.decode('ascii')
            print(content)

            # 反转内容并发回
            reversed_content = content[::-1]
            response = pack_reverse_answer(reversed_content)
            connectionSocket.sendall(response)


        except Exception as e:
            print("处理客户端出错", e)
            break


def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', 8000))  # serverSocket will be the welcoming socket
    serverSocket.listen(
        10)  # Let the server listen for TCP connection requests(handshake). Parameter specifies the maximum number of queued connections(at least 1).

    while True:
        connectionSocket, addr = serverSocket.accept()  # Creates a new socket in the server, called connectionSocket and complete the handshaking then creating a TCP connection between the client's clientSocket and the server's connectionSocket.

        thread = threading.Thread(target=handle_client, args=(connectionSocket, ), name=f"Thread-{addr}")  # 进入处理函数
        thread.start()


if __name__ == '__main__':
    main()