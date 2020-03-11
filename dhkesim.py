# I couldn't integrate the Diffie Hellman Key Exchange
# into the chat app right now but I wanted to see
# how it works so I made this simulation for it

class DH_Endpoint(object):
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None

    def generate_partial_key(self):
        partial_key = self.public_key1**self.private_key
        partial_key = partial_key % self.public_key2
        return partial_key

    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r**self.private_key
        full_key = full_key % self.public_key2
        self.full_key = full_key
        return full_key

    def encrypt_message(self, message):
        encrypted_message = ""
        key = self.full_key
        for c in message:
            encrypted_message += chr(ord(c)+key)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c) - key)
        return decrypted_message


message = "Mia San Mia"
s_public = 197
s_private = 199
m_public = 151
m_private = 157

User1 = DH_Endpoint(s_public, m_public, s_private)
User2 = DH_Endpoint(s_public, m_public, m_private)

User1_partialKey=User1.generate_partial_key()
User2_partialKey=User2.generate_partial_key()

print(User1_partialKey)
print(User2_partialKey)

User1_fullKey=User1.generate_full_key(User2_partialKey)
User2_fullKey=User2.generate_full_key(User1_partialKey)

print(User1_fullKey)
print(User1_fullKey)

encryptedMessage = User1.encrypt_message(message)
print(encryptedMessage)

decryptedMessage = User2.decrypt_message(encryptedMessage)
print(decryptedMessage) 



