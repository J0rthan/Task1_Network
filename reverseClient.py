import sys
import random
from Common import *
from socket import *

# 分割报文，至达到合规的范围[Lmin, Lmax]
def split_Message(file_path, Lmin, Lmax):
    # 先读文件
    with open(file_path, 'r', encoding='ASCII') as file:
        data = file.read()

    chunks = list()
    idx = 0
    length = len(data)

    # 开始分块[Lmin, Lmax]
    while idx < length:
        size = random.randint(Lmin, Lmax)
        if idx + size >= length :  # 为最后一块
            chunk = data[idx:length]
            chunks.append(chunk)
        else:  # 不是最后一块
            chunk = data[idx:idx + size]
            chunks.append(chunk)

        idx += size  # 结束循环用

    return chunks

def main():
    serverIp = sys.argv[1]
    serverPort = int(sys.argv[2])
    Lmin = int(sys.argv[3])
    Lmax = int(sys.argv[4])
    file_path = './test' # 要发送txt文件的位置

    # 返回分块结果列表
    chunks = split_Message(file_path, Lmin, Lmax)
    length = len(chunks)

    # 创建socket
    clientSocket = socket(AF_INET, SOCK_STREAM)  # SOCK_STREAM means it's a TCP socket
    clientSocket.connect((serverIp, serverPort))  # Initiates the TCP connection between the client and server.

    N = len(chunks)  # 要发送的次数
    Initial_Message = pack_initialization(N)
    clientSocket.send(Initial_Message)  # 发送握手报文
    Agree_Message = unpack_agree(clientSocket.recv(2))  # 接受Agree报文，2bytes
    if(Agree_Message[0] == TYPE_AGREE): # 接收到正确报文，开始发送各分块
        for i in range(N):
            msg = pack_reverse_request(chunks[i])
            pack_reverse_request(msg)

            # 发完之后准备接收
            receive_msg = clientSocket.recv(1024)
            header, content = unpack_reverse_answer()
            print(content)  # 在终端打印显示
            with open('output.txt', 'a', encoding='ASCII') as f:
                f.write(content)




if __name__ == "__main__":
    main()
