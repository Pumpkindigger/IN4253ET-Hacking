# Create bridge
brctl addbr br0

# Make sure everything is up
ip link set dev br0 up

# Start X86 QEMU instance
qemu-system-x86_64 -drive format=raw,file=/qemu_images/openwrt-19.07.7-x86-64-combined-ext4.img -net nic -net bridge,br=br0 -daemonize -serial telnet:localhost:4321,server,nowait;

# Start mips QEMU instance
qemu-system-mips -kernel /qemu_images/openwrt-19.07.7-malta-be-vmlinux-initramfs.elf -net nic -net bridge,br=br0 -daemonize -serial telnet:localhost:4323,server,nowait;

#Start arm qemu, does not yet work
#qemu-system-arm -drive format=raw,file=/qemu_images/debian-10.8.0-armhf-netinst.img -net nic -net bridge,br=br0 -machine virt-3.1 -daemonize -serial telnet:localhost:4322,server,nowait;
qemu-system-aarch64 -m 2G -M virt -cpu max \
  -bios /usr/share/qemu-efi-aarch64/QEMU_EFI.fd \
  -drive if=none,file=/qemu_images/debian-10-openstack-arm64.qcow2,id=hd0 -device virtio-blk-device,drive=hd0 \
  -device e1000,netdev=net0 -netdev user,id=net0,hostfwd=tcp:127.0.0.1:5555-:22 \
  -nographic

# Start PPC (does not work)
# qemu-system-ppc -L pc-bios -drive format=raw,file=/qemu_images/debian-bullseye-DI-alpha3-ppc64el-netinst.iso -net nic -net bridge,br=br0 -nographic -M g3beige -g 1024x768x8

#Assign an IP address to the bridge, can probably be removed later as we no longer use br0
#dhclient -v br0