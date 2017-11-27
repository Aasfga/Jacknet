def data_to_bin(data):
    return "".join(bin(ord(x))[2:].zfill(8) for x in data)


def mac_to_bin(mac):
    return "{0:048b}".format(mac)


def int_to_bin(x):
    return "{0:032b}".format(x)


def bin_to_data(binary):
    return "".join(chr(int(binary[8*i:8*i + 8], 2)) for i in range(len(binary)//8))


def bin_to_mac(bin_mac):
    return int(bin_mac, 2)


def bin_to_int(x):
    return int(x, 2)


def list_to_string(l):
    return "".join([str(x) for x in l])


def string_to_list(s):
    return [int(x) for x in s]
