import socket
import cv2
import pickle
import struct

def client_program():
    host = socket.gethostname()
    port = 5123

    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = input(" -> ")
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())

        if message.strip() == 'Error':
            # Video streaming code
            client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            video_port = 9985
            client_socket_video.bind((host, video_port))
            client_socket_video.listen(5)
            print("Waiting for video stream connection at:", (host, video_port))

            conn_video, addr_video = client_socket_video.accept()
            print('Got video stream connection from:', addr_video)

            vid = cv2.VideoCapture(0)

            while vid.isOpened():
                img, frame = vid.read()
                a = pickle.dumps(frame)
                message = struct.pack("Q", len(a)) + a
                conn_video.sendall(message)

                cv2.imshow('Transmitting Video to server', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

            conn_video.close()

        message = input(" -> ")

    client_socket.close()

if __name__ == '__main__':
    client_program()

# import socket
# import cv2
# import pickle
# import struct

# def client_program():
#     host = socket.gethostname()
#     port = 5123

#     client_socket = socket.socket()
#     client_socket.connect((host, port))

#     message = input(" -> ")
#     while message.lower().strip() != 'bye':
#         client_socket.send(message.encode())

#         if message.strip() == 'Error':
#             # Video streaming code
#             client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             video_port = 9985
#             client_socket_video.connect((host, video_port))

#             data = b""
#             payload_size = struct.calcsize("Q")

#             while True:
#                 while len(data) < payload_size:
#                     packet = client_socket_video.recv(4 * 1024)
#                     if not packet:
#                         break
#                     data += packet
#                 packed_msg_size = data[:payload_size]
#                 data = data[payload_size:]
#                 msg_size = struct.unpack("Q", packed_msg_size)[0]

#                 while len(data) < msg_size:
#                     data += client_socket_video.recv(4 * 1024)
#                 frame_data = data[:msg_size]
#                 data = data[msg_size:]
#                 frame = pickle.loads(frame_data)
#                 cv2.imshow("Receiving Video", frame)
#                 key = cv2.waitKey(1) & 0xFF
#                 if key == ord('q'):
#                     break

#             client_socket_video.close()

#         message = input(" -> ")

#     client_socket.close()

# if __name__ == '__main__':
#     client_program()
