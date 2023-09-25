import machine

mac_address = ":".join("{:02X}".format(b) for b in machine.unique_id()[-6:])
print("Pico W's MAC Address:", mac_address)
