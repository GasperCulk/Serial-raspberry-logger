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


class USBRemoved(Exception):
    pass

def open_usb_files():
    usbDrives = []

    subprocess.run(['sudo', 'rm', '-rf', base_dir+'*'])
    for usb_dir in os.listdir(base_dir):
        usb_path = os.path.join(base_dir, usb_dir)
        if os.path.isdir(usb_path):
            usb_path = os.path.join(usb_path, 'logs')
            #os.makedirs(usb_path, exist_ok=True)
            date = datetime.now().strftime('%d_%B_%H-%M')
            filePath = os.path.join(usb_path, f'usb_data_log_{date}.txt')
            print("File made:", filePath)
            usbDrives.append(open(filePath, "a"))
    return usbDrives

def open_ser():
    while True:
        print("Searching for box connection.")
        sleep(1)
        try:
            serDev = serial.Serial(serial_port, boud_rate, timeout=1)

            if serDev.is_open:
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
                          
                                    
print("Starting connection")    
serial_port = connect_usb()
print("serial port:", serial_port)
ser = open_ser()
while True:
    try: 
        # open files
        usbDrives=open_usb_files()
        if usbDrives == []: continue
        
        # write data
        try:
            while True:
                ser.write(data_to_send)
                sleep(1)
                data = ser.read(ser.in_waiting).hex() + '\n'
                for logFile in usbDrives:
                    if not Path(logFile.name).exists():
                        raise USBRemoved("USB has been removed from device.")
                    logFile.write(data)
                    logFile.flush()
                    #log_file = open(file_name, "a")
                    #log_file.write(data + '\n')
                    #log_file.flush()
                    #log_file.close()
        except serial.SerialException:
            print("Lost connection to box")
            ser.close()
            ser = open_ser()
        except Exception as e:
            print(e)
        finally:
            for logFile in usbDrives:
                try: logFile.close() 
                except:pass
    except KeyboardInterrupt:
            print(" user interupt")
            break
    except PermissionError:
        pass
    except Exception as e:
            print(e)
ser.close()
print(f"Logging stoped: {datetime.now().strftime('%d_%B_%H-%M')}")

