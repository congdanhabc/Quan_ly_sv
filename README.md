**Chạy ứng dụng:**
 *   **Docker:** Cài đặt Docker Desktop.
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
