import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from pdf_soru_uretici import read_pdf, generate_questions  # güncellendi

# PDF seçme
def select_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        entry_pdf_path.delete(0, tk.END)
        entry_pdf_path.insert(0, file_path)

# Soruları üretme ve ekranda gösterme
def run_question_generator():
    pdf_path = entry_pdf_path.get()
    if not pdf_path:
        messagebox.showerror("Hata", "Lütfen bir PDF dosyası seçin.")
        return

    try:
        pdf_text = read_pdf(pdf_path)
        if not pdf_text:
            messagebox.showerror("Hata", "PDF metni okunamadı.")
            return

        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Sorular üretiliyor, lütfen bekleyin...\n")
        root.update()

        questions = generate_questions(pdf_text)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, questions)

    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu: {e}")

# Soruları kaydetme
def save_questions():
    content = output_text.get(1.0, tk.END).strip()
    if not content:
        messagebox.showerror("Hata", "Kaydedilecek bir soru yok.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Başarılı", f"Sorular kaydedildi: {file_path}")

# Oval card çizen fonksiyon
def create_rounded_card(canvas, x, y, width, height, radius=25, color="#fff"):
    points = [x+radius, y,
              x+width-radius, y,
              x+width, y,
              x+width, y+radius,
              x+width, y+height-radius,
              x+width, y+height,
              x+width-radius, y+height,
              x+radius, y+height,
              x, y+height,
              x, y+height-radius,
              x, y+radius,
              x, y]
    return canvas.create_polygon(points, smooth=True, fill=color, outline="")

# Tkinter arayüz
root = tk.Tk()
root.title("📄 PDF'ten 10 Soruluk Test Üretici")
root.geometry("900x750")
root.configure(bg="#f0f2f5")

# Üst card (PDF seçme + butonlar)
canvas_top = tk.Canvas(root, width=860, height=120, bg="#f0f2f5", highlightthickness=0)
canvas_top.pack(pady=15)
create_rounded_card(canvas_top, 0, 0, 860, 120, radius=25, color="#ffffff")

frame_top = tk.Frame(canvas_top, bg="#ffffff")
frame_top.place(relx=0.5, rely=0.5, anchor="center")

entry_pdf_path = tk.Entry(frame_top, width=50, font=("Segoe UI", 10))
entry_pdf_path.grid(row=0, column=0, padx=10, pady=20)

btn_select = tk.Button(frame_top, text="📂 Seç", command=select_pdf, bg="#dbeafe", fg="#1e40af",
                       font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8)
btn_select.grid(row=0, column=1, padx=5)

btn_generate = tk.Button(frame_top, text="✨ Soruları Üret", command=run_question_generator, bg="#bbf7d0", fg="#166534",
                         font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8)
btn_generate.grid(row=0, column=2, padx=5)

btn_save = tk.Button(frame_top, text="💾 Kaydet", command=save_questions, bg="#fde68a", fg="#92400e",
                     font=("Segoe UI", 10, "bold"), relief="flat", padx=15, pady=8)
btn_save.grid(row=0, column=3, padx=5)

# Alt card (soru kutusu)
canvas_bottom = tk.Canvas(root, width=860, height=550, bg="#f0f2f5", highlightthickness=0)
canvas_bottom.pack()
create_rounded_card(canvas_bottom, 0, 0, 860, 550, radius=25, color="#ffffff")

frame_bottom = tk.Frame(canvas_bottom, bg="#ffffff")
frame_bottom.place(relx=0.5, rely=0.5, anchor="center")

output_text = scrolledtext.ScrolledText(frame_bottom, wrap=tk.WORD, width=95, height=28, font=("Segoe UI", 10), relief="flat", borderwidth=0)
output_text.pack(padx=20, pady=20)

root.mainloop()
