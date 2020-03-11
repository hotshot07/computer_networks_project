# I couldn't integrate the Diffie Hellman Key Exchange
# into the chat app right now but I wanted to see
# how it works so I made this simulation for it

# ---------- Explanation of DHKE from Stack Overflow ---------------------

# Diffie-Hellman is a way of generating a shared secret between two people in such a way 
#that the secret can't be seen by observing the communication. That's an important distinction: 
#You're not sharing information during the key exchange, you're creating a key together.

# This is particularly useful because you can use this technique to create an encryption key with someone,
# and then start encrypting your traffic with that key. And even if the 
# traffic is recorded and later analyzed, there's absolutely no way to figure out
# what the key was, even though the exchanges that created it may have been visible. 
# This is where perfect forward secrecy comes from. Nobody analyzing the traffic at a later 
# date can break in because the key was never saved, never transmitted, and never made visible anywhere.

# The way it works is reasonably simple. A lot of the math is the same as you see in public key crypto 
#in that a trapdoor function is used. And while the discrete logarithm problem is traditionally used 
#(the xy mod p business), the general process can be modified to use elliptic curve cryptography as well.

# But even though it uses the same underlying principles as public key cryptography, this is 
# not asymmetric cryptography because nothing is ever encrypted or decrypted during the exchange. 
# It is, however, an essential building-block, and was in fact the base upon which asymmetric 
# crypto was later built.

# The basic idea works like this:

# I come up with a prime number p and a number g which is coprime to p-1 and tell you what they are.
# You then pick a secret number (a), but you don't tell anyone. Instead you compute ga mod p and send 
# that result back to me. (We'll call that A since it came from a).
# I do the same thing, but we'll call my secret number b and the computed number B. So I compute gb mod p and send you the result (called "B")
# Now, you take the number I sent you and do the exact same operation with it. So that's Ba mod p.
# I do the same operation with the result you sent me, so: Ab mod p.
# The "magic" here is that the answer I get at step 5 is the same number you got at step 4.
# Now it's not really magic, it's just math, and it comes down to a fancy property of modulo exponents. Specifically:

# (ga mod p)b mod p = gab mod p
# (gb mod p)a mod p = gba mod p

# Which, if you examine closer, means that you'll get the same answer no matter which order you do the exponentiation in.
# So I do it in one order, and you do it in the other. I never know what secret number you used to get to the result and you never know what number I used, but we still arrive at the same result.

# That result, that number we both stumbled upon in step 4 and 5, is our shared secret key. 
# We can use that as our password for AES.

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



