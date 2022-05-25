import socket
from time import sleep
from helper import *
import struct
import os

# global data
client_seq_number = get_random_seq()
client_ack_number = 0
server = ('127.0.0.1', 20001)

def create_packet(payload, flags):
    # contine headerul de udp si payload-ul
    # print(type(source_port))
    flag_number = calculeaza_flag_number(flags)
    packet = struct.pack('!HHB', client_seq_number, client_ack_number, flag_number)
    if payload == "":
        packet += bytes(payload,'utf-8')
    else:
        packet += payload

    return packet

def main():

    client_sock = socket.socket(family = socket.AF_INET, type = socket.SOCK_DGRAM)
    ok = True
    while ok:
        
        global client_ack_number, client_seq_number
        packet_initial_SYN = create_packet("", ['SYN'])

        try:
            print("Cererea de conectare la server a fost trimisa: [SYN]")

            client_sock.sendto(packet_initial_SYN, server)
            
            try:
                payload, _ = client_sock.recvfrom(1400)
            except Exception as e:
                print("Reincercare de trimitere pachet: [SYN]")
                continue
            else:
                (server_seq_number, server_ack_number, flag_number, _) = unpackage(payload)
                client_ack_number = increment(server_seq_number)

                if (flag_number ^ dict["SYN"] ^ dict["ACK"]) == 0 and client_seq_number + 1 == server_ack_number:
                    print("Raspuns de la server primit: [SYN-ACK]")
                    client_seq_number = increment(client_seq_number)
                    packet = create_packet("", ["ACK"])
                    print("Trimitere raspuns: [ACK]")
                    
                    client_sock.sendto(packet,server)
                        
                    ok = False

        except Exception as e:
            print(e)
        
    print("Conexiune reusita...\n")

    f = open('input.txt',"rb")
    chunks = []
    file = f.read()


    for i in range(0,len(file),80):
        chunks.append(file[i:i+80])
    
    client_sock.settimeout(3)
    i = 0
    while i < len(chunks):
        packet = create_packet(chunks[i], ["PSH"])            

        client_sock.sendto(packet, server)
        try:
            payload, address = client_sock.recvfrom(1400)
            (_,_,flag_number, _) = unpackage(payload)
            if flag_number == dict["ACK"]:
                print("Raspuns primit de la server...OK")
            i += 1
        except:
            print("Retrimitere pachet...")
            continue
                
        
    packet = create_packet("",["FIN"])
    client_sock.sendto(packet,server)
    print("FIN")
        # size = os.path.getsize('f:/file.txt') 
        # print('Size of file is', size, 'bytes')
        # break
        
        # print("Mesaj de trimis: ")
        # data = input()
        # packet = create_packet(data, ["PSH"])

        # client_seq_number = creste_seq_number(client_seq_number, len(data))
        # client_sock.sendto(packet, server)

        # payload, address = client_sock.recvfrom(1400)
        # (server_seq_number, server_ack_number, flag_number, data) = unpackage(payload)

        # if flag_number == dict["PSH"]:
        #     print("Raspuns primit de la server...")
        #     server_ack_number = (client_seq_number + len(data)) % (1 << 16)



if __name__ == "__main__":
    main()