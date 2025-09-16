import cv2
import socket
import pickle
import math
import time

# Server configuration
HOST = "127.0.0.1"
PORT = 9999

# Initialize UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Path to video file
video_file = r"C:\Users\Pravesh\Downloads\1MB.mp4"  # update with your own path
capture = cv2.VideoCapture(video_file)

if not capture.isOpened():
    raise FileNotFoundError(f"Unable to open video: {video_file}")

MAX_PACKET_SIZE = 60000  # safe UDP payload size
frame_index = 0

print("[SERVER] Starting video transmission...")

while capture.isOpened():
    success, frame = capture.read()
    if not success:
        print("[SERVER] Video playback finished.")
        break

    # Resize frame to control data size
    frame = cv2.resize(frame, (640, 360))

    # Compress frame into JPEG format
    _, encoded = cv2.imencode(".jpg", frame)
    serialized = pickle.dumps(encoded)

    # Determine how many packets needed
    num_segments = math.ceil(len(serialized) / MAX_PACKET_SIZE)

    for seg in range(num_segments):
        start = seg * MAX_PACKET_SIZE
        stop = start + MAX_PACKET_SIZE
        piece = serialized[start:stop]

        # Flag = 1 → last segment of frame
        flag = 1 if seg == num_segments - 1 else 0

        # Send tuple (flag, data_chunk)
        server_socket.sendto(pickle.dumps((flag, piece)), (HOST, PORT))

    frame_index += 1
    print(f"[SERVER] Sent frame {frame_index}")

    # Control playback rate (~30 fps)
    time.sleep(0.03)

capture.release()
server_socket.close()
print("[SERVER] Transmission ended")
