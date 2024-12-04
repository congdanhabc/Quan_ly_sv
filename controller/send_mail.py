import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import os
import pandas as pd

#Gửi mail cảnh báo
def send_email(recipient, subject, body):
    sender_email = "cd5112003@gmail.com"
    sender_password = "bnzn mgdp icbb cjyy"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)

    msg['To'] = recipient
    text = msg.as_string()
    server.sendmail(sender_email, recipient, text)

    server.quit()

def send_absent_warning(absent_list):
    students_missing_email = []

    for student in absent_list:
        if float(student["ThoiLuong"]) >= 50:
            if is_gmail_at_end(student["EmailSinhVien"]) and is_gmail_at_end(student["EmailPhuHuynh"]):
                subject = "Cảnh báo học vụ: Vắng mặt vượt quá 50%"
                message = f"Sinh viên: {student["TenSinhVien"]} đã vắng trên 50% số buổi học môn {student["TenMonHoc"]}, Yêu câù sinh viên đi học nghiêm túc hơn nếu không sẽ bị cấm thi."
                send_email(student["EmailSinhVien"], subject, message)
                send_email(student["EmailPhuHuynh"], subject, message)
                send_email(student["EmailGVCN"], subject, message)
                send_email(student["EmailTBM"], subject, message)
            else:
                students_missing_email.append(f"{student["MaSinhVien"]} - {student["TenSinhVien"]}")
        elif float(student["ThoiLuong"]) >= 20 and float(student["ThoiLuong"]) < 50:
            if is_gmail_at_end(student["EmailSinhVien"]):
                subject = "Cảnh báo học vụ: Vắng mặt vượt quá 20%"
                message = f"Sinh viên: {student["TenSinhVien"]} đã vắng trên 50% số buổi học môn {student["TenMonHoc"]}, Yêu câù sinh viên đi học nghiêm túc hơn."
                send_email(student["EmailSinhVien"], subject, message)
            else:
                students_missing_email.append(f"{student["MaSinhVien"]} - {student["TenSinhVien"]}")
                

    return students_missing_email

def is_gmail_at_end(email): 
    return email.endswith("@gmail.com")

#Gửi excel
def send_excel_report(absent_list):
     # Lọc dữ liệu
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
    # Chuyển đổi dữ liệu thành DataFrame
    df = pd.DataFrame(filtered_data)
    # Ghi dữ liệu vào file Excel
    file_path = 'bao_cao_vang.xlsx'
    df.to_excel(file_path, index=False)
    send_email_with_attachment(file_path)

def send_email_with_attachment(file_path):
    sender_email = "cd5112003@gmail.com"
    sender_password = "bnzn mgdp icbb cjyy"
    recipient = "abcxyz544000@gmail.com"
    subject = "Thông tin chuyên cần của sinh viên"
    body = "Danh sách thông tin của các sinh viên về việc chuyên cần."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Đính kèm file Excel
    attachment = MIMEBase('application', 'octet-stream')
    with open(file_path, 'rb') as attachment_file:
        attachment.set_payload(attachment_file.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
    msg.attach(attachment)

    # Kết nối tới server và gửi email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    msg['To'] = recipient
    text = msg.as_string()
    server.sendmail(sender_email, recipient, text)
    server.quit()

    # Xóa file sau khi gửi email
    if os.path.exists(file_path):
        os.remove(file_path)


