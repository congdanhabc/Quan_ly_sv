import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import os
import pandas as pd
import threading
from queue import Queue
import time
import re

class EmailSender:
    def __init__(self):
        self.sender_email = "cd5112003@gmail.com"
        self.sender_password = "bnzn mgdp icbb cjyy"
        self.email_queue = Queue()
        self.worker_thread = threading.Thread(target=self._process_email_queue, daemon=True)
        self.worker_thread.start()

    def _send_single_email(self, recipient, subject, body, attachment=None):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            if attachment:
                attachment_part = MIMEBase('application', 'octet-stream')
                with open(attachment, 'rb') as attachment_file:
                    attachment_part.set_payload(attachment_file.read())
                encoders.encode_base64(attachment_part)
                attachment_part.add_header(
                    'Content-Disposition',
                    f'attachment; filename={os.path.basename(attachment)}'
                )
                msg.attach(attachment_part)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()
            server.sendmail(self.sender_email, recipient, text)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email to {recipient}: {str(e)}")
            return False

    def _process_email_queue(self):
        while True:
            if not self.email_queue.empty():
                email_data = self.email_queue.get()
                self._send_single_email(
                    email_data['recipient'],
                    email_data['subject'],
                    email_data['body'],
                    email_data.get('attachment')
                )
                self.email_queue.task_done()
            time.sleep(0.1)  # Tránh CPU quá tải

    def send_email(self, recipient, subject, body, attachment=None):
        self.email_queue.put({
            'recipient': recipient,
            'subject': subject,
            'body': body,
            'attachment': attachment
        })

def is_gmail_at_end(email): 
    return email.endswith("@gmail.com")

class AbsenteeManager:
    def __init__(self):
        self.email_sender = EmailSender()

    def get_students_missing_gmail(self, absent_list):
        """
        Lấy danh sách sinh viên chưa có email Gmail hợp lệ.
        Args:
            absent_list (list): Danh sách sinh viên vắng mặt.
        Returns:
            list: Danh sách sinh viên chưa có Gmail hợp lệ.
        """
        students_missing_gmail = []

        for student in absent_list:
            # Kiểm tra Gmail của sinh viên và phụ huynh
            if not is_gmail_at_end(student.get("EmailSinhVien", "")) or not is_gmail_at_end(student.get("EmailPhuHuynh", "")):
                students_missing_gmail.append({
                    "MaSinhVien": student["MaSinhVien"],
                    "TenSinhVien": student["TenSinhVien"],
                    "EmailSinhVien": student.get("EmailSinhVien", "Không có"),
                    "EmailPhuHuynh": student.get("EmailPhuHuynh", "Không có")
                })

        return students_missing_gmail


    def send_excel_report(self, absent_list):
        filtered_data = [
            {
                "Mã Sinh Viên": student["MaSinhVien"],
                "Tên Sinh Viên": student["TenSinhVien"],
                "Tên Môn Học": student["TenMonHoc"],
                "Số Buổi": student["SoBuoi"],
                "Thời Lượng (%)": student["ThoiLuong"],
            }
            for student in absent_list
        ]
        
        df = pd.DataFrame(filtered_data)
        file_path = 'bao_cao_vang.xlsx'
        df.to_excel(file_path, index=False)
        
        self.email_sender.send_email(
            "abcxyz544000@gmail.com",
            "Thông tin chuyên cần của sinh viên",
            "Danh sách thông tin của các sinh viên về việc chuyên cần.",
            file_path
        )

        # Xóa file sau khi đã gửi
        if os.path.exists(file_path):
            os.remove(file_path)

    def is_valid_email(self, email):
        """
        Kiểm tra xem địa chỉ email có hợp lệ không.
        Args:
            email (str): Địa chỉ email cần kiểm tra.
        Returns:
            bool: True nếu hợp lệ, False nếu không hợp lệ.
        """
        if not email:
            return False
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None

    def send_bulk_emails(self, absent_list):
        """
        Gửi email hàng loạt cho danh sách sinh viên vắng mặt.
        Args:
            absent_list (list): Danh sách sinh viên vắng mặt, mỗi mục là một dictionary chứa thông tin sinh viên.
        Returns:
            tuple: (số email thành công, số email thất bại, danh sách lỗi)
        """
        success_count = 0
        failure_count = 0
        error_list = []

        for student in absent_list:
            email = student.get("EmailSinhVien")
            if self.is_valid_email(email):
                subject = "Cảnh báo học vụ: Vắng mặt vượt quá 50%"
                message = f"""Sinh viên: {student['TenSinhVien']} đã vắng trên 50% số buổi học môn {student['TenMonHoc']}.\n
    Yêu cầu sinh viên đi học nghiêm túc hơn nếu không sẽ bị cấm thi."""
                try:
                    self.email_sender.send_email(email, subject, message)
                    success_count += 1
                except Exception as e:
                    failure_count += 1
                    error_list.append(f"{student['MaSinhVien']} - {student['TenSinhVien']}: {str(e)}")
            else:
                failure_count += 1
                error_list.append(f"{student['MaSinhVien']} - {student['TenSinhVien']}: Email không hợp lệ ({email}).")

        return success_count, failure_count, error_list


    def send_email_for_student(self, student_info):
        """
        Gửi email cho một sinh viên cụ thể.
        Args:
            student_info (dict): Thông tin sinh viên bao gồm email và các dữ liệu cần thiết.
        """
        email = student_info.get("EmailSinhVien")
        if not self.is_valid_email(email):
            return False, f"Email không hợp lệ: {email}"

        try:
            subject = "Cảnh báo học vụ: Vắng mặt vượt quá 50%"
            message = f"""Sinh viên: {student_info['TenSinhVien']} đã vắng trên 50% số buổi học môn {student_info['TenMonHoc']}.\n
    Yêu cầu sinh viên đi học nghiêm túc hơn nếu không sẽ bị cấm thi."""

            self.email_sender.send_email(email, subject, message)
            return True, f"Email đã gửi đến {email}."
        except Exception as e:
            return False, str(e)
