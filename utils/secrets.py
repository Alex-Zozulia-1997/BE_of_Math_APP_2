from cryptography.fernet import Fernet

key = Fernet.generate_key()

# uncomment the line below to print your key (SK) into the console.
print(key.decode())
