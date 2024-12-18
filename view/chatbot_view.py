import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from controller.chatbot_controller import ChatbotController

class ChatbotView:
    def __init__(self, root):
        self.root = root
        self.controller = ChatbotController(self)
        
        self.chatbot_window = tk.Toplevel(root)
        self.chatbot_window.title("AI Chatbot")
        self.chatbot_window.geometry("500x600")
        
        # Khung hiển thị tin nhắn
        self.chat_display = tk.Text(self.chatbot_window, state='disabled', wrap=tk.WORD)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Khung nhập tin nhắn
        input_frame = tk.Frame(self.chatbot_window)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Ô nhập tin nhắn
        self.message_entry = tk.Entry(input_frame, width=40)
        self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0,10))
        
        # Nút micro
        mic_icon = Image.open("assets/mic.png")
        mic_icon = mic_icon.resize((25, 25), Image.LANCZOS)
        self.mic_icon = ImageTk.PhotoImage(mic_icon)
        
        mic_button = tk.Button(input_frame, image=self.mic_icon, 
                               command=self.start_speech_recognition, 
                               bd=0)
        mic_button.pack(side=tk.RIGHT)
        
        # Nút gửi
        send_button = tk.Button(input_frame, text="Gửi", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=5)
    
    def send_message(self):
        message = self.message_entry.get()
        self.controller.send_message(message)
        self.message_entry.delete(0, tk.END)
    
    def start_speech_recognition(self):
        self.controller.start_speech_recognition()
    
    def update_chat_display(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)