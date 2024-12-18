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

    def send_absent_warning(self, absent_list):
        students_missing_email = []

        for student in absent_list:
            if float(student["ThoiLuong"]) >= 50:
                if is_gmail_at_end(student["EmailSinhVien"]) and is_gmail_at_end(student["EmailPhuHuynh"]):
                    subject = "Cảnh báo học vụ: Vắng mặt vượt quá 50%"
                    message = f"Sinh viên: {student['TenSinhVien']} đã vắng trên 50% số buổi học môn {student['TenMonHoc']}, Yêu cầu sinh viên đi học nghiêm túc hơn nếu không sẽ bị cấm thi."
                    
                    recipients = [
                        student["EmailSinhVien"],
                        student["EmailPhuHuynh"],
                        student["EmailGVCN"],
                        student["EmailTBM"]
                    ]
                    
                    for recipient in recipients:
                        self.email_sender.send_email(recipient, subject, message)
                else:
                    students_missing_email.append(f"{student['MaSinhVien']} - {student['TenSinhVien']}")
            
            elif float(student["ThoiLuong"]) >= 20 and float(student["ThoiLuong"]) < 50:
                if is_gmail_at_end(student["EmailSinhVien"]):
                    subject = "Cảnh báo học vụ: Vắng mặt vượt quá 20%"
                    message = f"Sinh viên: {student['TenSinhVien']} đã vắng trên 20% số buổi học môn {student['TenMonHoc']}, Yêu cầu sinh viên đi học nghiêm túc hơn."
                    self.email_sender.send_email(student["EmailSinhVien"], subject, message)
                else:
                    students_missing_email.append(f"{student['MaSinhVien']} - {student['TenSinhVien']}")

        return students_missing_email

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
