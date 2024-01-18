#!/bin/bash

# Change return code of a function, Ghidra is your friend here if you want to figure out details
binary_patch=$(cat <<EOF
001f4a10: 01  .
001f4a13: e3  .
001f4a60: 01  .
001f4a63: e3  .
EOF
)

fake_licence=$(cat <<EOF
{"sn":"00000000","auth_code":"0000000000000000000000.00000000","digest":"0000000000000000000000000000000000000000000=","sign":"0"}
EOF
)

md5=($(md5sum /home/pi/ASIAIR/bin/zwoair_imager))
tempfile=$(mktemp -t tmp.XXXXXXXXXX)
timestamp=$(date +%s)

echo $binary_patch > $tempfile

if [[ $md5 != "ba4e082adb279175f33fe61ed46e4cd3" ]]; then
        echo "File verification failed, just works with 2.1 (dpkg asiair version 1.0.0-1074)"
        echo "current version is:"
        dpkg -l asiair
        exit -1
fi

#Creating Fake CPUID file
sed -e "s/.*Serial.*/Serial          : 0000000000000000/" /proc/cpuinfo > /boot/fake_cpuinfo

#TODO this step needs to be persistet in rc.local
sudo mount --bind /boot/fake_cpuinfo /proc/cpuinfo


echo "Creating backup of tiles to modify"
cp -v $1 $1.bak.$timestamp
cp -v /boot/zwoair_license /boot/zwoair_license.bak.$timestamp
cp -v /home/pi/.ZWO/zwoair_license /home/pi/.ZWO/zwoair_license.bak.$timestamp

#echo "Creating fake license file"
echo $fake_license > /boot/zwoair_license
echo $fake_license > /home/pi/.ZWO/zwoair_license

#echo "Patching binary"
xxd -c1 -r $tempfile /home/pi/ASIAIR/bin/zwoair_imager

#Creating Fake CPUID file
sed -e "s/.*Serial.*/Serial          : 0000000000000000/" /proc/cpuinfo > /boot/fake_cpuinfo

#TODO make this automatic
echo "Patching should have been successeded, howeer persist this line in rc.local before asiair gets started"
sudo mount --bind /boot/fake_cpuinfo /proc/cpuinfo
echo "sudo mount --bind /boot/fake_cpuinfo /proc/cpuinfo"

#Cleanup
rm $tempfile
