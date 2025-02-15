
def cidr(address, addressRange):
    from netaddr import IPNetwork, IPAddress
    if type(addressRange) is list:
        for networkAddressRange in addressRange:
            if IPAddress(address) in IPNetwork(networkAddressRange):
                return True
    else:
        if IPAddress(address) in IPNetwork(addressRange):
            return True
    return False

def cidrAddresses(cidr):
    from netaddr import IPNetwork
    ips = [ str(x) for x in IPNetwork(cidr) ]
    return ips
