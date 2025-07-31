import sqlite3

try:
    # Veritabanı bağlantısı
    conn = sqlite3.connect("arac_kiralama.db")
    cursor = conn.cursor()

    # Kullanıcılar tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kullanıcılar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kullanıcı_adı TEXT NOT NULL,
        şifre TEXT NOT NULL
    )
    """)

    # Araçlar tablosu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS araçlar (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marka TEXT NOT NULL,
        model TEXT NOT NULL,
        yıl INTEGER NOT NULL,
        fiyat REAL NOT NULL,
        durum TEXT NOT NULL,  -- 'Kiralık' veya 'Satılık'
        yakıt_türü TEXT,
        renk TEXT,
        kilometre INTEGER,
        hasar TEXT
    )
    """)

    # Örnek kullanıcı ekle
    cursor.execute("INSERT INTO kullanıcılar (kullanıcı_adı, şifre) VALUES ('admin', '1234')")

    # Örnek araçlar ekle
    araclar = [
        ("Toyota", "Corolla", 2020, 150000, "Satılık", "Benzin", "Beyaz", 15000, "Hayır"),
        ("Honda", "Civic", 2019, 200, "Kiralık", "Dizel", "Siyah", 20000, "Evet"),
        ("Opel", "Astra", 2017, 200, "Kiralık", "Dizel", "Gri", 20000, "Evet"),
        ("BMW", "3 Serisi", 2017, 200, "Kiralık", "Dizel", "Gri", 20000, "Evet"),
        ("Ford", "Focus", 2018, 120000, "Satılık", "Benzin", "Mavi", 30000, "Hayır"),
        ("Volkswagen", "Golf", 2021, 180000, "Satılık", "Dizel", "Gri", 10000, "Hayır"),
        ("BMW", "3 Serisi", 2022, 250000, "Satılık", "Benzin", "Siyah", 5000, "Hayır"),
        ("Mercedes-Benz", "C Serisi", 2021, 300000, "Satılık", "Dizel", "Beyaz", 8000, "Hayır"),
        ("Audi", "A4", 2020, 220000, "Satılık", "Benzin", "Kırmızı", 12000, "Evet"),
        ("Renault", "Megane", 2017, 90000, "Satılık", "Dizel", "Gri", 40000, "Hayır"),
        ("Peugeot", "308", 2019, 110000, "Satılık", "Benzin", "Mavi", 25000, "Hayır"),
        ("Hyundai", "i20", 2020, 130000, "Satılık", "Benzin", "Beyaz", 18000, "Hayır"),
        ("Kia", "Rio", 2018, 100000, "Satılık", "Dizel", "Siyah", 22000, "Evet"),
        ("Fiat", "Egea", 2019, 95000, "Satılık", "Benzin", "Kırmızı", 28000, "Hayır"),
        ("Opel", "Astra", 2020, 140000, "Satılık", "Dizel", "Gri", 15000, "Hayır"),
        ("Skoda", "Octavia", 2021, 160000, "Satılık", "Benzin", "Beyaz", 10000, "Hayır"),
        ("Volvo", "S60", 2022, 280000, "Satılık", "Dizel", "Siyah", 5000, "Hayır"),
        ("Mazda", "3", 2021, 170000, "Satılık", "Benzin", "Kırmızı", 12000, "Hayır"),
        ("Nissan", "Qashqai", 2020, 150000, "Satılık", "Dizel", "Gri", 20000, "Evet"),
        ("Seat", "Leon", 2019, 120000, "Satılık", "Benzin", "Mavi", 25000, "Hayır"),
        ("Chevrolet", "Cruze", 2018, 110000, "Satılık", "Dizel", "Siyah", 30000, "Hayır"),
        ("Dacia", "Sandero", 2021, 80000, "Satılık", "Benzin", "Beyaz", 10000, "Hayır")
    ]

    # Araçları veritabanına ekle
    cursor.executemany("""
    INSERT INTO araçlar (marka, model, yıl, fiyat, durum, yakıt_türü, renk, kilometre, hasar)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, araclar)

    # Değişiklikleri kaydet ve bağlantıyı kapat
    conn.commit()
    print("Veritabanı ve tablolar başarıyla oluşturuldu! 20 araç eklendi.")

except sqlite3.Error as e:
    print(f"Veritabanı hatası: {e}")

finally:
    if conn:
        conn.close()