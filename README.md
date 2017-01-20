
# Docker Machinator

Docker machinator is a python tool that allows you to access your [docker
machine](https://docs.docker.com/machine/) from any workstation.

This tool solves the problem of transferring your docker-machine credentials
(certificates and configuration) from one computer to another in a reasonably
secure manner. (Encrypted using your password, with python
[sstash](https://github.com/realcr/sstash))


# Example of usage


```
dmachinator load machine hamshoosh
```


