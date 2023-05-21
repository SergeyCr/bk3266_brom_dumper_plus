# bk3266_brom_dumper
Beken BK3266 Boot ROM dumper

## Usage
`bk3266_dump_brom.py <serial port> <file>`  

Needs pySerial installed. Needs USB-TTL adapter with 3.3v support.

Connect UART to target device, run the python script and power the target on,
and in the easiest case it should start dumping right away. UART is usually 
wired to micro USB data lines. If it is not, there are possibly some test 
points on the board where you can solder the wiring.

This particular fork was created because original one didn't work for me on a
BK3266 based board. At first it did not dump anything, so i've fiddled with
the code a bit. A bit of luck pressing play/answer button and it dumped a few
bytes, then suddenly stopped. Many retries later, I've figured out that the
chip looks like protected from reading internal flash memory this way. 

So as a workaround I've built a simple arduino circuit based on a typical
blink example, but it does raise for 180 ms and turn off for 20, so that's
about 5 Hz clock with 90% duty cycle. After having dump started, I've 
attached arduino's output to battery input of this board. This restarts the 
MCU and luckily we're getting a few more bytes of code every time.

When I managed to finish dumping two times, I've ran into a case that they
were not identical about 10% in different places. So I've improved the data
reading procedure to be much more strict to the result it recieves from MCU.
Good thing is that MCU returns 4 bytes of data only in the case it reiceves
a valid reading command with exact memory address.

So with this one we can dump bootloader code (16 kb size) in about 5 min!
Always do a few dumps and compare them!
