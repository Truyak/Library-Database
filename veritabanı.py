import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from tkcalendar import DateEntry


root = tk.Tk()
root.title("Kitap Veritabanı Uygulaması")
root.geometry('860x550+60+50')
root.config(bg='#0077b4')

acik_pencere = None
detay_pencere_acik = False

def pencere_acik_mi(pencere_tipi):
    return any(w.title() == pencere_tipi for w in root.winfo_children() if isinstance(w, tk.Toplevel))

def yeni_pencere_ac(pencere_tipi):
    global acik_pencere
    # Eğer istenilen pencere açık değilse, yeni pencereyi aç
    if not pencere_acik_mi(pencere_tipi):        
        # Pencere içeriğini oluşturmak için fonksiyonu çağır
        pencere_icerik_olustur(pencere_tipi)

    

def pencere_icerik_olustur(pencere_tipi):
    if pencere_tipi == "Kitap Ekle":
        kitap_ekle()

    elif pencere_tipi == "Tüm Kitaplar":
        kitaplari_listele()

    elif pencere_tipi == "Kitap Güncelle":
        kitap_guncelle_ekrani()

    elif pencere_tipi == "Kitap Detay":
        secili_kitabi_goster()
    elif pencere_tipi == "Ödünç Verilen Kitaplar":
        odunc_verilen_kitaplari_listele()
    elif pencere_tipi == "Ödünç Alınan Kitaplar":
        odunc_alinan_kitaplari_listele()

def pencere_kapat(pencere_tip, pencere):
    pencere.destroy()

def kitap_ekle():
    yeni_pencere = tk.Toplevel(root)
    yeni_pencere.title("Kitap Ekle")
    yeni_pencere.geometry('500x500+1000+30')
    yeni_pencere.config(bg='#0077b4')

    ad_label = tk.Label(yeni_pencere, text="Kitap Adı:", bg='#0077b4')
    ad_label.grid(row=0, column=0, pady=10)
    
    ad_entry = tk.Entry(yeni_pencere)
    ad_entry.grid(row=0, column=2,ipadx=90, ipady=2, columnspan=2, padx=20, sticky="w")
    
    yazar_label = tk.Label(yeni_pencere, text="Yazar:", bg='#0077b4')
    yazar_label.grid(row=1, column=0, pady=10)
    
    yazar_entry = tk.Entry(yeni_pencere)
    yazar_entry.grid(row=1, column=2,ipadx=90, ipady=2, columnspan=2, padx=20, sticky="w")
    
    sira_label = tk.Label(yeni_pencere, text="Sıra Numarası:", bg='#0077b4')
    sira_label.grid(row=2, column=0, pady=10)
    
    sira_entry = tk.Entry(yeni_pencere)
    sira_entry.grid(row=2, column=2,ipadx=90, ipady=2, columnspan=2, padx=20, sticky="w")
    
    raf_label = tk.Label(yeni_pencere, text="Raf Sırası:", bg='#0077b4')
    raf_label.grid(row=3, column=0, pady=10)
    
    raf_entry = tk.Entry(yeni_pencere)
    raf_entry.grid(row=3, column=2,ipadx=90, ipady=2, columnspan=2, padx=20, sticky="w")

    durum_label = tk.Label(yeni_pencere, text="Durum:", bg='#0077b4')
    durum_label.grid(row=4, column=0, pady=10)
    
    durum_var = tk.StringVar()
    durum_options = ["Ödünç Verildi", "Rafta", "Ödünç Alındı"]
    durum_var.set(durum_options[1])  # Varsayılan durumu ayarlayın
    
    durum_optionmenu = tk.OptionMenu(yeni_pencere, durum_var, *durum_options)
    durum_optionmenu.config(bg='#0077b4')
    durum_optionmenu.grid(row=4, column=2,ipadx=50, ipady=2, columnspan=2, padx=20, sticky="w")
    
    tarih_label = tk.Label(yeni_pencere, text="Tarih:", bg='#0077b4')
    tarih_label.grid(row=5, column=0, pady=10)
    
    tarih_cal = DateEntry(
                            yeni_pencere,
                            foreground='white', borderwidth=2)
    tarih_cal.grid(row=5, column=1, ipadx=50, ipady=2, columnspan=3, padx=10)
    
    odunc_kisi_label = tk.Label(yeni_pencere, text="Ödünç Alınan Veya Verilen Kişi:",font=("ariel", 8), bg='#0077b4')
    odunc_kisi_label.grid(row=6, column=0, pady=10)
    
    odunc_kisi_entry = tk.Entry(yeni_pencere)
    odunc_kisi_entry.grid(row=6, column=1, ipadx=90, ipady=2, columnspan=2, padx=20,sticky="w")

    kaydet_button = tk.Button(yeni_pencere, bg='#0077b4', text="Kaydet", command=lambda: yeni_kitabi_kaydet(ad_entry.get(), yazar_entry.get(), sira_entry.get(), raf_entry.get(), durum_var.get(), odunc_kisi_entry.get() if durum_var.get() != "Rafta" else "", tarih_cal.get_date() if durum_var.get() != "Rafta" else ""))
    kaydet_button.grid(row=7, column=0,ipadx=210, ipady=5, columnspan=3, padx=20, sticky="w")
    
        

