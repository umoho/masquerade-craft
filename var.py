
class VarInt:
    SEGMENT_BITS = 0x7f
    CONTINUE_BIT = 0x80

    def __init__(self, value: int):
        self.value = value

    def get_bytes(self):
        b = []
        while True:
            if (self.value & ~self.SEGMENT_BITS) == 0:
                b.append(self.value)
                return bytes(b)
            b.append((self.value & self.SEGMENT_BITS) | self.CONTINUE_BIT)
            self.value = r_shift(self.value, 7)


def string(s: str):
    str_len = VarInt(len(s)).get_bytes()
    return str_len + bytes(s, encoding='utf-8')


def r_shift(val: int, n: int):
    return val >> n if val >= 0 else (val + 0x1_0000_0000) >> n
