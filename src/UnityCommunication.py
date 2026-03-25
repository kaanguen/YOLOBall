import UdpComms as U
import json

def get_udp_socket():
    
    sock = U.UdpComms(udpIP="0.0.0.0", portTX=8000, portRX=8001, enableRX=False, suppressWarnings=True)
    sock.udpIP = "host.docker.internal"
    return sock

def send_tracking_data(sock, obj_id, cls, x, z):
    data = {
        "id": int(obj_id),
        "class": int(cls),
        "x": round(float(x), 2),
        "z": round(float(z), 2)
    }
    json_string = json.dumps(data)
    sock.SendData(json_string)