def yeni_kitabi_kaydet(ad, yazar, sira, raf, durum, odunc_kisi="", tarih=""):
    if ad and yazar and sira and raf and durum:
        if (durum == "Ödünç Verildi" or durum == "Ödünç Alındı") and (odunc_kisi and tarih):
            kitap_ekle_veritabanina(ad, yazar, sira, raf, durum, odunc_kisi, tarih)
            messagebox.showinfo("Başarılı", "Kitap eklendi!")
        elif durum == "Rafta": 
            kitap_ekle_veritabanina(ad, yazar, sira, raf, durum)
            messagebox.showinfo("Başarılı", "Kitap eklendi!")
        else:
            messagebox.showerror("Hata", "Tüm alanları doldurun!")
    else:
        messagebox.showerror("Hata", "Tüm alanları doldurun!")

def kitap_ekle_veritabanina(ad, yazar, sira, raf, durum, odunc_kisi = None, tarih = None):
    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()
    if durum != "Rafta":
        if durum == "Ödünç Verildi":
            cursor.execute('INSERT INTO kitaplar (ad, yazar, sira, raf, durum, odunc_verilen_kisi, tarih) VALUES (?, ?, ?, ?, ?, ?, ?)', (ad, yazar, sira, raf, durum, odunc_kisi, tarih))
        else:
            cursor.execute('INSERT INTO kitaplar (ad, yazar, sira, raf, durum, tarih, odunc_alinan_kisi) VALUES (?, ?, ?, ?, ?, ?, ?)', (ad, yazar, sira, raf, durum, tarih, odunc_kisi))
    else:
        cursor.execute('INSERT INTO kitaplar (ad, yazar, sira, raf, durum) VALUES (?, ?, ?, ?, ?)', (ad, yazar, sira, raf, durum))
    
    connection.commit()
    connection.close()

def kitap_ara(event=None):
    arama_metni = ad_arama_entry.get()

    if arama_metni:        
        # Veritabanından kitapları ara ve sonuçları güncelle
        kitaplar = kitap_ara_veritabaninda(arama_metni)
        if kitaplar:
            kitap_listbox.delete(0, tk.END)
            for i, kitap in enumerate(kitaplar):
                if kitap[4] == "Ödünç Verildi":
                    bg_color = '#fe0017'
                elif kitap[4] == "Ödünç Alındı":
                    bg_color = "#01daff"
                elif i % 2 == 0:
                    bg_color = '#bcbcbc'
                else:
                    bg_color = '#ffffff'
                
                kitap_ad = f"Ad: {kitap[0]}, Yazar: {kitap[1]}"
                kitap_listbox.insert(tk.END, kitap_ad)
                kitap_listbox.itemconfig(tk.END, {'bg': bg_color})

            sonuc_label.config(text=f"{len(kitaplar)} sonuç bulundu.")
        else:
            kitap_listbox.delete(0, tk.END)
            sonuc_label.config(text="Sonuç bulunamadı.")

