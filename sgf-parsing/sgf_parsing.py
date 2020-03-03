import re

class SgfTree:
    def __init__(self, properties=None, children=None):
        self.properties = properties or {}
        self.children = children or []

    def __eq__(self, other):
        if not isinstance(other, SgfTree):
            return False
        for k, v in self.properties.items():
            if k not in other.properties:
                return False
            if other.properties[k] != v:
                return False
        for k in other.properties.keys():
            if k not in self.properties:
                return False
        if len(self.children) != len(other.children):
            return False
        for a, b in zip(self.children, other.children):
            if a != b:
                return False
        return True

    def __ne__(self, other):
        return not self == other

def get_nodes(sgf_str):
    '''Separate SGF string by nodes. Yield each node.

    '''
    # All space characters except '\n' become spaces
    sgf_str = sgf_str.replace('\t', ' ').replace('\\', '')

    # Node with values or empty node '(;)'
    node_pattern = r'((?!;)[A-Z]{1,2}(\[(.+?)\])+(?=\(|\)|;))|(^\(;\)$)'

    node_found = False
    for node in re.finditer(node_pattern, sgf_str, re.DOTALL):
        if not node_found:
            node_found = True
        yield node
    if not node_found:
        raise ValueError('invalid node')


def parse_nodes(nodes):
    '''Parse key and values into a dict for each node.

    '''
    kv_pattern = r'([A-Z]{1,2})(\[.+?\](?=[A-Z]|$))+'

    for node in nodes:
        prop = {}
        for kv_str in re.finditer(kv_pattern, node.group(), re.DOTALL):
            key, value = kv_str.groups()

            # Syntax parsing
            if value.startswith('[') and value.endswith(']'):
                value = value[1:-1]
            value = value.split('][')
            prop[key] = value
        yield prop

def parse(input_string):
    nodes = get_nodes(input_string)
    node_properties = parse_nodes(nodes)
    children = []
    properties = None

    for count, prop in enumerate(node_properties):
        if count == 0:
            properties = prop
        else:
            children.append(SgfTree(prop))

    return SgfTree(properties=properties, children=children)
