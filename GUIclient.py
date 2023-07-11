import socket
import cv2
import pickle
import struct
import tkinter as tk
from tkinter import ttk
import threading

class ClientGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Client")

        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#e1d8b9")
        self.style.configure("TButton", background="#7a9eb1", foreground="white")
        self.style.configure("TLabel", background="#e1d8b9", foreground="#333333", font=("Arial", 12))
        self.style.configure("TText", background="#ffffff", foreground="#333333", font=("Arial", 11))

        self.frame = ttk.Frame(self.window)
        self.frame.pack(padx=20, pady=20)

        self.text_area = tk.Text(self.frame, height=10, width=40)
        self.text_area.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.message_entry = ttk.Entry(self.frame)
        self.message_entry.grid(row=1, column=0, padx=5, pady=5)

        self.send_button = ttk.Button(self.frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    def send_message(self):
        message = self.message_entry.get()
        self.text_area.insert(tk.END, "-> " + message + "\n")

        if message.lower().strip() == 'bye':
            self.text_area.insert(tk.END, "Client disconnected.\n")
            self.send_button.config(state=tk.DISABLED)
            self.message_entry.config(state=tk.DISABLED)
        else:
            self.message_entry.delete(0, tk.END)

        self.client_thread = threading.Thread(target=self.client_program, args=(message,))
        self.client_thread.start()

    def client_program(self, message):
        host = socket.gethostname()
        port = 3296

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        client_socket.send(message.encode())

        if message.strip() == 'error':
            self.text_area.insert(tk.END, "Starting video stream...\n")
            # Video streaming code
            client_socket_video = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            video_port = 5323
            client_socket_video.connect((host, video_port))

            while True:
                data = b""
                payload_size = struct.calcsize("L")

                while len(data) < payload_size:
                    packet = client_socket_video.recv(4 * 1024)
                    if not packet:
                        break
                    data += packet

                if not data:
                    break

                message_size = struct.unpack("L", data[:payload_size])[0]
                data = data[payload_size:]

                while len(data) < message_size:
                    data += client_socket_video.recv(4 * 1024)

                frame_data = data[:message_size]
                data = data[message_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow("Receiving Video from server", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break

            client_socket_video.close()

        client_socket.close()

    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    client_gui = ClientGUI()
    client_gui.run()