def auto_search(event):
    arama_metni = ad_arama_entry.get()
    if len(arama_metni) >= 1:
        kitap_ara()
    if len(arama_metni) == 0:
        kitap_listbox.delete(0, tk.END)

def kitaplari_listele():
    yeni_pencere = tk.Toplevel(root)
    yeni_pencere.title("Tüm Kitaplar")
    yeni_pencere.geometry('800x700+700+50')
    
    kitap_listbox = tk.Listbox(yeni_pencere, width=50, height=20, font=('Times new roman', 25, "italic"))
    kitap_listbox.pack(fill=tk.BOTH, expand=True)  # fill ve expand ile içeriği boyutlandırma
    kitap_listbox.config(fg='#000000')
    
    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, ad, yazar FROM kitaplar')
    kitaplar = cursor.fetchall()
    connection.close()
    
    for i, kitap in enumerate(kitaplar):
        if i % 2 == 0:
            bg_color = '#bcbcbc'
        else:
            bg_color = '#ffffff'
        
        kitap_ad = f"Ad: {kitap[1]}, Yazar: {kitap[2]}"
        kitap_listbox.insert(tk.END, kitap_ad)
        kitap_listbox.itemconfig(tk.END, {'bg': bg_color})
    toplam_kitap_label = tk.Label(yeni_pencere, text=f"Toplam {len(kitaplar)} kitap bulundu.", font=("Times new roman", 15))
    toplam_kitap_label.pack()

    kitap_listbox.bind("<Double-Button-1>", lambda event: show_kitap_detay(event, kitap_listbox))

def show_kitap_detay(event, kitap_listbox):
    selected_item = kitap_listbox.curselection()
    if selected_item:
        index = selected_item[0]
        secili_kitap = kitap_listbox.get(index)
        kitap_ad = secili_kitap.split(",")[0][4:]
        kitap_id = kitap_id_getir_veritabanindan(kitap_ad)
        
        if kitap_id is not None:
            kitap_detay_goster(kitap_id)
        else:
            messagebox.showerror("Hata", "Kitap bulunamadı.")

def kitap_ara_veritabaninda(arama_metni):
    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()
    
    arama_metni = arama_metni.lower()
            
    cursor.execute('SELECT ad, yazar, sira, raf, durum FROM kitaplar WHERE ad LIKE ? OR yazar LIKE ? ORDER BY ad',
                   ('%' + arama_metni + '%', '%' + arama_metni + '%'))
    kitaplar = cursor.fetchall()
    connection.close()
    
    return kitaplar

def odunc_verilen_kitaplari_listele():
    yeni_pencere = tk.Toplevel(root)
    yeni_pencere.title("Ödünç Verilen Kitaplar")
    yeni_pencere.geometry('500x300+950+50')

    kitap_listbox = tk.Listbox(yeni_pencere, width=80, height=20, font=('times new roman', 15), bg="#f0b1a4", exportselection=False)
    kitap_listbox.pack(fill=tk.BOTH, expand=True)

    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()

    query = 'SELECT id, ad, yazar FROM kitaplar WHERE durum = "Ödünç Verildi"'
    cursor.execute(query)
    
    kitaplar = cursor.fetchall()
    connection.close()

    for i, kitap in enumerate(kitaplar):
        if i % 2 == 0:
            bg_color = '#bcbcbc'
        else:
            bg_color = '#ffffff'
        
        kitap_ad = f"Ad: {kitap[1]}, Yazar: {kitap[2]}"
        kitap_listbox.insert(tk.END, kitap_ad)
        kitap_listbox.itemconfig(tk.END, {'bg': bg_color})

    kitap_listbox.bind("<Double-Button-1>", lambda event: show_kitap_detay(event, kitap_listbox))

