import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from tkinter import messagebox
import tkinter as tk
import os
from threading import Thread
import queue

class VoiceRecognitionWindow:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.command_handler = VoiceCommandHandler(dashboard)
        
        # Tạo cửa sổ mới
        self.window = tk.Toplevel()
        self.window.title("Nhận diện giọng nói")
        self.window.geometry("400x300")
        
        # Tạo các thành phần giao diện
        self.create_widgets()
        
        # Khởi tạo các biến điều khiển
        self.is_listening = False
        self.audio_queue = queue.Queue()
        
        # Khởi tạo model
        self.model_path = "venv/Lib/site-packages/vosk-model-small-vn-0.4"
        if os.path.exists(self.model_path):
            self.model = Model(self.model_path)
            self.recognizer = KaldiRecognizer(self.model, 16000)
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy model voice recognition!")
            self.window.destroy()
            return

    def create_widgets(self):
        # Frame chính
        main_frame = tk.Frame(self.window, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Nút Bắt đầu/Dừng
        self.toggle_button = tk.Button(
            main_frame, 
            text="Bắt đầu", 
            command=self.toggle_listening,
            width=20,
            height=2
        )
        self.toggle_button.pack(pady=10)
        
        # Trạng thái
        self.status_label = tk.Label(
            main_frame, 
            text="Trạng thái: Chờ bắt đầu",
            font=("Arial", 10)
        )
        self.status_label.pack(pady=5)
        
        # Khung hiển thị kết quả
        result_frame = tk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(result_frame, text="Kết quả nhận diện:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        # Text widget để hiển thị kết quả
        self.result_text = tk.Text(
            result_frame, 
            height=10, 
            wrap=tk.WORD, 
            font=("Arial", 10)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar cho text widget
        scrollbar = tk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.result_text.yview)

    def toggle_listening(self):
        if not self.is_listening:
            self.start_listening()
        else:
            self.stop_listening()

    def start_listening(self):
        self.is_listening = True
        self.toggle_button.config(text="Dừng")
        self.status_label.config(text="Trạng thái: Đang lắng nghe...")
        
        # Bắt đầu luồng xử lý âm thanh
        self.audio_thread = Thread(target=self.audio_processing_thread)
        self.audio_thread.daemon = True
        self.audio_thread.start()

    def stop_listening(self):
        self.is_listening = False
        self.toggle_button.config(text="Bắt đầu")
        self.status_label.config(text="Trạng thái: Đã dừng")

    def audio_processing_thread(self):
        try:
            def audio_callback(indata, frames, time, status):
                if status:
                    print(f"Trạng thái âm thanh: {status}")
                if self.is_listening:
                    self.audio_queue.put(bytes(indata))

            with sd.RawInputStream(
                samplerate=16000, 
                blocksize=8000, 
                dtype='int16',
                channels=1, 
                callback=audio_callback
            ):
                while self.is_listening:
                    if not self.audio_queue.empty():
                        data = self.audio_queue.get()
                        if self.recognizer.AcceptWaveform(data):
                            result = json.loads(self.recognizer.Result())
                            text = result.get("text", "").strip()
                            if text:
                                self.update_result(text)
                                self.command_handler.process_command(text)

        except Exception as e:
            self.window.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi xử lý âm thanh: {str(e)}"))
            self.stop_listening()

    def update_result(self, text):
        self.window.after(0, lambda: self.add_result_text(text))

    def add_result_text(self, text):
        self.result_text.insert(tk.END, f"➤ {text}\n")
        self.result_text.see(tk.END)

class VoiceCommandHandler:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.commands = {
            "điểm danh": self.handle_attendance,
            "trang chủ": self.go_to_home,
            "quản lý": self.go_to_manager,
            "đổi giao diện": self.toggle_theme,
            "tìm kiếm": self.search_student,
            "gửi email": self.send_email,
            "xuất file": self.export_file,
            "làm mới": self.refresh_data,
            "đóng": self.close_app,
            "trợ giúp": self.show_help,
            "thống kê": self.show_statistics,
            "báo cáo": self.generate_report,
        }
        
    def process_command(self, text):
        """Xử lý văn bản được nhận diện và thực hiện lệnh phù hợp."""
        if not text:  # Kiểm tra text rỗng
            return False
            
        text = text.lower().strip()
        for command, handler in self.commands.items():
            if command in text:
                try:
                    handler(text)
                    return True
                except Exception as e:
                    messagebox.showerror("Lỗi", f"Lỗi khi thực hiện lệnh: {str(e)}")
                    return False
        return False


    # Các hàm xử lý lệnh cụ thể
    def handle_attendance(self, text):
        messagebox.showinfo("Điểm danh", "Đang mở chức năng điểm danh...")
        # TODO: Implement attendance functionality
    
    def go_to_home(self, text):
        self.dashboard.home_page()
        messagebox.showinfo("Điều hướng", "Đã chuyển đến trang chủ")
    
    def go_to_manager(self, text):
        self.dashboard.manager_page()
        messagebox.showinfo("Điều hướng", "Đã chuyển đến trang quản lý")
    
    def toggle_theme(self, text):
        self.dashboard.toggle_theme()
        messagebox.showinfo("Giao diện", "Đã thay đổi theme")
    
    def search_student(self, text):
        # Tách từ khóa tìm kiếm từ câu lệnh
        keywords = text.replace("tìm kiếm", "").strip()
        if keywords:
            messagebox.showinfo("Tìm kiếm", f"Đang tìm kiếm: {keywords}")
            # TODO: Implement search functionality
        else:
            messagebox.showinfo("Tìm kiếm", "Vui lòng nói từ khóa tìm kiếm")

    def send_email(self, text):
        if "hàng loạt" in text:
            messagebox.showinfo("Email", "Đang chuẩn bị gửi email hàng loạt...")
            # TODO: Implement bulk email sending
        else:
            messagebox.showinfo("Email", "Đang chuẩn bị gửi email...")
            # TODO: Implement single email sending
    
    def export_file(self, text):
        if "excel" in text:
            messagebox.showinfo("Xuất file", "Đang xuất file Excel...")
        elif "pdf" in text:
            messagebox.showinfo("Xuất file", "Đang xuất file PDF...")
        else:
            messagebox.showinfo("Xuất file", "Đang xuất dữ liệu...")
        # TODO: Implement export functionality
    
    def refresh_data(self, text):
        messagebox.showinfo("Làm mới", "Đang cập nhật dữ liệu...")
        # TODO: Implement refresh functionality
    
    def close_app(self, text):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đóng ứng dụng?"):
            self.dashboard.root.destroy()
    
    def show_help(self, text):
        help_text = """Các lệnh giọng nói có sẵn:
        - "điểm danh": Mở chức năng điểm danh
        - "trang chủ": Quay về trang chủ
        - "quản lý": Đến trang quản lý
        - "đổi theme": Thay đổi giao diện sáng/tối
        - "tìm kiếm [từ khóa]": Tìm kiếm sinh viên
        - "gửi email": Gửi email
        - "xuất file": Xuất dữ liệu
        - "làm mới": Cập nhật dữ liệu
        - "đóng": Thoát ứng dụng
        - "trợ giúp": Hiển thị hướng dẫn
        - "thống kê": Xem thống kê
        - "báo cáo": Tạo báo cáo"""
        messagebox.showinfo("Hướng dẫn", help_text)
    
    def show_statistics(self, text):
        messagebox.showinfo("Thống kê", "Đang tải thống kê...")
        # TODO: Implement statistics view
    
    def generate_report(self, text):
        messagebox.showinfo("Báo cáo", "Đang tạo báo cáo...")
        # TODO: Implement report generation

# Cập nhật hàm recognize_speech
def recognize_speech(dashboard, handle_result):
    """
    Hàm nhận diện giọng nói.
    Args:
        dashboard: Instance của Dashboard để truy cập các chức năng
        handle_result: Hàm xử lý để hiển thị kết quả
    """
    command_handler = VoiceCommandHandler(dashboard)
    
    # Kiểm tra và tạo đường dẫn model
    model_path = "venv/Lib/site-packages/vosk-model-small-vn-0.4"
    if not os.path.exists(model_path):
        messagebox.showerror("Lỗi", "Không tìm thấy model voice recognition!")
        return

    try:
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)

        def audio_callback(indata, frames, time, status):
            if status:
                print(f"Trạng thái âm thanh: {status}")
                return
            
            try:
                data = bytes(indata)
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").strip()
                    if text:  # Chỉ xử lý khi có text
                        handle_result(text)
                        if not command_handler.process_command(text):
                            messagebox.showwarning(
                                "Lệnh không hợp lệ",
                                "Không hiểu lệnh. Hãy nói 'trợ giúp' để xem danh sách lệnh."
                            )
            except Exception as e:
                print(f"Lỗi trong callback: {str(e)}")

        # Cấu hình stream âm thanh
        stream_config = {
            'samplerate': 16000,
            'blocksize': 8000,
            'dtype': 'int16',
            'channels': 1,
            'callback': audio_callback
        }

        with sd.RawInputStream(**stream_config):
            messagebox.showinfo("Thông báo", "Đang lắng nghe... Nhấn OK sau khi nói xong.")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khởi tạo nhận diện giọng nói: {str(e)}")