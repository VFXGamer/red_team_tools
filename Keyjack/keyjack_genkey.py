from cryptography.fernet import Fernet


key = Fernet.generate_key()
file = open("encryption_key.txt", 'wb')
file.write(key)
file.close()
print("Copy the text in encryption_key.txt and paste it in keyjack.py, keyjack_decrypt.py under 'key' variable")
