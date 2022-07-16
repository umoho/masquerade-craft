import var


def packet(packet_id: int, data: list, compressed=False):
    if not compressed:
        body = []
        pid = var.VarInt(packet_id).get_bytes()
        for o in data:
            body += o
        length = var.VarInt(len(body) + 1).get_bytes()
        return bytes(length) + bytes(pid) + bytes(body)
