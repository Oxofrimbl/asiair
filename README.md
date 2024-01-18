# asiair jailbreak
Jailbreak for Seestar/ASIAIR and simliar devices via RPC call

usage
python3 jailbreak.py

options:
* --client-ip (override client ip for RPC calls to connect the reverse shell or upload the disk-dump)
* --shell (This mode established a reverse shell to the client this request is initiated OR the --client-ip given use nc -l 4242 on the clinet to get the shell
* --backup this mode performs a disk-dump of the complete mmc memory to the client (or --client-ip) example usage on the client to rcive the dump: nc -l 4444 | dd of=asiair.img
* --jailbreak setting username:password for ssh to pi:raspberry

# asiair - patch_for_rpi.sh

Disclaimer - under US LAW youre entitled to perform an repair of your device (Magnuson–Moss_Warranty_Act), meaning if your processor broke and you want to run your legally obtained ASIAIR/Seestar on a fixed/replaced board this is currently failing due to a version/cpuid check in the SW.

However the patch does inject a "fake" licence file (which actually inernally failed the SSL decryption), combined with a still matching and fake /proc/cpuinfo (overriden by a bind-mount from a file). Last step was patching the binary by returning internally in the execution flow "true" for the hardware verification step. By doing so the SW should be able to run on a replaced CPU. Run this application on the rw-mounted os. Backups of all files *should* be created. However all on your own risk and legal responsibility.
