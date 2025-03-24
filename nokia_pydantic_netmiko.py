import json
from pydantic import BaseModel, IPvAnyAddress, conint
from netmiko import ConnectHandler

# device pydantic model 

class byod(BaseModel):
    device_type: str
    vendor: str
    nos: str
    hostname: str
    ip_address: IPvAnyAddress
    port: conint(gt=0, lt=65536)
    username: str
    password: str


with open("devices.json", "r") as file:
    device_list = json.load(file)

with open("logs.txt", "w") as log_file:
    for device_data in device_list:
        try:
            device = byod(**device_data)
            print(f"Device data is validated for {device.hostname}")
        
            device_connection = {
                "device_type": device.device_type,
                "host": str(device.ip_address),
                "username": device.username,
                "password": device.password,
                "port": device.port,
            }
            if (device.vendor.lower() == "nokia") and (device.device_type.lower() == "nokia.sros"):
#            if device.device_type.lower() == "nokia.sros":
                print(f"Connecting to {device.hostname}...")
                connection = ConnectHandler (**device_connection)
                print(f"Connected to {device.hostname}")
                output = connection.send_command("show system information")
                print(f"{device.hostname} Output:\n", output)

                log_file.write(f"\n=== {device.hostname} ===\n")
                log_file.write(output + "\n")

                connection.disconnect()
                print(f"Connection closed for {device.hostname}")

            elif (device.vendor.lower() == "nokia") and (device.device_type.lower() == "nokia.srl"):
#            elif device.device_type.lower() == "nokia.srl":
                print(f"Connecting to {device.hostname}...")
                connection = ConnectHandler (**device_connection)
                print(f"Connected to {device.hostname}")
                output = connection.send_command("show system information")
                print(f"{device.hostname} Output:\n", output)

                log_file.write(f"\n=== {device.hostname} ===\n")
                log_file.write(output + "\n")

                connection.disconnect()
                print(f"Connection closed for {device.hostname}")

            else:
                print (f"No connection built for {device.vendor.upper()} {device.nos.upper()} devices...")
            
        except Exception as e:
            error_message = f"Error with {device_data['hostname']}: {e}\n"
            print(error_message)
            log_file.write(error_message)        
