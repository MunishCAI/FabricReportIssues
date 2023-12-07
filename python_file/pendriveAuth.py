import os
import pyudev
import time
import socket
import subprocess
# from encryption_file import caesar_cipher as ef
from python_file.encryption_file import caesar_cipher as ef




def get_device_name():
    try:
        device_name = socket.gethostname()
        return device_name.lower()
    except socket.error as e:
        print(f"Error: {e}")
        return None
    
    


def is_authorized():
    device_name = get_device_name()
    
    # unmount previous drive
    
    # cmd = "dir /media/{}/drive/".format(device_name)
    # result = subprocess.check_output(cmd, shell=True, text=True)
    # print('result: ',result)
    # if result:
    #     try:
    #         cmd = "umount /media/{}/".format(device_name)
    #         result = subprocess.check_output(cmd, shell=True, text=True)
    #         print("Sucess UN-mounting usb drive!",result)
    #     except:
    #         print("errror in unmounting")

    # create drive dir
    try:
        cmd = "mkdir /media/{}/drive/".format(device_name)
        result = subprocess.check_output(cmd, shell=True, text=True)
        print('drive folder sucessfully created!')
    except:
        print("Drive folder already present!")

    # list of USBDevices 
    cmd = "dir /dev/"
    result = subprocess.check_output(cmd, shell=True, text=True)
    my_list = result.split()

    matches = [word for word in my_list if word.startswith('s') and word.endswith('1')]
    if not matches:
        matches = [word for word in my_list if word.startswith('s') ]
    print(matches)
    for i in matches:
        try:
            
            try:
                cmd = "mount /dev/{} /media/{}/drive/".format(i,device_name)
                result = subprocess.check_output(cmd, shell=True, text=True)
                print("Sucess mounting usb drive!",result)
            except:
                print('error in  mounting')
            files = os.listdir("/media/"+device_name+"/drive")
            print("files:",files)
            for k in files:
                if k == "my_key_file.txt":
                    print("found the file")
                    cmd = "cat /media/{}/drive/{}".format(device_name, k)    
                    result = subprocess.check_output(cmd, shell=True, text=True)
                    print('result:',result) 
                    text = "Charlemagne@1"
                    shift = 3
                    encrypted_text = ef(text, shift)
                    if (result[:-1].__eq__(encrypted_text)):
                        print('path :',"/media/"+device_name+"/drive") 
                        return "/media/"+device_name+"/drive"         
        except:
            print("Error In finding File")
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