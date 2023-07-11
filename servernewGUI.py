import socket
import cv2
import pickle
import struct
import tkinter as tk
import threading

class ServerGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Server")
        
        self.text_area = tk.Text(self.window)
        self.text_area.pack()

        self.start_button = tk.Button(self.window, text="Start Server", command=self.start_server)
        self.start_button.pack()

    def start_server(self):
        self.start_button.config(state=tk.DISABLED)
        self.text_area.insert(tk.END, "Server started.\n")
        
        self.server_thread = threading.Thread(target=self.server_program)
        self.server_thread.start()

    def server_program(self):
        host = socket.gethostname()
        port = 3296

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(2)

        conn, address = server_socket.accept()
        self.text_area.insert(tk.END, "Connection from: " + str(address) + "\n")

        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            if data.lower() == 'error':
                self.text_area.insert(tk.END, "Critical alert\n")
                # Video streaming code
                client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                video_port = 5323
                client_socket_video.bind((host, video_port))
                client_socket_video.listen(5)
                self.text_area.insert(tk.END, "Waiting for video stream connection at: " + str((host, video_port)) + "\n")

                conn_video, addr_video = client_socket_video.accept()
                self.text_area.insert(tk.END, "Got video stream connection from: " + str(addr_video) + "\n")

                vid = cv2.VideoCapture(0)

                while True:
                    ret, frame = vid.read()
                    if not ret:
                        break

                    data = pickle.dumps(frame)
                    message_size = struct.pack("L", len(data))

                    try:
                        conn_video.sendall(message_size + data)
                    except:
                        break

                    cv2.imshow('Transmitting Video to server', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break

                conn_video.close()

            else:
                self.text_area.insert(tk.END, "From connected user: " + str(data) + "\n")

        conn.close()

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    server_gui = ServerGUI()
    server_gui.run()