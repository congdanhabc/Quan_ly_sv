import openai
import speech_recognition as sr

class ChatbotModel:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
    
    def generate_response(self, message):
        """Tạo phản hồi từ chatbot"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý AI hữu ích"},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Lỗi: {str(e)}"
    
    def recognize_speech(self):
        """Nhận dạng giọng nói"""
        recognizer = sr.Recognizer()
        
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
                
                try:
                    text = recognizer.recognize_google(audio, language="vi-VN")
                    return text
                except sr.UnknownValueError:
                    return None
                except sr.RequestError:
                    return None
        
        except Exception:
            return None