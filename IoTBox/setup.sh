# Create bridge
brctl addbr br0

dhclient -v br0

# Make sure everything is up
ip link set dev br0 up

# Start QEMU instance
qemu-system-x86_64 -drive format=raw,file=openwrt-19.07.7-x86-64-combined-ext4.img -nographic -net nic -net bridge,br=br0