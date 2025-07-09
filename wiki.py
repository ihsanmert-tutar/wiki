import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import wikipedia

wikipedia.set_lang("tr")
dil = "tr"

def dil_degistir(secim):
    global dil
    if secim == "Türkçe":
        wikipedia.set_lang("tr")
        dil = "tr"
    else:
        wikipedia.set_lang("en")
        dil = "en"
    messagebox.showinfo("Dil Değişti", f"Wikipedia dili: {secim}")

def ara():
    konu = entry.get()
    if not konu:
        messagebox.showwarning("Uyarı", "Lütfen bir konu girin.")
        return
    try:
        ozet = wikipedia.summary(konu)
        baslik = wikipedia.page(konu).title
        sonuc_ozet.delete(1.0, tk.END)
        sonuc_baslik.delete(1.0, tk.END)
        sonuc_baslik.insert(tk.END, baslik)
        sonuc_ozet.insert(tk.END, ozet)
    except wikipedia.exceptions.DisambiguationError as e:
        sonuc_ozet.delete(1.0, tk.END)
        sonuc_ozet.insert(tk.END, f"⚠️ Çok anlamlı sonuç:\n\n{', '.join(e.options[:5])}")
    except wikipedia.exceptions.PageError:
        sonuc_ozet.delete(1.0, tk.END)
        sonuc_ozet.insert(tk.END, "❌ Sayfa bulunamadı.")

def temizle():
    entry.delete(0, tk.END)
    sonuc_baslik.delete(1.0, tk.END)
    sonuc_ozet.delete(1.0, tk.END)

def kaydet_txt():
    text = sonuc_ozet.get(1.0, tk.END)
    if not text.strip():
        messagebox.showwarning("Uyarı", "Kaydedilecek bir içerik yok.")
        return
    dosya = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if dosya:
        with open(dosya, "w", encoding="utf-8") as f:
            f.write(text)
        messagebox.showinfo("Başarılı", "Özet başarıyla kaydedildi.")

def tam_icerik_goster():
    konu = entry.get()
    if not konu:
        messagebox.showwarning("Uyarı", "Lütfen bir konu girin.")
        return
    try:
        sayfa = wikipedia.page(konu)
        tam_metin = sayfa.content

        icerik_pencere = tk.Toplevel(pencere)
        icerik_pencere.title(f"{konu} - Tam İçerik")
        icerik_pencere.geometry("800x600")

        metin_alani = scrolledtext.ScrolledText(icerik_pencere, wrap=tk.WORD, font=("Arial", 11))
        metin_alani.pack(expand=True, fill="both", padx=10, pady=10)
        metin_alani.insert(tk.END, tam_metin)
    except wikipedia.exceptions.DisambiguationError as e:
        messagebox.showerror("Hata", f"Çok anlamlı sonuç: {', '.join(e.options[:5])}")
    except wikipedia.exceptions.PageError:
        messagebox.showerror("Hata", "Sayfa bulunamadı.")

# Arayüz
pencere = tk.Tk()
pencere.title("Gelişmiş Wikipedia Özetleyici")
pencere.geometry("900x600")

dil_menusu = ttk.Combobox(pencere, values=["Türkçe", "English"])
dil_menusu.set("Türkçe")
dil_menusu.bind("<<ComboboxSelected>>", lambda e: dil_degistir(dil_menusu.get()))
dil_menusu.place(x=20, y=20)

entry = tk.Entry(pencere, width=60, font=("Arial", 13))
entry.place(x=160, y=20)

tk.Button(pencere, text="Ara", width=10, command=ara).place(x=700, y=17)
tk.Button(pencere, text="Temizle", width=10, command=temizle).place(x=790, y=17)

tk.Label(pencere, text="Sayfa Başlığı", font=("Arial", 12)).place(x=20, y=70)
sonuc_baslik = scrolledtext.ScrolledText(pencere, height=2, width=105, font=("Arial", 11))
sonuc_baslik.place(x=20, y=100)

tk.Label(pencere, text="Wikipedia Özeti", font=("Arial", 12)).place(x=20, y=150)
sonuc_ozet = scrolledtext.ScrolledText(pencere, height=20, width=105, font=("Arial", 11))
sonuc_ozet.place(x=20, y=180)

tk.Button(pencere, text="Kaydet (.txt)", command=kaydet_txt).place(x=780, y=530)
tk.Button(pencere, text="Tam İçeriği Göster", command=tam_icerik_goster).place(x=630, y=530)

pencere.mainloop()
