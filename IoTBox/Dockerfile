FROM debian:latest

# Do installs
RUN apt-get update
RUN apt-get install --no-install-recommends -y qemu-system libvirt-clients libvirt-daemon-system virtinst libguestfs-tools telnet qemu-efi-aarch64 # Install QEMU for virtualization, libvirt for configuration and management, virtinst for cli vm creation, libguestsfs for accessing images, telnet for establishing connection to the VMs, qemu-efi-aarch64 for bios of arm instance
RUN apt-get install -y bridge-utils libosinfo-bin wget net-tools

# Download image x86 openwrt for QEMU
RUN mkdir /qemu_images
RUN wget -P /qemu_images https://downloads.openwrt.org/releases/19.07.7/targets/x86/64/openwrt-19.07.7-x86-64-combined-ext4.img.gz
RUN gunzip /qemu_images/openwrt-19.07.7-x86-64-combined-ext4.img.gz

#Download mips openwrt
RUN wget -P /qemu_images https://downloads.openwrt.org/releases/19.07.7/targets/malta/be/openwrt-19.07.7-malta-be-vmlinux-initramfs.elf

#Download arm image
RUN wget -P /qemu_images https://cdimage.debian.org/cdimage/openstack/current/debian-10-openstack-arm64.qcow2

#Download ppc image
#RUN wget -P /qemu_images https://cdimage.debian.org/cdimage/bullseye_di_alpha3/ppc64el/iso-cd/debian-bullseye-DI-alpha3-ppc64el-netinst.iso
#RUN wget -P /qemu_images https://cdimage.debian.org/debian-cd/current/ppc64el/iso-cd/debian-10.8.0-ppc64el-netinst.iso

# Make bridge.conf file to allow bridge utilities for QEMU
RUN mkdir /etc/qemu
RUN echo "allow br0" >> /etc/qemu/bridge.conf

COPY setup.sh /setup.sh
RUN chmod +x /setup.sh

# https://wiki.debian.org/KVM
# https://jamielinux.com/docs/libvirt-networking-handbook/