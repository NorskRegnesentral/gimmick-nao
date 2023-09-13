# gimmick-nao
Various bits to make the gimmick work with NAO

This uses the [robot
jumpstarter](https://github.com/aldebaran/robot-jumpstarter) from
Aldebaran, which lets you do most of the heavy lifting inside of
Python, instead of requiring Choregraphe.

You must use Python 2 to run these items on your local machine. Make
sure you have Python 2 installed and then follow [the
instructions](http://doc.aldebaran.com/2-8/dev/python/install_guide.html)
to make sure your things are set up correctly on your operating
system.

# Client

You need to have numpy and zeromq for Python 2 installed on the NAO
for this to work. Numpy is there by default, but zeromq must be built. We have that from ROSA. Then you simply run main.

You press the back of the right hand or the front of the head to take
a picture. You can also press the back of the head to stop. This is
here mostly for testing purposes now.

# Server

There is a simple server that takes a numpy array through a local
socket and then will process it. It uses the recognition model from
[gimmick_model](https://github.com/NorskRegnesentral/gimmick_model),
which in turn uses MediaPipe.


# Installing on NAO

Running `scripts/sync-nao.sh` should synchronize the files from the repo
to the NAO. This assumes that you already have Python 3.10 and all the
other libraries installed.

# Running on NAO

We assume that you have a proper Python 3.10 build with the
accompanying libraries. For the Python 2 that is installed on NAO, you
also have a version of PyZMQ installed. Documentation for this is
beyond the scope of this document, but documented in other Notes.

Currently this is done via scripts, we can choose to have these items
start automatically afterwards when we have things working.

## Starting the server

Run the `start_gimmick_server.sh` script.

## Starting the client

Run the `start_gimmick_client.sh` script.


# Misc

There is code here for NAO6, we'll see about getting it to work with a
NAO5 later.
