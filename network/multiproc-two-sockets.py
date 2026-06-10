'''
Sample to run two processes each reading from socket and sending to another socket while sharing same queue.
In particular, this simulator reads from TCP and forwards to UDP.

queue.get() blocks the queue, thus we using except pass when queue is empty, and continue execution

'''

import socket
from multiprocessing import Process, Queue
import time, random

def get_tcp(queue, rs):
    rs.bind((RCV_HOST, RCV_PORT))
    rs.listen(1)
    conn, addr = rs.accept()

    while True:
        indata = conn.recv(1024)
        print('received', indata)
        queue.put([addr, indata])
        time.sleep(5)
        # b=[random.randint(0,10), random.randint(0,10), random.randint(0,10)]
        # print('received', b)
        # queue.put(b)
        # time.sleep(5)


def send_udp(queue, ds, DST_HOST, DST_PORT):
    ds.bind((DST_HOST, DST_PORT))
    buff = []
    while True:
        time.sleep(1)
        try:
            buff = queue.get(False)
            print('sent', buff)
        except:
            pass
        for i in buff:
            print(i)
            ds.sendto((DST_HOST, DST_PORT), i[0])


if __name__ == '__main__':
    # TCP receiver
    RCV_HOST = '127.0.0.1'
    RCV_PORT = 65435

    # UDP destination
    DST_HOST = '127.0.0.1'
    DST_PORT = 65433

    print('TCP receiver started at: %s:%s' % (RCV_HOST, RCV_PORT))
    rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    print('UDP destination set to: %s:%s' % (DST_HOST, DST_PORT))
    ds = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    

    q = Queue()
    p1 = Process(target=get_tcp, args=(q,rs))
    p2 = Process(target=send_udp, args=(q,ds,DST_HOST,DST_PORT))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

''''

'''