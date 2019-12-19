import socket


def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=3):
    """
    https://stackoverflow.com/questions/12248132/how-to-change-tcp-keepalive-timer-using-python-script

    Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)


def set_keepalive_win(sock, keep_alive_time=10000, keep_alive_interval=3000):
    """
    The keepalivetime member specifies the timeout, in milliseconds,
    with no activity until the first keep-alive packet is sent.
    The keepaliveinterval member specifies the interval,
     in milliseconds, between when successive keep-alive packets are sent if no acknowledgement is received.
    """
    sock.ioctl(socket.SIO_KEEPALIVE_VALS, (1, keep_alive_time, keep_alive_interval))
