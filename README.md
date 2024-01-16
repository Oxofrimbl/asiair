# asiair
Jailbreak for Seestar/ASIAIR and simliar devices via RPC call

usage
python3 jailbreak.py

options:
* --client-ip (override client ip for RPC calls to connect the reverse shell or upload the disk-dump)
* --shell (This mode established a reverse shell to the client this request is initiated OR the --client-ip given use nc -l 4242 on the clinet to get the shell
* --backup this mode performs a disk-dump of the complete mmc memory to the client (or --client-ip) example usage on the client to rcive the dump: nc -l 4444 | dd of=asiair.img
* --jailbreak setting username:password for ssh to pi:raspberry