def odunc_alinan_kitaplari_listele():
    yeni_pencere = tk.Toplevel(root)
    yeni_pencere.title("Ödünç Alınan Kitaplar")
    yeni_pencere.geometry('500x300+950+50')

    kitap_listbox = tk.Listbox(yeni_pencere, width=80, height=20, font=('times new roman', 15), bg="#f0b1a4", exportselection=False)
    kitap_listbox.pack(fill=tk.BOTH, expand=True)

    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()

    query = 'SELECT id, ad, yazar FROM kitaplar WHERE durum = "Ödünç Alındı"'
    cursor.execute(query)
    
    kitaplar = cursor.fetchall()
    connection.close()

    for i, kitap in enumerate(kitaplar):
        if i % 2 == 0:
            bg_color = '#bcbcbc'
        else:
            bg_color = '#ffffff'
        
        kitap_ad = f"Ad: {kitap[1]}, Yazar: {kitap[2]}"
        kitap_listbox.insert(tk.END, kitap_ad)
        kitap_listbox.itemconfig(tk.END, {'bg': bg_color})

    kitap_listbox.bind("<Double-Button-1>", lambda event: show_kitap_detay(event, kitap_listbox))

def secili_kitabi_cikar():
    secili_item = kitap_listbox.curselection()
    if secili_item:
        index = secili_item[0]
        secili_kitap = kitap_listbox.get(index)
        kitap_ad = secili_kitap.split(",")[0][4:]
        
        cevap = messagebox.askyesno("Onay", f"{kitap_ad} kitabını çıkarmak istediğinizden emin misiniz?")
        
        if cevap:
            kitap_id = kitap_cikar_veritabanindan(kitap_ad)
            if kitap_id is not None:
                kitap_listbox.delete(index)
                messagebox.showinfo("Başarılı", f"{kitap_ad} kitabı çıkarıldı!")
            else:
                messagebox.showerror("Hata", "Kitap çıkarılamadı.")
        else:
            messagebox.showinfo("Bilgi", "Kitap çıkarılmadı.")
    else:
        messagebox.showerror("Hata", "Bir kitap seçin!")

def kitap_cikar_veritabanindan(kitap_ad):
    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT id FROM kitaplar WHERE ad = ?', (kitap_ad,))
    kitap_id = cursor.fetchone()
    
    if kitap_id:
        kitap_id = kitap_id[0]
        cursor.execute('DELETE FROM kitaplar WHERE id = ?', (kitap_id,))
        connection.commit()
    
    connection.close()
    
    return kitap_id

def secili_kitabi_guncelle(kitap_id, yeni_bilgiler):
    
    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()
    tarih_bilgisi = yeni_bilgiler[6]  # Yeni tarih bilgisini alın

    if len(yeni_bilgiler) == 7 and yeni_bilgiler[4] == "Ödünç Alındı":
         cursor.execute('UPDATE kitaplar SET ad = ?, yazar = ?, sira = ?, raf = ?, durum = ?, odunc_verilen_kisi = ?, tarih = ?, odunc_alinan_kisi = ? WHERE id = ?',
                   (yeni_bilgiler[0], yeni_bilgiler[1], yeni_bilgiler[2], yeni_bilgiler[3], yeni_bilgiler[4], None, tarih_bilgisi, yeni_bilgiler[5], kitap_id))
    else:
        if yeni_bilgiler[4] == 'Rafta':  # Eğer tarih boşsa, SQL sorgusunda NULL olarak atayın
            cursor.execute('UPDATE kitaplar SET ad = ?, yazar = ?, sira = ?, raf = ?, durum = ?, odunc_verilen_kisi = ?, tarih = ?, odunc_alinan_kisi = ? WHERE id = ?',
                    (yeni_bilgiler[0], yeni_bilgiler[1], yeni_bilgiler[2], yeni_bilgiler[3], yeni_bilgiler[4], None, None, None, kitap_id))
        elif yeni_bilgiler[4] == 'Ödünç Verildi':  # Eğer tarih doluysa, yeni tarih bilgisini SQL sorgusuna ekleyin
            cursor.execute('UPDATE kitaplar SET ad = ?, yazar = ?, sira = ?, raf = ?, durum = ?, odunc_verilen_kisi = ?, tarih = ?, odunc_alinan_kisi = ? WHERE id = ?',
                    (yeni_bilgiler[0], yeni_bilgiler[1], yeni_bilgiler[2], yeni_bilgiler[3], yeni_bilgiler[4], yeni_bilgiler[5], tarih_bilgisi, None, kitap_id))

    connection.commit()
    connection.close()

    messagebox.showinfo("Başarılı", "Kitap güncellendi!")
    guncelle_pencere.destroy()

