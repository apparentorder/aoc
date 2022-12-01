import errno
import socket
import threading
import time
from typing import Callable, Union


class Socket:
    def __init__(self, address_family: socket.AddressFamily, socket_kind: socket.SocketKind):
        self.socket = socket.socket(family=address_family, type=socket_kind)
        self.__recv_buffer = b""

    def send(self, buffer: Union[str, bytes]) -> int:
        if isinstance(buffer, str):
            buffer = buffer.encode("UTF-8")

        send_bytes = 0
        while send_bytes < len(buffer):
            send_bytes += self.socket.send(buffer[send_bytes:])

        return send_bytes

    def recv(self, maxlen: int = 4096, blocking: bool = True) -> bytes:
        maxlen -= len(self.__recv_buffer)
        try:
            self.socket.setblocking(blocking)
            ret = self.__recv_buffer + self.socket.recv(maxlen)
            self.__recv_buffer = b""
            return ret
        except socket.error as e:
            err = e.args[0]
            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                return self.__recv_buffer
            else:
                raise

    def sendline(self, line: str):
        if not line.endswith("\n"):
            line += "\n"

        self.send(line)

    def recvline(self, timeout: int = 0) -> Union[str, None]:
        """
        Receive exactly one text line (delimiter: newline "\n" or "\r\n") from the socket.

        :param timeout: wait at most TIMEOUT seconds for a newline to appear in the buffer
        :return: Either a str containing a line received or None if no newline was found
        """
        start = time.time()
        while b"\n" not in self.__recv_buffer:
            self.__recv_buffer += self.recv(1024, blocking=False)
            if time.time() - start <= timeout:
                time.sleep(0.01)  # release *some* resources
            else:
                break

        if b"\n" not in self.__recv_buffer:
            return None
        else:
            line = self.__recv_buffer[:self.__recv_buffer.index(b"\n")]
            self.__recv_buffer = self.__recv_buffer[self.__recv_buffer.index(b"\n") + 1:]
            return line.decode("UTF-8")

    def close(self):
        self.socket.close()


class ClientSocket(Socket):
    def __init__(self, addr: str, port: int, address_family: socket.AddressFamily = socket.AF_INET,
                 socket_kind: socket.SocketKind = socket.SOCK_STREAM):
        super().__init__(address_family, socket_kind)
        self.socket.connect((addr, port))
        self.laddr, self.lport = self.socket.getsockname()
        self.raddr, self.rport = self.socket.getpeername()


class RemoteSocket(Socket):
    def __init__(self, client_sock: socket.socket):
        super().__init__(client_sock.family, client_sock.type)
        self.socket = client_sock
        self.laddr, self.lport = self.socket.getsockname()
        self.raddr, self.rport = self.socket.getpeername()


class ServerSocket(Socket):
    def __init__(self, addr: str, port: int, address_family: socket.AddressFamily = socket.AF_INET,
                 socket_kind: socket.SocketKind = socket.SOCK_STREAM):
        super().__init__(address_family, socket_kind)
        self.socket.bind((addr, port))
        self.socket.listen(5)
        self.laddr, self.lport = self.socket.getsockname()
        self.raddr, self.rport = None, None  # Transport endpoint is not connected. Surprisingly.

    def _connection_acceptor(self, target: Callable[..., None]):
        while 1:
            (client_socket, client_address) = self.socket.accept()
            connection_handler_thread = threading.Thread(target=target, args=(RemoteSocket(client_socket), ))
            connection_handler_thread.start()

    def accept(self, target: Callable[..., None], blocking: bool = True):
        if blocking:
            self._connection_acceptor(target)
            return None
        else:
            connection_accept_thread = threading.Thread(target=self._connection_acceptor, kwargs={'target': target})
            connection_accept_thread.start()
            return connection_accept_thread
