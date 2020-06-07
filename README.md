# Emotive
#### by [@KubaMaciazek](https://github.com/KubaMaciazek), [@tomjan0](https://github.com/tomjan0) & [@malinowska423](https://github.com/malinowska423)

## Introduction

Kivy application that recognizes emotions and turn them into emoticons. Once running you can see image from camera in your computer and current emotion that has been recognized. You can save the emoji anytime and then copy to any other application. Enjoy!

## Developer dependencies

- Python 3.7
- Kivy 1.11.1
- Pyperclip 1.7.0


## Kivy instalation
### For Windows:

If you have Anaconda: 
```
$ conda install kivy -c conda-forge
```

If you don't, this should work: 
```
$ python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
$ python -m pip install kivy_deps.gstreamer==0.1.*
$ python -m pip install kivy==2.0.0rc1
```

All information can be found [here](https://kivy.org/doc/stable/installation/installation-windows.html).

### For Linux:

Just run this in your command line.

```
$ apt install python3-pip
$ apt install cython3 python3-dev
$ apt install libsdl2-dev libsdl2-ttf-dev libsdl2-image-dev libsdl2-mixer-dev
$ python3 -m pip install git+https://github.com/kivy/kivy.git@master
```

## Run the app

<b>Note:</b> Before you run the app, remember to check if you have pyperclip installed. If not run ``pip install pyperclip``

To start using the app, go into `Emotive` folder and run `main.py` with python.

```
$ cd Emotive && python main.py
```
