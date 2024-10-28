#from __future__ import annotations
import yaml



class DeviceInfo(yaml.YAMLObject):
    yaml_tag = u'!DeviceInfo'

    def __init__(self,
            name,
            executor_name,
            executor_group_name,
            executor_customer_name,
            executor_customer_region,
            executor_customer_group_name,
            executor_auth_group,
            model_family,
            device_type,
            ned_id,
            ip,
            port : int,
            user,
            password,
            secret):

        self.name = name

        # info for config management & param tree traversal
        self.executor_name = executor_name
        self.executor_group_name = executor_group_name
        self.executor_customer_name = executor_customer_name
        self.executor_customer_group_name = executor_customer_group_name
        self.executor_customer_region = executor_customer_region
        self.executor_auth_group = executor_auth_group
        self.model_family = model_family # type TODO rename

        # info for device access
        self.device_type = device_type # TODO rename
        self.ned_id = ned_id
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.secret = secret

class InventoryEntries(yaml.YAMLObject):
    yaml_tag = u'!Inventory'

    def __init__(self, devices: [DeviceInfo]):
        self.devices = devices


class DeviceInventory:
    def __init__(self, inventory: InventoryEntries):
        self.inventory = inventory

    @classmethod
    def parse_file(cls, filename):
        with open(filename) as f:
            inventory: InventoryEntries = yaml.load(f, Loader=yaml.FullLoader)
        return DeviceInventory(inventory)

    @classmethod
    def parse_str(cls, content):
        inventory: InventoryEntries = yaml.load(content, Loader=yaml.FullLoader)
        if not isinstance(inventory, InventoryEntries):
            raise TypeError("%r is not an InventoryEntries" % inventory)
        return DeviceInventory(inventory)

    def get_device_for_model(self, device_model: str):
        devices = [device for device in self.inventory.devices
                    if device.model_family == device_model]

        if len(devices) == 0:
            raise NotImplementedError("No device found with model family " + device_model)

        # return the first found device with matching model family
        return devices[0]

