# Jacknet - Unleash the power of sound!!

**Jacknet** - use it if you want to send data. Forget about gigabit ethernet, **Jacknet** is better!!

# How To
To install **Jacknet** put source code in your project folder. To send data by speakers **Jacknet** needs pulseaudio. I will describe some classes from **Jacknet** for you now:
* *Sender* - class used to send data. To construct object you have to specify device
* *Receiver* - class used to receive data. To construct object you have to specify device
* *Device* - abstract class which represents device used to send data
* *BufferedJack* - device that saves data in the buffer. No real device needed
* *RealJack* - device that sends data through the speakers (audio jack). Real device is needed here
* *FileReader* - device that reads data from wav file (in the future)

# Specification
**Jacknet** is based on ethernet frame. It can send data with amazing speed 32b/s!

# Tests
**Jacknet** wave creator was tested on satori. Conversion functions were tested by using unittests. Whole app was tested by our most valuable employee.

# Examples

Buffered connection: 
```
bj = BufferedJack(0.03) 
jc = JackConnection(bj)
jc.send_msg("ABCDEDF", get_mac())
print(jc.receive_msg())
```
Jack connection:
```
#Sender
from uuid import getnode as get_mac

jack = RealJack(0.025)
jc = JackConnection(jack)
jc.send_msg("ABCDEFGHIJKALSDFAF", get_mac())

#Receiver
jack = RealJack(0.025)
jc = JackConnection(jack)
print(jc.receive_msg())
```