import cv2
import socket
import numpy as np

# Create UDP sockets for receiving and sending video frames
server_receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the receiving socket to a specific IP address and port
server_address = ('localhost', 12345)
server_receive_socket.bind(server_address)

# Address of the client to send video frames
client_address = ('localhost', 54321)

# OpenCV window to display the received video frames
cv2.namedWindow('Server Video')

# Receive and send video frames
while True:
    # Receive a video frame from the client
    encoded_frame, address = server_receive_socket.recvfrom(65536)  # Adjust buffer size as needed

    # Decode the received frame
    frame = cv2.imdecode(np.frombuffer(encoded_frame, np.uint8), cv2.IMREAD_COLOR)

    if frame is not None:
        # Display the received frame
        cv2.imshow('Server Video', frame)

        # Send the received frame to the other client
        server_send_socket.sendto(encoded_frame, client_address)

    # Check for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the sockets and close the OpenCV window
server_receive_socket.close()
server_send_socket.close()
cv2.destroyAllWindows()