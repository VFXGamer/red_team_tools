# KeyJack is a python keylogger.
## _This tool is just for educational purposes I am not responsible for any loses_
### Prerequisites:
1. Python installed
2. An IDE to run the files.


### Setup Steps:
1. Run `python3 -m pip install -r requirements.txt` to install all the required modules.
2. Add your email id and password from which you will like to reecieve the logged file.
```python
email_address = "Enter Email ID"
password = "Enter Your Email account's Password"
```
3. Add a email id in which you would like to recieve the logged file.
```python
toaddr = "Enter the email id in which you want to receive email"
```
4. (_This is optional_) Generate a key by running `python3 keyjack_genkey.py` and pasting the key generated to key variable in keyjack.py file.
```python
# by default I have added a key
key = "sbC9IsydZX1wJB0E2ZIXQhZIEIggXV3mkgqdxyaTfe4=" 
# generate encryption key and enter into here
```
5. As all the things are set its time to run it. Run `python3 keyjack.py`.
6. You will recieve the file on your email that you entered in step 3. (All the logged files files will be deleted from your pc once the program ends.)
7. Now ypu will have to decrypt all the text inside the *e_keyjack_final_.txt* by running `python3 keyjack_decrypt.py`
(Note:- Both *keyjack_decrypt.py* and *e_keyjack_final_.txt* should be in the same folder.) </br>

<b>Don't miss use your knowledge.</b> </br>

> With great power comes great responsiblities

<b>Thank You</b>
