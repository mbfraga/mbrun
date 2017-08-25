# mbrun

Series of useful scripts revolving around rofi that I have made. They depend
on a library found in `helpers/mbrofi.py` meant to minimize maintenace of
each individual script. This can be used as a nice platform for anyone that
wants to make a quick rofi interface in python. However, it is not meant to be
a real project in any way, so consequential idiosyncracies abound--buyer
beware.

The idea is to make it very easy for me to go from an idea to a useful script,
to keep a uniform look to all the scripts, and to be able to generate a global
menu from where to launch them.

For many of these, they can be trivially made to be standalone by copying the
few functions from mbrofi that they rely on. Please feel free to use or get
inspiration from any of these scripts for your own personal needs.


## layout

* mbmain -- script manager which allows enabling and disabling of scripts from
            the global menu. It also generates the global menu and can be used
            as the launcher for every other script in here. It should be able
            to enable any symlinked launcher as well--allowing the user to add
            other rofi apps to it.

* helpers/mbrofi.py -- helper script that is used in virtually every other
                       script in here.


## dependencies

For mbmain and mbrofi, the dependencies are:

* rofi
* python3 (built on 3.5.4)
* xclip
* notify-send


Other scripts will have other dependencies. Some are common dependencies found
in most decent repos, others are more esoteric ones found chiefly on git.
Ideally I will make getting them as easy as possible. Below is a list of the
dependencies for each script.

* sshot.py

   - Depends on my homebaked script
       [sshot](https://github.com/mbfraga/scripts/blob/master/sshot)
       which requires the additional following dependencies:
       * xrandr
       * maim
       * curl
       * xclip

* screenshots.py
   - python-requests

* buku.py (I don't like the use of sqlite on this one, will personally try to
    move to plain text files for bookmark management)

    - [buku](https://github.com/jarun/Buku)
