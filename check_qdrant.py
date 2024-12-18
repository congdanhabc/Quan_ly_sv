from qdrant_client import QdrantClient, models
from qdrant_client.http.exceptions import ResponseHandlingException, UnexpectedResponse
import tkinter as tk
from tkinter import messagebox
import sys


def check_qdrant_connection():
    try:
        client = QdrantClient(host="localhost", port=6333)
        client.get_collection("mem0")  # Thử gọi một API đơn giản để kiểm tra kết nối
        return True
    except ResponseHandlingException:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Kết Nối Qdrant", "Không thể kết nối đến Qdrant. Vui lòng kiểm tra xem Qdrant đã được chạy chưa")
        sys.exit() 
    except UnexpectedResponse as e:
        if r'"error":"Not found: Collection `mem0` doesn\'t exist!"' in str(e):
            client.recreate_collection(
              collection_name="mem0",
               vectors_config=models.VectorParams(size=768, distance=models.Distance.COSINE),
            )
            print(f"Collection 'mem0' created successfully.")
    except Exception as e:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Kết Nối Qdrant", "Có lỗi không xác định")
        print(e)
        sys.exit()