import sys
import random
from Common import *
from socket import *

# 分割报文，至达到合规的范围[Lmin, Lmax]
def split_Message(file_path, Lmin, Lmax):
    # 先读文件
    with open(file_path, 'r', encoding='ASCII') as file:
        data = file.read()  # type(data) == str

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
    file_path = './test'  # 要发送txt文件的位置

    # 返回分块结果列表
    chunks = split_Message(file_path, Lmin, Lmax)
    length = len(chunks)

    # 创建socket
    clientSocket = socket(AF_INET, SOCK_STREAM)  # SOCK_STREAM means it's a TCP socket
    clientSocket.connect((serverIp, serverPort))  # Initiates the TCP connection between the client and server.

    N = len(chunks)  # 要发送的次数
    Initial_Message = pack_initialization(N)
    clientSocket.sendall(Initial_Message)  # 发送握手报文
    Agree_Message = unpack_agree(recv_exact(clientSocket, 2))  # 接受Agree报文，2bytes
    if Agree_Message[0] == TYPE_AGREE:  # 接收到正确报文，开始发送各分块
        result = []
        for i in range(N):
            msg = pack_reverse_request(chunks[i])
            clientSocket.sendall(msg)

            # 发完之后准备接收首部
            header = recv_exact(clientSocket, 6)
            type, length = struct.unpack('!HI', header)

            # 接受data部分
            data = recv_exact(clientSocket, length)
            content = data.decode('ascii')
            result.append((i, content))  # 把二元组放到容器中

            # 打印
            print("%d: %s" % (i, content))

        # 整合收到的所有数据
        # 按编号排序
        result.sort(key=lambda x: x[0])
        res = result[::-1]

        # 提取所有内容并拼接
        full_text = ''.join(item[1] for item in res)

        # 写文件
        with open('./output.txt', 'w') as file:
            file.write(full_text)


if __name__ == "__main__":
    main()
