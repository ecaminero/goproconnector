# -*- coding: utf-8 -*-
from bluetooth.ble import DiscoveryService
import gatt
from goprocam import GoProCamera, constants
import time


#gopro = GoProCamera.GoPro()
def discover_camera():
    cameras=[]
    service = DiscoveryService()
    devices = service.discover(2)
    for address, name in devices.items():
        if name.startswith("GoPro"):
            cameras.append([name,address])
    if len(cameras) == 0:
        print("No cameras detected.")
        exit()
    if len(cameras) == 1:
        return cameras[0][1]
    for index, i in enumerate(cameras):
        print("[{}] {} - {}".format(index, i[0], i[1]))
    return cameras[int(input("ENTER BT GoPro ADDR: "))][1]

mac_address=discover_camera()

manager = gatt.DeviceManager(adapter_name='hci0')
class AnyDevice(gatt.Device):

    def connect_succeeded(self):
        super().connect_succeeded()
        print("[%s] Connected" % (self.mac_address))
        #gopro.pair(usepin=False)

    def services_resolved(self):
        super().services_resolved()
        control_service = next(
            s for s in self.services
            if s.uuid == '0000fea6-0000-1000-8000-00805f9b34fb')

        time.sleep(5)
        for i in control_service.characteristics:
            print(i.uuid)
            if i.uuid.startswith("b5f90072"):
                i.write_value(bytearray(b'\x02\x01\x01'))
        pass
    def characteristic_write_value_succeeded(self, characteristic):
        print("[recv] {}".format(characteristic.uuid))
        if characteristic.uuid.startswith("b5f90072"):
            cmd=input(">> ")
            if cmd == "exit":
                exit()
            if cmd == "record start":
                characteristic.write_value(bytearray(b'\x02\x01\x01'))
            if cmd == "record stop":
                characteristic.write_value(bytearray(b'\x02\x01\x00'))
            if cmd == "mode video":
                characteristic.write_value(bytearray(b'\x03\x02\x01\x00'))
            if cmd == "mode photo":
                characteristic.write_value(bytearray(b'\x03\x02\x01\x01'))
            if cmd == "mode multishot":
                characteristic.write_value(bytearray(b'\x03\x02\x01\x02'))
            if cmd == "poweroff":
                characteristic.write_value(bytearray(b'\x01\x05'))
            if cmd == "poweroff-force":
                characteristic.write_value(bytearray(b'\x01\x04'))
            if cmd == "tag":
                characteristic.write_value(bytearray(b'\x01\x18'))
            if cmd == "locate on":
              characteristic.write_value(bytearray(b'\x03\x16\x01\x01'))
            if cmd == "locate off":
              characteristic.write_value(bytearray(b'\x03\x16\x01\x00'))
            if cmd == "wifi off":
                characteristic.write_value(bytearray(b'\x03\x17\x01\x00'))
            if cmd == "wifi on":
                characteristic.write_value(bytearray(b'\x03\x17\x01\x01'))
        #exit()

device = AnyDevice(mac_address=mac_address, manager=manager)
device.connect()
manager.run()

