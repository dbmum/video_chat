import cv2
import socket
import numpy as np

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific IP address and port
client_address = ('localhost', 54321)
client_socket.bind(client_address)

# OpenCV window to display the received video frames
cv2.namedWindow('Client Video')

# Receive and display video frames
while True:
    # Receive a video frame from the server
    encoded_frame, address = client_socket.recvfrom(65536)  # Adjust buffer size as needed

    # Decode the received frame
    frame = cv2.imdecode(np.frombuffer(encoded_frame, np.uint8), cv2.IMREAD_COLOR)

    if frame is not None:
        # Display the received frame
        cv2.imshow('Client Video', frame)

    # Check for 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the socket and destroy the OpenCV window
client_socket.close()
cv2.destroyAllWindows()
