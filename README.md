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
for this to work. Numpy is there by default, but zeromq must be built.
We have that from ROSA. Then you simply run main.

Once it is running, pressing the right foot bumper will start a game.
Pressing the left foot bumper will stop the gimmick. Pressing the top
of NAO's head will change language between Norwegian and English
(default language is whatever the robot is configured to).

You can also toggle between sitting and standing by pressing the back
of NAO's head, this is more to give motors a rest.

# Server

There is a simple server that takes a numpy array through a local
socket and then will process it. It uses the recognition model from
[gimmick_model](https://github.com/NorskRegnesentral/gimmick_model),
which in turn uses MediaPipe.


# Installing on NAO

Running `scripts/sync-nao.sh` should synchronize the files from the repo
to the NAO. This assumes that you already have Python 3.10 and all the
other libraries installed.

## Stubs

Since we are using a cross-built Python 3.10 on NAO, not all the
packages have been installed via Pip, this results in stops when
installing our gimmick_model package. We have all these installed,
just not through pip. So, we created minimum stubs so that pip
doesn't complain when installing gimmick_model.

One *should not* use these outside of our environment. Especially if
one can easily get the real modules. This only places an entry in
pip's database. We are dependent on the actual modules being there.

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

Alternatively, you can add these to `$HOME/naoqi/Preferences/autoload.ini`

This has been done for the NAO 6 robots that NR has (at least as of
this writing). This means if something isn't working, it may be better
to just turn it off and try again.

# How the thing works

Right now, the classifier runs on the NAO and there are no game
elements. With the scripts running, you can touch parts of NAO's body
to activate the classifier.

* Left Bumper: Start game
* Back head: Change position between stand and sit (Ideally, sit is
  better for longer periods).
* Top head: Change language between English and Norwegian  
  
The classifier uses the camera between and a little above NAO's eyes.
When you activate the classifier, hold you hand around 50 cm from
NAO's head. This should make sure that the entire hand is visible.

Normally, NAO can run for about an hour or so before the battery needs
to be changed. It may make sense to keep the battery charger
connected, but it is nice to run the battery down a little.

# Misc

There is code here for NAO6, we'll see about getting it to work with a
NAO5 later.
