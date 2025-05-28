import struct

# Type定义
TYPE_INIT = 1
TYPE_AGREE = 2
TYPE_REQUEST = 3
TYPE_ANSWER = 4
Error = -1  # 错误报文

# client握手请求报文
def pack_initialization(n):
    return struct.pack('!HI', TYPE_INIT, n)  # Type (2 Bytes) + N (4 Bytes)

# server解包握手报文
def unpack_initialization(data):
    t, n = struct.unpack('!HI', data)
    return t, n

# server发送回复握手报文
def pack_agree():
    return struct.pack('!H', TYPE_AGREE)

# client解包Agree报文
def unpack_agree(data):
    return struct.unpack('!H', data)


# client发送reverse请求报文
def pack_reverse_request(chunk):
    if isinstance(chunk, str):
        data = chunk.encode('ascii')  # 确保是 bytes
    elif isinstance(chunk, bytes):
        data = chunk
    else:
        raise TypeError("Expected str or bytes for chunk")
    return struct.pack('!HI', TYPE_REQUEST, len(data)) + data

# server解包reverse请求报文
def unpack_reverse_request(data):
    header, length, number = struct.unpack('!HI', data[:6])
    content = data[6:6+length].decode('ascii')
    return header, content

# server发送reverse结果报文
def pack_reverse_answer(chunk):
    if isinstance(chunk, str):
        data = chunk.encode('ascii')  # 确保是 bytes
    elif isinstance(chunk, bytes):
        data = chunk
    else:
        raise TypeError("Expected str or bytes for chunk")
    return struct.pack('!HI', TYPE_ANSWER, len(data)) + data

# client解包server发来的answer报文
def unpack_reverse_answer(data):
    type, length = struct.unpack('!HI', data[:6])
    content = data[6:6+length].decode('ascii')
    return type, content

# 精确读数据
def recv_exact(sock, size):
    data = b''
    while len(data) < size:
        more = sock.recv(size - len(data))
        if not more:
            raise ConnectionError("Socket closed before receiving enough data.")
        data += more
    return data