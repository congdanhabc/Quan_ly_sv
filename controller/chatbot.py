import os
from typing import List, Dict
from mem0 import Memory
from datetime import datetime
import google.generativeai as genai
import google.ai.generativelanguage
from controller.student import StudentController
from controller.student_class import Student_ClassController

# Set the OpenAI API key
os.environ["GEMINI_API_KEY"] = "AIzaSyDlYte7TuOdjzAD1szsZrvhNQxEKr5XiAY"

class Chatbot:
    def __init__(self):
        self.student_controller = StudentController()
        self.student_class_controller = Student_ClassController()

        # Khởi tạo Memory 
        self.config = {
        "llm": {
            "provider": "gemini",
            "config": {
                "model": "gemini-2.0-flash-exp",
                "temperature": 0.1,
                "max_tokens": 2000,
                "api_key": os.environ["GEMINI_API_KEY"],
                }
            },
        "embedder": {
            "provider": "gemini",
            "config": {
                "api_key": os.environ["GEMINI_API_KEY"],
                "model": "models/text-embedding-004"
            }
            },
        "vector_store": {
            "provider": "qdrant",
            "config": {
                "embedding_model_dims": 768,
                "collection_name": "mem0",
                "host": "localhost",
                "port": 6333,
                "on_disk": True,
            }
            },
        "version": "v1.1",
        }
        self.memory = Memory.from_config(self.config)
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        # Define support context
        self.system_context = """
        Bạn là là Nghĩa ngu, một trợ lý ảo giúp tôi trong việc quản lý sinh viên.
        Dựa vào câu hỏi của tôi, bạn sẽ đưa ra một trong các lựa chọn sau:
        1. Thêm sinh viên: Chọn lựa chọn này khi tôi hỏi về việc thêm hoặc tạo mới một sinh viên.
        2. Xem sinh viên: Chọn lựa chọn này khi tôi hỏi về việc xem hoặc tìm kiếm một sinh viên đã có.
        3. Khác: Chọn lựa chọn này cho các câu hỏi khác không thuộc hai lựa chọn trên.
        Vui lòng trả lời bằng số thứ tự của lựa chọn (1, 2, hoặc 3) thôi nhé.
        """

    def store_customer_interaction(self,
                                 user_id: str,
                                 message: str,
                                 response: str,
                                 metadata: Dict = None):
        """Store customer interaction in memory."""
        if metadata is None:
            metadata = {}

        # Add timestamp to metadata
        metadata["timestamp"] = datetime.now().isoformat()

        # Format conversation for storage
        conversation = [
            {"role": "user", "content": message},
            {"role": "system", "content": response}
        ]
        # Store in Mem0
        self.memory.add(
            conversation,
            user_id=user_id,
            agent_id="chatbot",
            metadata=metadata,
        )

    def get_relevant_history(self, user_id: str, query: str) -> List[Dict]:
        """Retrieve relevant past interactions."""
        return self.memory.search(
            query=query,
            user_id=user_id,
            limit=5  # Adjust based on needs
        )

    def classify_user_query(self, query: str) -> str:
        """Classify the user's query into a support option."""
        prompt = f"""
        {self.system_context}

        Current user query: {query}

        Provide the option number based on the user's query.
        """
        
        response = self.model.generate_content(prompt)
        return response.text.strip()

    def add_student(self, ma_sinh_vien: str, ho_ten: str, gioi_tinh: str, ngay_sinh: str):
        """Adds a student to the student database."""
        notify = "Lỗi không xác định, thêm sinh viên không thành công"
        if self.student_controller.add_student(ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh):
            notify = f"Đã thêm sinh viên có mã {ma_sinh_vien}."
        return notify

    def search_student_by_name(self, name: str) -> List[Dict]:
        """Searches for students by name and return a list of student's names and ids."""
        results = self.student_controller.search_student_by_name(name)
        return results

    def get_student_profile(self, ma_sinh_vien: str) -> Dict:
        """Retrieves a student's profile by their ID."""
        return self.student_controller.get_student_profile(ma_sinh_vien)

    def handle_customer_query(self, user_id: str, query: str) -> str:
        """Process customer query with context from past interactions."""

        # Get relevant past interactions
        relevant_history = self.get_relevant_history(user_id, query)

        # Build context from relevant history
        context = "Phản hồi trong quá khứ:\n"
        for memory in relevant_history['results']:
            context += f"Phản hồi: {memory['memory']}\n"
            context += "---\n"
        # Classify the user's query
        option = self.classify_user_query(query)

        # Prepare prompt and generate response
        if option == "1": # Add student
            prompt = f"""
                {context}
                Bạn là là Nghĩa ngu, một trợ lý ảo thông minh. Bạn có khả năng ghi nhớ và sử dụng thông tin từ các cuộc trò chuyện trước đây. Nếu có câu hỏi nào về các thông tin từ cuộc trò chuyện của tôi và bạn trong quá khứ, hãy cung cấp cho tôi sự hỗ trợ tốt nhất.

                Câu hỏi: {query}

                Bạn cần xác định các thông tin sau từ tôi: mã sinh viên, họ tên, giới tính, ngày sinh của sinh viên. Nếu chưa có đủ thông tin cần thiết, hãy hỏi lại tôi.
                Sau khi có đủ thông tin, bạn sẽ sử dụng hàm add_student() để thêm sinh viên vào hệ thống.
                Bạn nên hỏi người dùng cho đến khi có đủ các thông tin cần thiết.
                Nếu đã có đủ thông tin, trả về thông báo đã thêm sinh viên.
                """
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()

            # Attempt to extract student info from response
            if "mã sinh viên" in response_text.lower() and "họ tên" in response_text.lower() and "giới tính" in response_text.lower() and "ngày sinh" in response_text.lower():
                try:
                    parts = response_text.split("\n")
                    ma_sinh_vien = ""
                    ho_ten = ""
                    gioi_tinh = ""
                    ngay_sinh = ""
                    for part in parts:
                        if "mã sinh viên" in part.lower():
                            ma_sinh_vien = part.split(":")[-1].strip()
                        if "họ tên" in part.lower():
                            ho_ten = part.split(":")[-1].strip()
                        if "giới tính" in part.lower():
                            gioi_tinh = part.split(":")[-1].strip()
                        if "ngày sinh" in part.lower():
                            ngay_sinh = part.split(":")[-1].strip()

                    if ma_sinh_vien and ho_ten and gioi_tinh and ngay_sinh:
                        add_student_response = self.add_student(ma_sinh_vien, ho_ten, gioi_tinh, ngay_sinh)
                        response_text = add_student_response
                except:
                    response_text = "Tôi cần thêm thông tin để thêm sinh viên. Vui lòng cung cấp mã sinh viên, họ tên, giới tính và ngày sinh."


        elif option == "2": # Find student
            prompt = f"""
                {context}
                Bạn là là Nghĩa ngu, một trợ lý ảo thông minh. Bạn có khả năng ghi nhớ và sử dụng thông tin từ các cuộc trò chuyện trước đây. Nếu có câu hỏi nào về các thông tin từ cuộc trò chuyện của tôi và bạn trong quá khứ, hãy cung cấp cho tôi sự hỗ trợ tốt nhất.

                Hãy xác định tên sinh viên, mã sinh viên được đề cập trong câu hỏi của tôi
                Nếu trong câu hỏi đã có mã sinh viên, trả về cách tìm kiếm là "tìm kiếm theo mã" và mã sinh viên.
                Nếu trong câu hỏi đã có tên sinh viên, trả về cách tìm kiếm là "tìm kiếm theo tên" và tên sinh viên.
                Nếu trong câu hỏi chưa có tên sinh viên hoặc mã sinh viên, bạn cần yêu cầu tôi cung cấp tên hoặc mã sinh viên.

                Câu hỏi: {query}
                """
            response = self.model.generate_content(prompt)            
            response_text = response.text.strip()
            # Attempt to extract student info from response
            if "tìm kiếm theo tên" in response_text.lower():
                try:
                    # Improved extraction: split by "tên:" and get the LAST part (handling extra text)
                    name = response_text.split("Tên sinh viên: ")[1]
                    if name is not None:
                        found_students = self.search_student_by_name(name)
                        if found_students:
                            response_text = "Danh sách sinh viên tìm thấy:\n"
                            for student in found_students:
                                response_text += f"Mã sinh viên: {student.get('MaSinhVien')}, Tên: {student.get('HoTen')}, Giới tính: {student.get('GioiTinh')}, Ngày sinh {student.get('NgaySinh')}\n"
                        else:
                            response_text = "Không tìm thấy sinh viên nào có tên này."
                    else:
                        response_text = "Bạn muốn tìm sinh viên bằng tên hay mã số?"
                except:
                    response_text = "Có lỗi khi tìm sinh viên"
            elif "tìm kiếm theo mã" in response_text.lower():
                try:
                    # Improved extraction: split by "tên:" and get the LAST part (handling extra text)
                    ma_sinh_vien = response_text.split("Mã sinh viên: ")[1]
                    if ma_sinh_vien is not None:
                        profile = self.get_student_profile(ma_sinh_vien)
                        if profile:
                            response_text = f"Thông tin sinh viên:\nMã sinh viên: {profile.get('MaSinhVien')}\nHọ tên: {profile.get('HoTen')}\nGiới tính: {profile.get('GioiTinh')}\nNgày sinh: {profile.get('NgaySinh')}"
                        else:
                            response_text = "Không tìm thấy sinh viên với mã số này."
                    else:
                        response_text = "Bạn muốn tìm sinh viên bằng tên hay mã số?"
                except:
                    response_text = "Có lỗi khi tìm sinh viên"
        else: # option is "3" (other)
            prompt = f"""
            {context}
            Bạn là là Nghĩa ngu, một trợ lý ảo thông minh. Bạn có khả năng ghi nhớ và sử dụng thông tin từ các cuộc trò chuyện trước đây để cung cấp cho tôi sự hỗ trợ tốt nhất.
            {query}
            """
            response = self.model.generate_content(prompt)
            response_text = response.text

        # Store interaction
        self.store_customer_interaction(
            user_id=user_id,
            message=query,
            response=response_text, # Store response text only
            metadata={"type": "support_query"}
        )

        return response_text # Return response text


# chatbot = SupportChatbot()
# user_id = "customer_bot"
# print("Chào bạn, đây là AI chatbot! Nhập 'exit' để dừng cuộc trò chuyện.")

# while True:
#     # Get user input
#     query = input("Người dùng: ")

#     # Check if user wants to exit
#     if query.lower() == 'exit':
#         print("Thank you for using our support service. Goodbye!")
#         break
    
#     # Handle the query and print the response
#     response = chatbot.handle_customer_query(user_id, query)
#     print("Chatbot:", response, "\n\n")