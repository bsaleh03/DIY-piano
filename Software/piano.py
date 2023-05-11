import pcf8574_io
import time
import telnetlib

tn = telnetlib.Telnet('localhost', 9800)
#for fluidsynth midi communication
tn.write(b"load /usr/share/sounds/sf2/FluidR3_GM.sf2\n")


p1 = pcf8574_io.PCF(0x20)
#enable i2c GPIO expander. This block will be replicated after first octave is completed
pins = {"7": 60, "6": 62, "5": 64} 
btns = {pin:False for pin in pins}
# mapping for midi notes and pins, will need to be adjusted.
for k in pins:
    p1.pin_mode("p{}".format(k), "INPUT")


print("ready")
#TODO: map this ready signal to an LED so we know when its on
while True:
    time.sleep(0.1)
    for k in pins:
        if not p1.read("p{}".format(k)):
            if not btns[k]:
                tn.write('noteon 0 {} 30 \n'.format(pins[k]).encode('utf-8'))
                btns[k] = True
        else:
            if btns[k]:
                tn.write('noteoff 0 {}\n'.format(pins[k]).encode('utf-8'))
                btns[k] = False
