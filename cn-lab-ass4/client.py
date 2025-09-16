import cv2
import socket
import pickle

# Client configuration
HOST = "127.0.0.1"
PORT = 9999

# Initialize UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.bind((HOST, PORT))

frame_parts = []  # temporary storage for chunks

print("[CLIENT] Ready to receive video stream...")

while True:
    try:
        # Receive incoming UDP packet
        packet_data, _ = client_socket.recvfrom(65536)
        end_flag, segment = pickle.loads(packet_data)  # unpack (end_flag, segment)

        # Add received segment to list
        frame_parts.append(segment)

        # Check if this was the last segment of the frame
        if end_flag == 1:
            # Combine all pieces into one frame
            full_bytes = b"".join(frame_parts)
            encoded_frame = pickle.loads(full_bytes)

            # Decode image back into OpenCV format
            image = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)

            # Show the video frame
            cv2.imshow("Live UDP Stream", image)

            # Reset storage for next frame
            frame_parts.clear()

            # Exit loop when user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        break

# Clean up resources
client_socket.close()
cv2.destroyAllWindows()
print("[CLIENT] Connection closed")
