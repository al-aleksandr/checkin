# checkin

# How to setup "checkin" (acr122u) on Ubuntu

sudo apt-get install libusb-1.0-0-dev python-pyscard pcscd pcsc-tools libnfc-bin

# If pcsc_scan does not see ACR122U then permanently remove the pn533 kernel module use something like:
sudo rm -r /lib/modules/*/kernel/drivers/nfc/pn533

# to check: reader is working
pcsc_scan
