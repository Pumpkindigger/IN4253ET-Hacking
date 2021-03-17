FROM debian

# Do installs
RUN apt-get update && apt-get install -y qemu qemu-kvm libvirt-clients libvirt-daemon-system bridge-utils libguestfs-tools  genisoimage  virtinst  libosinfo-bin  virt-manager  wget uml-utilities  net-tools sudo



# Download image openwrt for QEMU
RUN sudo wget https://downloads.openwrt.org/releases/19.07.7/targets/x86/64/openwrt-19.07.7-x86-64-combined-ext4.img.gz
RUN sudo gunzip openwrt-19.07.7-x86-64-combined-ext4.img.gz

# Make bridge.conf file to allow bridge utilities for QEMU
RUN sudo mkdir etc/qemu
RUN sudo echo "allow br0" >> /etc/qemu/bridge.conf
