import socket
import cv2
import pickle
import struct

def server_program():
    # host = socket.gethostname()
    host = "192.168.250.210"
    
    port = 3298

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()

    print("Connection from: " + str(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        if data.lower() == "error":
            print("Critical alert")
            # Video streaming code
            client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            video_host = "192.168.250.79"
            video_port = 3033
            client_socket_video.connect((video_host, video_port))

            data = b""
            payload_size = struct.calcsize("Q")

            while True:
                while len(data) < payload_size:
                    packet = client_socket_video.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += client_socket_video.recv(4 * 1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("Receiving Video from client", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

            client_socket_video.close()

        else:
            print("From connected user: " + str(data))

    conn.close()

if __name__ == '__main__':
    server_program()


# import socket
# import cv2
# import pickle
# import struct

# def server_program():
#     host = socket.gethostname()
#     port = 5123

#     server_socket = socket.socket()
#     server_socket.bind((host, port))
#     server_socket.listen(1)
#     conn, address = server_socket.accept()

#     print("Connection from: " + str(address))

#     while True:
#         data = conn.recv(1024).decode()
#         if not data:
#             break

#         if data.lower() == "error":
#             print("Critical alert")
#             # Video streaming code
#             server_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             host_name = socket.gethostname()
#             print("Host name:", host_name)
#             host_ip = socket.gethostbyname(host_name)
#             print('Host IP:', host_ip)
#             video_port = 9985
#             socket_address_video = (host_ip, video_port)
#             server_socket_video.bind(socket_address_video)
#             server_socket_video.listen(5)
#             print("Listening for video stream at:", socket_address_video)

#             client_socket_video, addr_video = server_socket_video.accept()
#             print('Got video stream connection from:', addr_video)

#             vid = cv2.VideoCapture(0)

#             while vid.isOpened():
#                 img, frame = vid.read()
#                 a = pickle.dumps(frame)
#                 message = struct.pack("Q", len(a)) + a
#                 client_socket_video.sendall(message)

#                 cv2.imshow('Transmitting Video', frame)
#                 key = cv2.waitKey(1) & 0xFF
#                 if key == ord('q'):
#                     client_socket_video.close()
#                     break

#         else:
#             print("From connected user: " + str(data))

#     conn.close()

# if __name__ == '__main__':
#     server_program()
