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

Assuming all this is set up correctly, you can run the program from your computer with:

```
python2 main.py --qi-url 156.116.9.156
```

This assumes that you have numpy installed for Python 2 though (which is not likely).

There is code here for NAO6, we'll see about getting it to work with a
NAO5 later.
