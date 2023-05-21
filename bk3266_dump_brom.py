#!/usr/bin/env python3
import sys,serial,time

MAGIC=b"\x01\xe0\xfc"
MAGIC2=b"\x01\xe0\xfc\x05\xfe\x95\x27\x95\x27"
MAGIC3=b"\x01\xe0\xfc\x01\x00"


if len(sys.argv) < 3:
    print("usage: bk3266_dump_brom.py <serial port> <file>")
    exit()

#open serial port
serialPort = serial.Serial(port = sys.argv[1], baudrate=115200,\
    bytesize=8, timeout=0.1, stopbits=serial.STOPBITS_ONE)

#send echo handshake
length=1
cmd=0
while True:
    serialPort.write(MAGIC2)
    time.sleep(0.1)
    serialPort.write(MAGIC3)
    print("no answer")
    if (serialPort.read(8) == b"\x04\x0e\x05\x01\xe0\xfc\x01\x00"):
        print("answer good, start dump")
        break

f = open(sys.argv[2],"wb")

#read memory
length=5
cmd=3

i = 0
#here is max offset. 0x4000 = 16 kb flash)
while (i < 0x4000):
    serialPort.write(MAGIC+length.to_bytes(1,byteorder='little')+\
        cmd.to_bytes(1,byteorder='little')+i.to_bytes(4,byteorder='little'))
    offset = list(i.to_bytes(4,byteorder='little'))
    data = list(serialPort.read(15))
    if (len(data) != 15 or data[0] != 0x04 or data[1] != 0x0e or data[2] != 0x0c or data[3] != 0x01 or data[4] != 0xe0 or data[5] != 0xfc or data[6] != 0x03 or data[7] != offset[0] or data[8] != offset[1] or data[9] != offset[2] or data[10] != offset[3]):
        continue
    print(data[7:15])
    f.write(bytes(data[11:15]))
    i = i + 4

#that's all folks
f.close()
serialPort.close()
