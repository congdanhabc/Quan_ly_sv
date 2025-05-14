# Hệ Thống Quản Lý Điểm Danh Sinh Viên Thông Qua Giọng Nói 📢

## Tổng Quan 🌟
Dự án này phát triển một hệ thống quản lý điểm danh sinh viên dựa trên giọng nói nhằm tự động hóa và đơn giản hóa quy trình điểm danh trong môi trường giáo dục. Sử dụng công nghệ nhận diện giọng nói và giao diện thân thiện, hệ thống giúp giảng viên quản lý điểm danh hiệu quả, giảm sai sót thủ công và tiết kiệm thời gian. Hệ thống tích hợp chatbot AI để hỗ trợ tương tác tự nhiên thông qua lệnh giọng nói.

## Tính Năng ✨
- **Nhận Diện Giọng Nói** 🎙️: Xác định danh tính sinh viên qua giọng nói trong thời gian thực.
- **Quản Lý Điểm Danh** 📋: Ghi nhận và quản lý dữ liệu điểm danh, bao gồm thời gian và trạng thái sinh viên.
- **Giao Diện Thân Thiện** 🖥️: Bao gồm giao diện đăng nhập, đăng ký, quản lý sinh viên, quản lý học vụ và chatbot.
- **Lưu Trữ Dữ Liệu** 💾: Lưu thông tin sinh viên, điểm danh và giảng viên trong cơ sở dữ liệu SQLite nhẹ.
- **Chatbot AI** 🤖: Cho phép tương tác tự nhiên để hỗ trợ các tác vụ điểm danh và truy vấn hệ thống.
- **Khả Năng Mở Rộng** 🚀: Được thiết kế để hỗ trợ nhiều lớp học và cơ sở giáo dục với tiềm năng mở rộng trong tương lai.

## Công Nghệ Sử Dụng 🛠️
- **Ngôn Ngữ Lập Trình**: Python 🐍
- **Nhận Diện Giọng Nói**:
  - SpeechRecognition (thư viện Python) 🎤
  - Google Speech API (chuyển giọng nói thành văn bản dựa trên đám mây) ☁️
- **Xử Lý Âm Thanh**:
  - PyAudio (thu âm) 🔊
  - Librosa (phân tích tín hiệu âm thanh) 📊
- **Cơ Sở Dữ Liệu**: SQLite 🗄️
- **Giao Diện Người Dùng**: Tkinter 🖼️
- **Công Cụ Phát Triển**:
  - Visual Studio Code (IDE) 💻
  - GitHub (quản lý mã nguồn) 📂

## Yêu Cầu Cài Đặt 📋
- Python 3.8 trở lên
- Kết nối internet ổn định (cho Google Speech API)
- Micro để nhập giọng nói
- Git (để tải mã nguồn)

## Hướng Dẫn Cài Đặt 🛠️
1. **Tải Mã Nguồn**:
   ```bash
   git clone https://github.com/your-repo/voice-attendance-system.git
   cd voice-attendance-system
   ```

2. **Tạo Môi Trường Ảo** (khuyến nghị):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   ```

3. **Cài Đặt Thư Viện**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Cài Đặt Thư Viện Âm Thanh**:
   - Đảm bảo PyAudio được cài đặt. Trên một số hệ thống, cần cài `portaudio` trước:
     ```bash
     # Trên macOS
     brew install portaudio
     # Trên Ubuntu
     sudo apt-get install libasound-dev portaudio19-dev
     ```

5. **Cấu Hình Google Speech API** (nếu cần):
   - Lấy thông tin xác thực từ Google Cloud Console và thiết lập biến môi trường:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="đường/dẫn/đến/tệp/credentials.json"
     ```

## Hướng Dẫn Sử Dụng 🚀
1. **Khởi Chạy Ứng Dụng**:
 *   **Docker🐳:** Cài đặt Docker Desktop.
 *   Mở terminal hoặc command prompt **tại thư mục gốc của dự án**.
 *   Lệnh chạy Qdrant:
     ```bash
     docker run -d --name qdrant_db -p 6333:6333 -p 6334:6334 -v "${PWD}/qdrant_storage:/qdrant/storage" qdrant/qdrant:latest
     ```
*   Chạy lệnh sau để cài đặt các thư viện:
    ```bash
    pip install -r requirements.txt
    ```
*   Chạy ứng dụng:
    ```bash
    python main.py
    ```

2. **Tương Tác Với Hệ Thống**:
   - **Đăng Nhập** 🔑: Sử dụng giao diện đăng nhập để truy cập với tư cách giảng viên.
   - **Đăng Ký** 📝: Tạo tài khoản giảng viên mới nếu cần.
   - **Điểm Danh** 🎙️: Sử dụng giao diện nhận diện giọng nói để điểm danh bằng cách nói tên hoặc mã số sinh viên.
   - **Quản Lý Sinh Viên** 👩‍🎓: Xem và cập nhật thông tin sinh viên.
   - **Quản Lý Học Vụ** 📚: Gửi email, đưa ra cảnh báo hoặc tạo báo cáo vắng mặt.
   - **Chatbot** 🤖: Tương tác với chatbot AI để được hỗ trợ các tác vụ điểm danh.

3. **Quy Trình Mẫu**:
   - Đăng nhập vào hệ thống.
   - Chuyển đến giao diện điểm danh.
   - Nói tên hoặc mã số sinh viên để ghi nhận điểm danh.
   - Xem tóm tắt điểm danh trong giao diện quản lý.

## Hạn Chế ⚠️
- **Tiếng Ồn Môi Trường** 🌬️: Độ chính xác nhận diện giọng nói có thể giảm trong môi trường ồn ào.
- **Giọng Nói Không Chuẩn** 🗣️: Hệ thống có thể gặp khó khăn với giọng nói có phương ngữ hoặc phát âm không rõ.
- **Phụ Thuộc Internet** 🌐: Yêu cầu kết nối internet ổn định cho Google Speech API.

## Cải Tiến Trong Tương Lai 🔮
- Cải thiện độ chính xác nhận diện giọng nói trong môi trường ồn ào.
- Tích hợp phương thức xác thực khác (như nhận diện khuôn mặt hoặc quét mã QR).
- Phát triển ứng dụng di động để tăng khả năng truy cập.
- Thêm tính năng báo cáo phân tích điểm danh nâng cao.
- Cải thiện giao diện người dùng để phù hợp với nhiều đối tượng hơn.

## Đóng Góp 👥
- **Phan Tài Nguyên** (3121411151)
- **Nguyễn Công Danh** (3121411035)
- **Võ Văn Nhân** (3121411156)
- **Giảng Viên Hướng Dẫn**: Trần Quang Huy

## Giấy Phép 📜
Dự án được cấp phép theo Giấy phép MIT. Xem tệp [LICENSE](LICENSE) để biết chi tiết.

## Lời Cảm Ơn 🙏
- **Tài Liệu Tham Khảo**:
  - Phạm Văn Át - *Giáo trình lập trình Python cơ bản và nâng cao*
  - Lê Minh Hoàng - *Trí tuệ nhân tạo: Cơ sở và ứng dụng*
  - Allen B. Downey - *Think Python: How to Think Like a Computer Scientist*
  - Steven Bird và cộng sự - *Natural Language Processing with Python*
  - Matthew A. Russell - *Mining the Social Web*

Để biết thêm chi tiết, liên hệ với các thành viên nhóm hoặc tham khảo tài liệu dự án.