def kitap_detay_goster(kitap_id):
    global detay_pencere_acik

    if not detay_pencere_acik:
        detay_pencere_acik = True
        kitap_bilgileri = kitap_bilgilerini_getir(kitap_id)
        def pencere_kapat():
            global detay_pencere_acik
            detay_pencere_acik = False
            detay_pencere.destroy()

        detay_pencere = tk.Toplevel(root)
        detay_pencere.title("Kitap Detayı")
        detay_pencere.geometry('650x300+800+50')
        detay_pencere.config(bg='#0077b4')

        detay_label = tk.Label(detay_pencere, text=f"Kitap Adı: {kitap_bilgileri[0]}\nYazar: {kitap_bilgileri[1]}\nSıra: {kitap_bilgileri[2]}\nRaf: {kitap_bilgileri[3]}\nDurum: {kitap_bilgileri[4]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
        detay_label.pack()

        detay_pencere.protocol("WM_DELETE_WINDOW", pencere_kapat)
        if kitap_bilgileri[5] is not None and kitap_bilgileri[6] is not None:
            odunc_verilen_kisi_label = tk.Label(detay_pencere, text=f"Ödünç Verilen Kişi: {kitap_bilgileri[5]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
            odunc_verilen_kisi_label.pack(pady=(10,0))

            tarih_label = tk.Label(detay_pencere, text=f"Ödünç Verilen Tarih: {kitap_bilgileri[6]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
            tarih_label.pack()
        elif kitap_bilgileri[7] is not None and kitap_bilgileri[6] is not None:
            odunc_verilen_kisi_label = tk.Label(detay_pencere, text=f"Ödünç Alınan Kişi: {kitap_bilgileri[7]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
            odunc_verilen_kisi_label.pack(pady=(10,0))

            tarih_label = tk.Label(detay_pencere, text=f"Ödünç Alınan Tarih: {kitap_bilgileri[6]}", font=("Calibri", 20, "italic", "bold"), bg='#0077b4', fg="#000000")
            tarih_label.pack()
        else:
            pass

        
    else:
        pass

    # Ödünç verilen bilgileri kontrol et ve görüntüle       

def kitap_guncelle_ekrani():
    secili_item = kitap_listbox.curselection()
    if secili_item:
        index = secili_item[0]
        secili_kitap = kitap_listbox.get(index)
        kitap_ad = secili_kitap.split(",")[0][4:]
        kitap_id = kitap_id_getir_veritabanindan(kitap_ad)
        
        if kitap_id:
            kitap_bilgileri = kitap_bilgilerini_getir(kitap_id)
            global guncelle_pencere
            guncelle_pencere = tk.Toplevel(root)
            guncelle_pencere.title("Kitap Güncelle")
            guncelle_pencere.geometry('500x400+800+50')
            guncelle_pencere.config(bg='#0077b4')
            
            entry_list = []  # Entry alanlarını saklayacağımız liste
            
            for i, (label_text, bilgi) in enumerate(zip(["Kitap Adı:", "Yazar:", "Sıra Numarası:", "Raf Sırası:"], kitap_bilgileri[:4])):
                label = tk.Label(guncelle_pencere, text=label_text, bg='#0077b4')
                label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
                entry = tk.Entry(guncelle_pencere, bg='#0077b4')
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
                entry.insert(0, bilgi)  # Eski bilgileri entry'lere yerleştir
                entry_list.append(entry)  # Entry'yi listeye ekle
            
            odunc_bilgisi_label = tk.Label(guncelle_pencere, text="Durum:", bg='#0077b4')
            odunc_bilgisi_label.grid(row=i+1, column=0, padx=10, pady=5, sticky="e")
            
            odunc_var = tk.StringVar()
            odunc_options = ["Ödünç Verildi", "Rafta", "Ödünç Alındı"]
            odunc_var.set(kitap_bilgileri[4])  # Varsayılan durumu ayarlayın
    
            odunc_optionmenu = tk.OptionMenu(guncelle_pencere, odunc_var, *odunc_options, command=lambda value: update_odunc_kisi(value, odunc_kisi_entry, tarih_cal))
            odunc_optionmenu.config(bg='#0077b4')
            odunc_optionmenu.grid(row=i+1, column=1, padx=10, pady=5, sticky="w")
            
            tarih_label = tk.Label(guncelle_pencere, text="Tarih:", bg='#0077b4')
            tarih_label.grid(row=i+2, column=0, padx=10, pady=5, sticky="e")
            
            tarih_cal = DateEntry(
                guncelle_pencere, width=12, background='darkblue',
                foreground='white', borderwidth=2)
            tarih_cal.grid(row=i+2, column=1, padx=10, pady=5, sticky="w")
            
            odunc_kisi_label = tk.Label(guncelle_pencere, text="Ödünç Alınan Veya Verilen Kişi:", bg='#0077b4')
            odunc_kisi_label.grid(row=i+3, column=0, padx=10, pady=5, sticky="e")
            
            odunc_kisi_entry = tk.Entry(guncelle_pencere, bg='#0077b4')
            odunc_kisi_entry.grid(row=i+3, column=1, padx=10, pady=5, sticky="w")            
            
            if kitap_bilgileri[4] == "Ödünç Verildi" or kitap_bilgileri[4] == "Ödünç Alındı":
                if kitap_bilgileri[5]:
                    odunc_kisi_entry.insert(0, kitap_bilgileri[5])  # Ödünç verilen kişi
                elif kitap_bilgileri[7]:
                    odunc_kisi_entry.insert(0, kitap_bilgileri[7])  # Ödünç Alınan kişi
                if kitap_bilgileri[6]:
                    tarih_str = kitap_bilgileri[6]  # Ödünç verilen tarih metin değeri
                    try:
                        tarih_datetime = datetime.strptime(tarih_str, "%Y-%m-%d")  # Metni datetime türüne dönüştür
                        tarih_cal.set_date(tarih_datetime.date())  # Tarihi DateEntry bileşenine ata
                    except ValueError:
                        print("Geçersiz tarih formatı:", tarih_str)  # Ödünç verilen tarih
                    
            delete_tarih_button = tk.Button(
                guncelle_pencere, text="Tarihi Sil",
                command=lambda: delete_odunc_tarih(tarih_cal))
            delete_tarih_button.grid(row=i+2, column=2, padx=10, pady=5, sticky="w")
            
            guncelle_button = tk.Button(guncelle_pencere, bg='#0077b4', text="Güncelle", command=lambda: secili_kitabi_guncelle(kitap_id, [entry.get() for entry in entry_list] + [odunc_var.get(), odunc_kisi_entry.get(), tarih_cal.get_date()]))
            guncelle_button.grid(row=i+5, columnspan=2, pady=10)
        else:
            messagebox.showerror("Hata", "Kitap bulunamadı.")
    else:
        messagebox.showerror("Hata", "Bir kitap seçin!") 

def update_odunc_kisi(value, odunc_kisi_entry, tarih_cal):
    if value == "Rafta":
        odunc_kisi_entry.delete(0, tk.END)
        tarih_cal.set_date(None)  # Tarihi sıfırla


def delete_odunc_tarih(tarih_cal):
    tarih_cal._set_text("")


def kitap_id_getir_veritabanindan(kitap_ad):
    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT id FROM kitaplar WHERE ad = ?', (kitap_ad,))
    kitap_id = cursor.fetchone()
    
    connection.close()
    
    if kitap_id:
        return kitap_id[0]
    else:
        return None
    
def secili_kitabi_goster():
    secili_item = kitap_listbox.curselection()
    if secili_item:
        index = secili_item[0]
        secili_kitap = kitap_listbox.get(index)
        kitap_ad = secili_kitap.split(",")[0][4:]

        kitap_id = kitap_id_getir_veritabanindan(kitap_ad)
        if kitap_id is not None:
            kitap_detay_goster(kitap_id)
        else:
            messagebox.showerror("Hata", "Kitap bulunamadı.")
    else:
        messagebox.showerror("Hata", "Bir kitap seçin!")
    
def kitap_bilgilerini_getir(kitap_id):
    connection = sqlite3.connect('kitaplar.db')
    cursor = connection.cursor()
    cursor.execute('SELECT ad, yazar, sira, raf, durum, odunc_verilen_kisi, tarih, odunc_alinan_kisi FROM kitaplar WHERE id = ?', (kitap_id,))
    kitap_bilgileri = cursor.fetchone()
    connection.close()
    return kitap_bilgileri

if __name__ == "__main__":

    ekle_button = tk.Button(root, text="Kitap Ekle", command=lambda: yeni_pencere_ac("Kitap Ekle"), bg='#123fff', fg='#ffffff', relief=tk.RAISED)
    ekle_button.grid(row=0, column=2, padx=(20, 10), pady=10, sticky='e')

    kitaplık_label = tk.Label(root, text="ÖZCANLAR KİTAPLIĞI", bg='#0077b4', font=(10))
    kitaplık_label.grid(row=0, column=1,columnspan=2, padx=(100, 10), pady=10, sticky='w')

    cikar_button = tk.Button(root, text="Seçili Kitabı Çıkar", command=secili_kitabi_cikar, bg='#ee0000', fg='#ffffff', relief=tk.RAISED)
    cikar_button.grid(row=0, column=0, padx=(10, 20), pady=(10,0), sticky='w')

    ad_arama_label = tk.Label(root, text="Aranacak Kitap Adı:", bg='#0077b4', fg='#ffffff', font=('times new roman', 13, 'bold'))
    ad_arama_label.grid(row=1, column=0, padx=8, pady=(0, 5), sticky='w')

    ad_arama_entry = tk.Entry(root)
    ad_arama_entry.config(bg='#ffffff', relief=tk.SUNKEN , fg='#000000')
    ad_arama_entry.grid(row=1, column=1,columnspan=2, padx=10, pady=(0, 10),ipadx=(250),ipady=(4), sticky='w')

    # ara_button = tk.Button(root, text="Kitap veya Yazar ile Ara", command=kitap_ara, font=('calibri', 13), bg='#fff111', relief=tk.RAISED)
    # ara_button.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10), sticky='we')

    ad_arama_entry.bind("<KeyRelease>", auto_search)

    kitap_listbox = tk.Listbox(root, width=80, height=9, font=('times new roman', 15), bg="#f0b1a4")
    kitap_listbox.grid(row=3, column=0, columnspan=3, padx=10, ipadx=20)

    detay_goster_button = tk.Button(root, text="Kitap Detayı Göster", command=lambda: yeni_pencere_ac("Kitap Detay"), bg='#fff111')
    detay_goster_button.grid(row=4, column=2, padx=(10, 10), pady=(10, 0),ipady=10, sticky='e')

    sonuc_label = tk.Label(root, text="", bg='#0077b4', fg='#ffffff', font=('times new roman', 12, 'bold'))
    sonuc_label.grid(row=4, column=1, padx=(100,80), pady=5, sticky='we')

    kitap_guncelle_button = tk.Button(root, text="Seçili Kitabı Güncelle", command=lambda: yeni_pencere_ac("Kitap Güncelle"), bg='#fff111', relief="raised")
    kitap_guncelle_button.grid(row=4, column=0, padx=(10, 10), pady=(10, 0),ipady=10, sticky='w')

    odunc_listele_button = tk.Button(root, text="Ödünç Verilen Kitapları Listele", relief="raised", command=lambda: yeni_pencere_ac("Ödünç Verilen Kitaplar"), bg='#fff111')
    odunc_listele_button.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='we')

    odunc_alinan_listele_button = tk.Button(root, text="Ödünç Alınan Kitapları Listele", relief="raised", command=lambda: yeni_pencere_ac("Ödünç Alınan Kitaplar"), bg='#fff111')
    odunc_alinan_listele_button.grid(row=6, column=0, columnspan=3, padx=10, pady=(10,0), sticky='we')

    listele_button = tk.Button(root, text="Kitapları Listele", relief="raised", command=lambda: yeni_pencere_ac("Tüm Kitaplar"), bg='#fff111')
    listele_button.grid(row=7, column=0, columnspan=3,ipady=5, padx=10, pady=20, sticky='we')


    root.mainloop()