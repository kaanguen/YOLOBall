#import json
import cv2
from ultralytics import YOLO
import UdpComms as U 
import UnityCommunication as network

def setup():
    
    model = YOLO('yolo11n.pt') 
    video_path = "input.mp4"
    cap = cv2.VideoCapture(video_path)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    output_path = "outputs/detected_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    sock = network.get_udp_socket()

    return model, cap, out, sock, output_path





def detectBoxes(model, cap, out, sock, output_path):
    frame_count = 0
    print("Starte Erkennung und Senden an Unity...")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        frame_count += 1
        
        # Tracking Logik
        results = model.track(frame, persist=True, classes=[0, 32], conf=0.3, device='cpu') 

        for result in results:
            if result.boxes is None or result.boxes.id is None:
                continue

            boxes = result.boxes.xyxy.cpu().numpy()
            ids = result.boxes.id.cpu().numpy().astype(int)
            clss = result.boxes.cls.cpu().numpy().astype(int)

            for box, obj_id, cls in zip(boxes, ids, clss):
                x1, y1, x2, y2 = box
                

                pos_x = (x1 + x2) / 2
                pos_z = y2
                # Datenpaket (Hier später Homographie statt Pixel!)
    
                # Senden
                network.send_tracking_data(sock, int(obj_id), int(cls), pos_x, pos_z)

                # Zeichnen für das Debug-Video
                color = (0, 255, 0) if cls == 0 else (0, 0, 255)
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

        out.write(frame)

    cap.release()
    out.release()
    print(f"\n Video gespeichert: {output_path}")



# --- DER STARTPUNKT ---
if __name__ == "__main__":
    
    m, c, o, s, path = setup()

    detectBoxes(m, c, o, s, path)