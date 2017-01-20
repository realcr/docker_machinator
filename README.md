
# Docker Machinator

Docker machinator is a python tool that allows you to access your [docker
machine](https://docs.docker.com/machine/) from any workstation.

This tool solves the problem of storing or transferring your docker-machine
credentials (certificates and configuration) from one computer to another in a
reasonably secure manner. (Encrypted using your password, with python
[sstash](https://github.com/realcr/sstash)). See [sstash
cryptography](https://github.com/realcr/sstash#cryptography-used) for more
information about the cryptography used.

# Installation

Inside the directory where setup.py resides, type:

```
pip install -e .
```

I recommend to use [virtualenv](https://virtualenv.pypa.io/en/stable/) to avoid
polluting your main python installation.

After the installation is complete, you will have a new command line tool
called dmachinator. Typing `dmachinator` without any argument will give you
this help message:

```bash
$ dmachinator 
usage: dmachinator [-h] {load,store} ...

positional arguments:
  {load,store}  help for subcommand
    load        Load a machine
    store       Store a machine

optional arguments:
  -h, --help    show this help message and exit
```

# Example of usage

Assume that I have a docker-machine working somewhere that I used to manage
from my desktop. Now assume that I want to access it from my laptop.

Let's save the machine from the desktop. We first make sure that the machine is
present using the `docker-machine ls` command:

```
$ docker-machine ls
NAME        ACTIVE   DRIVER         STATE     URL                          SWARM   DOCKER    ERRORS
mymachine   -        digitalocean   Running   tcp://xxx.xxx.xxx.xxx:yyyy           v1.11.2   
```

Next, we save the machine using `dmachinator store` command:

```
$ dmachinator store mymachine stash
Stash password:
$ ls
stash
```

Note that above you will have to type a password for your machines stash. The
first time that you store a machine into your stash you will be able to choose
any password that you want. After that, you will have to use the same password.
(Future releases might add password changing functionality).


Next, I open my laptop and install docker machine.
I am expected to have no managed docker machines at this point on my laptop:

```
$ docker-machine ls
NAME   ACTIVE   DRIVER   STATE   URL   SWARM   DOCKER   ERRORS
```

I copy the stash file to my laptop (I can email it to myself for example, or
store it at some cloud provider).

```
$ ls
stash
```

To load the docker-machine from the stash, I use the following command:

```
$ dmachinator load mymachine stash 
Stash password:
```

Above you will have to type the same password the you used when you created the
stash.

Finally we can check that indeed the docker-machine credentials were loaded to
the laptop:

```
$ docker-machine ls
NAME        ACTIVE   DRIVER         STATE     URL                          SWARM   DOCKER    ERRORS
mymachine   -        digitalocean   Running   tcp://xxx.xxx.xxx.xxx:yyyy           v1.11.2   
```

Exactly as we head earlier on the desktop machine.
