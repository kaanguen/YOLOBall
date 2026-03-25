import UdpComms as U
import json

def get_udp_socket():
    # Dein Trick für Docker
    sock = U.UdpComms(udpIP="0.0.0.0", portTX=8000, portRX=8001, enableRX=False, suppressWarnings=True)
    sock.udpIP = "host.docker.internal"
    return sock

def send_frame_data(sock, frame_players):
  
    if not frame_players:
        return 

    packet = {
        "players": frame_players
    }
    
    json_string = json.dumps(packet)
    
    sock.SendData(json_string)


