import cv2
import socket
import numpy as np

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Server address to send video frames
server_address = ('localhost', 12345)

# Open the video capture device (e.g., camera)
capture = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not capture.isOpened():
    print("Failed to open camera")
    exit()

# Set the maximum packet size
MAX_PACKET_SIZE = 65507  # Maximum UDP packet size

# Read and send video frames
while True:
    # Read a frame from the camera
    ret, frame = capture.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Convert the frame to a suitable format (e.g., JPEG)
    encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()

    # Split the encoded frame into packets and send them sequentially
    packet_size = len(encoded_frame)
    num_packets = int(np.ceil(packet_size / MAX_PACKET_SIZE))

    for i in range(num_packets):
        start = i * MAX_PACKET_SIZE
        end = min((i + 1) * MAX_PACKET_SIZE, packet_size)
        packet = encoded_frame[start:end]

        # Send the packet to the server
        client_socket.sendto(packet, server_address)

# Release the video capture and close the socket
capture.release()
client_socket.close()
