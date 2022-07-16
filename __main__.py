import socket
import json
import time
import yaml

import proto
import var

default_conf = {
    'bind': {
        'ip': '0.0.0.0',
        'port': 25565
    },
    'motd': 'A Minecraft Server - Try login if you can!',
    'reason': 'Haha. It\'s a pseudo/fake server.',
    'player': {
        'online': 0,
        'max': 20
    }
}


def load_conf(file_name='./conf.yml'):
    try:
        with open(file_name, mode='r') as file_obj:
            file_text = file_obj.read()
            conf = yaml.load(file_text, yaml.FullLoader)
    except FileNotFoundError:
        with open(file_name, mode='w') as file_obj:
            y = yaml.dump(default_conf)
            file_obj.write(y)
            print(f'Put new config: {file_name}')
            conf = default_conf

    return conf


def main():

    print('Starting...')
    conf = load_conf()
    bind_address = (conf['bind']['ip'], conf['bind']['port'])
    motd = {
        'version': {
            'name': '1.18.2',
            'protocol': 758
        },
        'players': {
            'max': conf['player']['max'],
            'online': conf['player']['online'],
            'sample': []
        },
        'description': {
            'text': conf['motd']
        }
    }

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((conf['bind']['ip'], conf['bind']['port']))
    server_socket.listen()
    print(f'Listening on {bind_address}')

    while True:
        client, addr = server_socket.accept()
        print(f'Accepted client from {addr}')

        data = client.recv(1024)
        next_state = data[-1]
        if next_state == 0x01:
            time.sleep(0.5)
            _data = client.recv(1024)

            motd_json = json.dumps(motd)
            packet_id = 0
            motd_response = proto.packet(packet_id, [var.string(motd_json)])
            print('Send MOTD')
            client.sendall(motd_response)

        if next_state == 0x02:
            time.sleep(0.5)
            _data = client.recv(1024)
            reason = {
                'text': conf['reason']
            }
            reason_json = json.dumps(reason)
            packet_id = 0
            disconnect = proto.packet(packet_id, [var.string(reason_json)])
            print('Send Disconnect')
            client.sendall(disconnect)

        client.close()

    # server_socket.close()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exit')
        exit()
