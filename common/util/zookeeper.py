import json
import os.path
import kazoo
from kazoo.client import KazooClient
from kazoo.exceptions import NoNodeError

val = {}


class ZK:
    def connect(self, hosts, parent_path):
        # establishes a connection with the host
        zk = KazooClient(hosts=hosts, connection_retry=3)
        try:
            zk.start()
            zk.ensure_path(parent_path)
            return zk
        except Exception as e:
            raise ('ZK Connection error: {}'.format(e))

    def get_value(self, zk, full_path, node_name):
        # get node value for a node wrt to full path
        try:
            res = zk.get(full_path)[0]
            if res != b'':
                return json.loads(res.decode('utf-8'))
        except NoNodeError:
            raise ('Node {} could not be found'.format(node_name))
        return 'ZKNode({0}, {1})'.format(full_path, ZK.get_value(self, zk, full_path, node_name))

    def get_node_value(self, zk, parent_path, node_name):
        # get node value for a node wrt to parent path
        try:
            res = zk.get(os.path.join(parent_path, node_name))
            if res != b'':
                ZnodeData, ZnodeStat = res
                return json.loads(ZnodeData.decode('utf-8'))
        except NoNodeError:
            print('Node {} could not be found'.format(node_name))

    def is_node_exist(self, zk, parent_path, node_name):
        # checks if a node exists wrt to parent path
        print(zk.exists(os.path.join(parent_path, node_name)))
        return zk.exists(os.path.join(parent_path, node_name)) is not None

    def get_node(self, zk, parent_path, node_name):
        # get node wrt parent path
        full_path = os.path.join(parent_path, node_name)
        print(f"Full Path: {full_path}")
        if ZK.is_node_exist(self, zk, parent_path, node_name):
            return ZK.get_value(self, zk, full_path, node_name)

    def get_children1(self, zk, parent_path, node_name):
        # get all child nodes for a node wrt parent path
        children = zk.get_children(parent_path)
        for child in children:
            try:
                full_path = os.path.join(parent_path, child)
                res = zk.get(full_path)[0]
                if res != b'':
                    val[child] = json.loads(res.decode('utf-8'))
            except NoNodeError as err:
                print('Node {} could not be found'.format(child))
                print(err)
        print("Node type: ", type(val))
        return val

    def stop(self, zk):
        # stops the zookeeper session
        zk.stop()
