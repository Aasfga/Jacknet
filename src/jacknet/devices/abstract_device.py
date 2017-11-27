
class AbstractDevice:
    def conv4b5b(self, data):
        converted = ""
        for i in range(len(data) // 4):
            converted += encode_set[data[4*i: 4*i+4]]
        return converted

    def conv5b4b(self, data):
        converted = ""
        for i in range(len(data) // 5):
            converted += decode_set[data[5*i: 5*i + 5]]
        return converted

    def send_msg(self, data):
        raise NotImplementedError

    def get_msg(self):
        raise NotImplementedError




encode_set = {
    "0000": "11110",
    "0001": "01001",
    "0010": "10100",
    "0011": "10101",
    "0100": "01010",
    "0101": "01011",
    "0110": "01110",
    "0111": "01111",
    "1000": "10010",
    "1001": "10011",
    "1010": "10110",
    "1011": "10111",
    "1100": "11010",
    "1101": "11011",
    "1110": "11100",
    "1111": "11101"
}

decode_set = {encode_set[k]: k for k in encode_set}