# Emotive
#### by @KubaMaciazek, @tomjan0 & @malinowska423

## Introduction

Small Android app converting photos into emoji.

## Developer dependencies

- Python 3.7
- Kivy 1.11.1 (and everything that comes with it)
- Buildozer 1.2


## Kivy instalation
### For Windows:

If you have Anaconda: 
```
$ conda install kivy -c conda-forge
```

If you don't, this should work: 
```
$ python -m pip install kivy==2.0.0rc1
```

You might need to install other packages as well. All information can be found [here](https://kivy.org/doc/stable/installation/installation-windows.html).

<b>Note</b>: You will be able to run Kivy app on Windows, but you will not build it for Android. You will need <u>Linux</u> or <u>macOS</u>.

<b>Note 2</b>: You can do that from <b>Windows Subsystem for Linux</b>. Check this [link](https://github.com/kivy/kivy/issues/5854).

### For Linux:

Just run this in your command line.

```
$ apt install python3-pip
$ apt install cython3 python3-dev
$ apt install libsdl2-dev libsdl2-ttf-dev libsdl2-image-dev libsdl2-mixer-dev
$ python3 -m pip install git+https://github.com/kivy/kivy.git@master
```

## Build and deployment

First you need to <b>install and configure</b> Buildozer. 
```
$ pip install buildozer
```
Now the dependencies for Buildozer. For <b>Ubuntu</b>:
```
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install --user --upgrade Cython==0.29.19 virtualenv  # the --user should be removed if you do this in a venv

# add the following line at the end of your ~/.bashrc file
export PATH=$PATH:~/.local/bin/
```
For [macOS](https://buildozer.readthedocs.io/en/latest/installation.html#targeting-android).

To run the app on connected phone execute this line:
```
$ buildozer -v android debug deploy run logcat
```

t.b.c.