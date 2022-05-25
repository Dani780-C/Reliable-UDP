import socket
import struct

from helper import *
from time import sleep

server = ('127.0.0.1', 20001)
server_seq_number = get_random_seq()
server_ack_number = 0

def create_packet(payload, flags):
   
    flag_number = calculeaza_flag_number(flags)
    packet = struct.pack('!HHB', server_seq_number, server_ack_number, flag_number)
    packet += bytes(payload, 'utf-8')

    return packet


def main():

    server_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server_sock.bind(server) 

    print("RUDP server is listening 127.0.0.1:20001 ...")



    ok = True
    while ok:
        try:
            global server_ack_number, server_seq_number
            payload = None
            payload, client_address = server_sock.recvfrom(1400)

            (client_seq_number, client_ack_number, flag_number, _) = unpackage(payload)

            server_ack_number = increment(client_seq_number)

            if flag_number == dict["SYN"]:
                print("Cerere conexiune primita: [SYN] de la clientul {0}".format(client_address))
                packet = create_packet("", ["ACK", "SYN"])

                print("Trimitere raspuns: [SYN-ACK]")
                server_sock.sendto(packet, client_address)

                server_seq_number = increment(server_seq_number)
            
            elif flag_number == dict["ACK"] and server_seq_number == client_ack_number:
                print("Raspuns de la client: [ACK]")
                print("Conexiune reusita....\n")
                ok = False

        except Exception as e:
            print(e)

    chunks = []
    fin = False
    while fin == False:

        payload, address = server_sock.recvfrom(1400)

        (client_seq_number,client_ack_number,flag_number,data) = unpackage(payload)
        if flag_number == dict["PSH"]:
            # server_ack_number = (client_seq_number + len(data)) % (1 << 16)
            packet = create_packet("",["ACK"])
            print("Am primit chunk-ul de la {0}".format(address))
            chunks.append(data)
            server_sock.sendto(packet,address)
        elif flag_number == dict["FIN"]:
            fin = True
            print("FIN")

    fisier_bytes = b''.join(chunks)

    g = open("cirlan.txt", "wb")
    g.write(fisier_bytes)
        

main()