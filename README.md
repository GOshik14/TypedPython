# TypedPython
The idea and the base of implementation are from the youtube channel Digitilize, video https://www.youtube.com/watch?v=dKxiHlZvULQ&t=1590s.

Simple cli app weather for getting weather by outer ip-address and web-API of the most popular weather site openweather.org.
The project goal is to train to write typed Pythonical code.

To run the project in any directory you need to have Python3, the path to Python should be added in PATH var.
You need to add the weather app's path in PATH var too, for example, you can create a soft link to weather like this:
sudo ln -s $(pwd)/weather /usr/local/bin/