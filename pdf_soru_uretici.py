import fitz  # PyMuPDF
import subprocess

def read_pdf(file_path):
    """PDF dosyasından metni okur"""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()

def generate_questions(text):
    """Mistral ile 10 adet çoktan seçmeli TÜRKÇE soru üretir"""
    prompt = f"""
Sen bir öğretmensin. Aşağıdaki metinden tam olarak 10 adet çoktan seçmeli soru üret.

Kurallar:
- Sorular TÜRKÇE olacak.
- Her sorunun başında (Bilgi), (Analiz) veya (Değerlendirme) yazacak.
- Her soruda **mutlaka** 4 şık olacak: A), B), C), D) şeklinde.
- Şıklar kısa ve net olacak.
- Sadece 1 doğru cevap olacak.
- Her sorunun altında "Doğru cevap: X" yazacak.
- Gereksiz açıklama ekleme, sadece soru, şıklar ve doğru cevabı ver.

📌 ÖRNEK FORMAT:
Soru (Bilgi): Türkiye Cumhuriyeti ne zaman ilan edilmiştir?
A) 1921
B) 1922
C) 1923
D) 1924
Doğru cevap: C

Metin:
{text}

Yukarıdaki formatı kullanarak tam olarak 10 adet çoktan seçmeli soru üret.
"""
    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt.encode(),
        capture_output=True
    )
    return result.stdout.decode()
