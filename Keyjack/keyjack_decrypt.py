from cryptography.fernet import Fernet

key = "sbC9IsydZX1wJB0E2ZIXQhZIEIggXV3mkgqdxyaTfe4=" # change the key if you have changed in the keyjack.py file


keyjack_final_e = "e_keyjack_final_.txt" # file to decrypt

encrypted_files = [keyjack_final_e] 
count = 0


for decrypting_files in encrypted_files:

    with open(encrypted_files[count], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    with open("decryption.txt", 'ab') as f:
        f.write(decrypted)

    count += 1
