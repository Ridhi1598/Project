import yaml


from netmiko import ConnectHandler
from netmiko import BaseConnection

class DeviceInfo(yaml.YAMLObject):
    yaml_tag = u'!DeviceInfo'

    def __init__(self,
            name,
            executor_name,
            executor_group_name,
            executor_customer_name,
            executor_customer_region,
            executor_customer_group_name,
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
    def parse_file(cls, filename) -> InventoryEntries:
        with open(filename) as f:
            inventory: InventoryEntries = yaml.load(f, Loader=yaml.FullLoader)
        return DeviceInventory(inventory)

    @classmethod
    def parse_str(cls, content) -> InventoryEntries:
        inventory: InventoryEntries = yaml.load(content, Loader=yaml.FullLoader)
        return DeviceInventory(inventory)

    def get_device_for_model(self, device_model: str) -> DeviceInfo:
        devices = [device for device in self.inventory.devices
                    if device.model_family == device_model]

        if len(devices) == 0:
            raise NotImplementedError("No device found with model family " + device_model)

        # return the first found device with matching model family
        return devices[0]
class DeviceConfigurator:
    """ Device Configurator Base Class
    It contains the implementation for netmiko cisco ios devices.
    Subclasses are created by target type
    """

    SHOW_COMMAND = 'show running-config'

    def __init__(self, device_info: DeviceInfo):
        self.device_info = device_info
        self.net_connect = None

    def connect(self):
        connection_info = {
            'device_type': self.device_info.device_type,
            'host':   self.device_info.ip,
            'username': self.device_info.user,
            'password': self.device_info.password,
            'port' : self.device_info.port,
            'secret': self.device_info.secret,
        }
        self.net_connect: BaseConnection = ConnectHandler(**connection_info)

    def disconnect(self):
        self.net_connect.disconnect()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.disconnect()

    def write(self, section : str, config_list: [str]):
        self.net_connect.enable()
        self.net_connect.config_mode()

        self._write_section(section, config_list)

        self.net_connect.exit_config_mode()

    def write_sections(self, section_config_list: [(str, [str])]):
        self.net_connect.enable()
        self.net_connect.config_mode()

        for section, config_list in section_config_list:
            self._write_section(section, config_list)

        self.net_connect.exit_config_mode()


    def _write_section(self, section: str, config_list: [str]):
        if section:
            augmented_config_list = []
            augmented_config_list.append(section)
            augmented_config_list.extend(config_list)
            augmented_config_list.append('exit')

            self.net_connect.send_config_set(augmented_config_list)
        else:
            self.net_connect.send_config_set(config_list)

    def commit(self):
        try:
            self.net_connect.commit()
        except AttributeError:
            # ignore if commit isn't supported
            pass

    def read(self, section: str = None, regex_filter: str = None) -> str:
        command: str = self.SHOW_COMMAND
        command += ' ' + (section if section else "all")
        if regex_filter:
            command += ' | include ' + regex_filter
        return self.net_connect.send_command(command).strip()

    def compare(self, expected : str, section: str = None, regex_filter: str = None) -> (bool, str, str, str):
        found = self.read(section, regex_filter).strip()
        expected = expected.strip()
        section_regex = "%s|include %s" % (section, regex_filter)
        return (found == expected, found, expected, section_regex)

    def compare_list(
        self,
        expected_list: [str],
        section: str = None,
        regex_filter: str = None
        ) -> (bool, str, str, str):

        expected = "\n".join(expected_list)
        return self.compare(expected, section, regex_filter)


class E2EDeviceConfigurator():

    info = DeviceInfo(
        "name",
        "exname", 
        "gname", 
        "cname", 
        "eastern",
        "cgname", 
        "mfamily",
        "cisco_ios",
        "cisco-ios",
        "172.18.232.121",
        22,
        "cisco",
        "cisco",
        "cisco"
    )

    def setup_device_e2e_test(self):
        configurator: DeviceConfigurator = DeviceConfigurator(self.info)
        with configurator:
            ip_base_configuration_success = [
                (None, [
                    'no ip domain list',
                    'ip domain list .', 
                    'ip domain list core.tac.net',
                    'ip domain list osc.net.tac.net',
                    'ip domain name cust.on.tac.net',
                    'no ip domain lookup',
                    'no ip http secure-server',
                    'ip scp server enable',
                    'ip routing',
                    'ip forward-protocol nd',
                    'ip classless',
                    'ip subnet-zero',
                    'ip bgp-community new-format',
                    'no ip icmp redirect',
                    'no ip source-route',
                    'no ip finger',
                    'no ip http server',
                    'no cdp run',
                ])
            ]

            service_configuration_fail_to_remediate = [
                (None, [ 
                    'clock timezone MST -7',
                    'clock summer-time MDT recurring',
                    'no service nagle',
                    'no service tcp-keepalives-in',
                    'no service tcp-keepalives-in'
                ])

            ]
            
            logging_server_update_stnd = [
                (None, [
                    'no logging host',
                    'logging host 11.202.66.4'
                    'logging host 11.202.66.7',
                    'logging host 2.2.6.1',
                    'logging host 2.2.6.6',
                    'logging host 209.202.66.15',
                    'logging host 209.202.66.16',
                    'logging host 100.70.80.226',
                    'logging host 209.202.66.43',
                    'logging host 209.202.66.44'
                    ]
                )
            ]

            configurator.write_sections(ip_base_configuration_success)
            configurator.write_sections(service_configuration_fail_to_remediate)
            configurator.write_sections(logging_server_update_stnd)



if __name__ == "__main__":
    E2EDeviceConfigurator().setup_device_e2e_test()

