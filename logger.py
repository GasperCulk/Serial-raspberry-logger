import serial
import os
import subprocess
from time import time,sleep
from datetime import datetime
from pathlib import Path

# command sent
byte_seq = [
    0xF4, 0xF5, 0x00, 0x48, 0x0D, 0x00, 0x00, 0x27,
    0x01, 0xFE, 0x01, 0x00, 0x00, 0x69, 0x00, 0x00,
    0xAA, 0xFF, 0x03, 0x8E, 0xF4, 0XFB
]
data_to_send = bytes(byte_seq)
# box connection
boud_rate = 460800
# USBs base path
base_dir = '/media/student/'
log_dir = '/boot/firmware/logs/'


class USBRemoved(Exception):
    pass

def make_file():
    try:
        date = datetime.now().strftime('%d_%B_%H-%M')
        fileName = f'{log_dir}usb_data_log_{date}.txt'
        print("File made:", fileName)
        subprocess.run(['sudo', 'touch', fileName])
        return fileName
    except Exception as e:
        print(e)


def open_ser():
    while True:
        print("Searching for box connection.")
        sleep(1)
        try:
            serial_port = connect_usb()
            if serial_port == None:continue
            serDev = serial.Serial(serial_port, boud_rate, timeout=1)
            if serDev.is_open:
                print("serial port:", serial_port)
                print("Found connection to box")
                return serDev
            else:serDev.close()
        except serial.SerialException: pass

def connect_usb(baseDir='/dev', boudRate=boud_rate):
    ttyUSB_devices = [f"{baseDir}/ttyUSB{i}" for i in range(10)]
    for device in ttyUSB_devices:
        if os.path.exists(device):
            try:
                serDev = serial.Serial(device, boud_rate, timeout=1)
                if serDev.is_open:
                    serDev.close()
                    return device
                else:serDev.close()
            except serial.SerialException: pass
                          
                                    
print("Find connaction")
while True:
    try: 
        ser = open_ser()
        file_name = make_file()
        # write data
        try:
            while True:
                # uncoment for status log
                #ser.write(data_to_send)
                sleep(1)
                data = ser.read(ser.in_waiting).hex()
                if data == "": continue
                log_file = open(file_name, "a")
                log_file.write(data + '\n')
                log_file.flush()
                os.fsync(log_file.fileno())
                log_file.close()
        except Exception as e:
            print(e)
            ser.close()
            ser = open_ser()
        finally:
            pass
    except KeyboardInterrupt:
            print(" user interupt")
            break
    except PermissionError:
        pass
    except Exception as e:
            print(e)
ser.close()
print(f"Logging stoped: {datetime.now().strftime('%d_%B_%H-%M')}")


