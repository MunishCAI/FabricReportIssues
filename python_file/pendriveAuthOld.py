import os
import pyudev
import time
import socket
from python_file.encryption_file import caesar_cipher as ef
# from encryption_file import caesar_cipher as ef



# Define the name of the authorized key file
AUTHORIZED_KEY_FILE = "my_key_file.txt"




def get_device_name():
    try:
        device_name = socket.gethostname()
        return device_name.lower()
    except socket.error as e:
        print(f"Error: {e}")
        return None

# def get_usb_drive_name():
#     machineName =socket.gethostname().lower()
#     directory = f'/media/{machineName}/'
#     directory = os.listdir(directory)
#     return directory[0]

# def is_authorized(usb_drive_path):
#     device_name = get_device_name().lower()
#     usb_drive_name = get_usb_drive_name()
#     newpath = os.path.join('/media/',device_name,usb_drive_name, AUTHORIZED_KEY_FILE)
#     text = "Charlemagne@1"
#     shift = 3
#     encrypted_text = ef(text, shift)
#     with open(newpath, 'r') as file:
#             content = file.read()
#     return os.path.exists(newpath) and content[:-1].__eq__(encrypted_text)
import subprocess
def is_authorized():
    usb_drives = []
    device_name = get_device_name()
    # print(os.listdir("/media/santhosh/"))
    for i in os.listdir("/media/"+device_name+"/"):
        files = os.listdir("/media/"+device_name+"/"+i)
        print("/media/"+device_name+"/"+i,"files:",files)
        for k in files:
            if k == "my_key_file.txt":
                print("found the file")
                # key = os.system("cat "+"/media/"+device_name+"/"+i+"/"+k)
                cmd = "cat /media/{}/{}/{}".format(device_name, i, k)    
                result = subprocess.check_output(cmd, shell=True, text=True)
                # print('result:',result) 
                text = "Charlemagne@1"
                shift = 3
                encrypted_text = ef(text, shift)
                if (result[:-1].__eq__(encrypted_text)):
                    print('path :',"/media/"+device_name+"/"+i)
                    
                    return('path :',"/media/"+device_name+"/"+i)
    return False


def authendicatePendrive():
    print("Insert your USB drive for authentication...")

    while True:
        usb_drives = is_authorized()
        if usb_drives:
            print('usb_drive_path :',usb_drives)
            print(f"Authentication successful for {usb_drives}. Access granted!")                    
            return usb_drives
        else:
            print("Authentication failed. Access denied.")
        time.sleep(2)


# authendicatePendrive()