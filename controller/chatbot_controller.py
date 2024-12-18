import threading
import tkinter as tk
from tkinter import messagebox
from model.chatbot_model import ChatbotModel

class ChatbotController:
    def __init__(self, view):
        self.view = view
        self.model = ChatbotModel(api_key='your_openai_api_key')
    
    def send_message(self, message):
        """Xử lý gửi tin nhắn"""
        if message.strip():
            # Hiển thị tin nhắn người dùng
            self.view.update_chat_display("Bạn: " + message)
            
            # Lấy phản hồi từ model
            response = self.model.generate_response(message)
            
            # Hiển thị phản hồi
            self.view.update_chat_display("Chatbot: " + response)
    
    def start_speech_recognition(self):
        """Bắt đầu nhận dạng giọng nói"""
        def recognize():
            text = self.model.recognize_speech()
            if text:
                # Cập nhật giao diện từ luồng chính
                self.view.root.after(0, lambda: self.view.message_entry.delete(0, tk.END))
                self.view.root.after(0, lambda: self.view.message_entry.insert(0, text))
            else:
                messagebox.showwarning("Lỗi", "Không thể nhận dạng giọng nói")
        
        # Chạy nhận dạng giọng nói trong luồng riêng
        threading.Thread(target=recognize, daemon=True).start()