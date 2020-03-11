# Computer Networks Project

For my computer networks module in Trinity College Dublin, I have made a multithreaded chat application that sends messages to users instantly. I'm now working on adding security features like AES Encryption to the application.

I have added a file dhkesim.py to simulate how a Diffie Hellman key exchange works. I would integrate it into the chat app later.


Compilation instructions:

This program is made in Python version 3.7.3
You don’t need to download any separate libraries for it.

———————— For Chat Application —————————————————

If you’re on a mac, run term.py to open 3 new terminals for testing the app

Run $python3 server.py

Run $python3 client.py  (in two or more terminals as this is a chatting app)

Known issues: When a user disconnects, the server isn’t able to kill the specific thread

———————— For Simulating Diffie Hellman Key Exhange ———————

Run $python3 dhkesim.py


Current Progress
![Progress](progress.jpg)
