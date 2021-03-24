# Create bridge
brctl addbr br0

# Make sure everything is up
ip link set dev br0 up

# Start QEMU instance
qemu-system-x86_64 -drive format=raw,file=/qemu_images/openwrt-19.07.7-x86-64-combined-ext4.img -net nic -net bridge,br=br0 -daemonize -serial telnet:localhost:4321,server,nowait;
#Start arm qemu, does not yet work
#qemu-system-arm -drive format=raw,file=/qemu_images/debian-10.8.0-armhf-netinst.iso -net nic -net bridge,br=br0 -machine virt-3.1 -daemonize -serial telnet:localhost:4321,server,nowait;

#start mips
qemu-system-mips -kernel /qemu_images/openwrt-19.07.7-malta-be-vmlinux-initramfs.elf -net nic -net bridge,br=br0 -daemonize -serial telnet:localhost:4321,server,nowait;

#Assign an IP address to the bridge, can probably be removed later as we no longer use br0
#dhclient -v br0