import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QLabel, QDialog, QFormLayout, QLineEdit, QListWidget,
    QComboBox, QSpinBox, QCheckBox, QTabWidget, QGroupBox, QTextEdit
)
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtGui import QTextDocument
from datetime import datetime
import os
from PyQt5.QtWidgets import QDateEdit, QCalendarWidget, QHBoxLayout
from PyQt5.QtCore import QDate

# CSS Stilleri
STYLE_SHEET = """
    QWidget {
        background-color: #f0f0f0;
        font-family: Arial;
        font-size: 14px;
    }
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #45a049;
    }
    QLineEdit, QTextEdit, QComboBox, QSpinBox {
        padding: 5px;
        border: 1px solid #ccc;
        border-radius: 3px;
    }
    QListWidget {
        background-color: white;
        border: 1px solid #ccc;
        border-radius: 3px;
    }
    QLabel {
        font-weight: bold;
    }
    QGroupBox {
        border: 1px solid #ccc;
        border-radius: 5px;
        margin-top: 10px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px;
    }
"""

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Yap")
        self.setGeometry(200, 200, 300, 200)
        self.setStyleSheet(STYLE_SHEET)

        # Kullanıcı adı ve şifre için form layout oluştur
        layout = QFormLayout()
        self.kullanıcı_adı = QLineEdit()
        self.şifre = QLineEdit()
        self.şifre.setEchoMode(QLineEdit.Password)
        self.giriş_buton = QPushButton("Giriş Yap")
        self.kayıt_buton = QPushButton("Kayıt Ol")

        layout.addRow("Kullanıcı Adı:", self.kullanıcı_adı)
        layout.addRow("Şifre:", self.şifre)
        layout.addRow(self.giriş_buton)
        layout.addRow(self.kayıt_buton)

        self.setLayout(layout)
        self.giriş_buton.clicked.connect(self.giris_yap)
        self.kayıt_buton.clicked.connect(self.kayit_ac)

        # Veritabanı bağlantısını kontrol et
        self.veritabani_baslat()

    def veritabani_baslat(self):
        conn = None
        try:
            conn = sqlite3.connect("arac_kiralama.db")
            cursor = conn.cursor()
            
            # Kullanıcılar tablosunu oluştur (eğer yoksa)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS kullanıcılar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullanıcı_adı TEXT UNIQUE NOT NULL,
                şifre TEXT NOT NULL
            )
            """)
            conn.commit()
            
            # Test için bir kullanıcı ekleyelim (eğer yoksa)
            cursor.execute("SELECT * FROM kullanıcılar WHERE kullanıcı_adı='admin'")
            if not cursor.fetchone():
                cursor.execute("INSERT INTO kullanıcılar (kullanıcı_adı, şifre) VALUES (?, ?)", 
                             ("admin", "123456"))
                conn.commit()
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanı hatası: {str(e)}")
        finally:
            if conn:
                conn.close()

    def giris_yap(self):
        kullanıcı_adı = self.kullanıcı_adı.text().strip()
        şifre = self.şifre.text().strip()

        if not kullanıcı_adı or not şifre:
            QMessageBox.warning(self, "Hata", "Lütfen kullanıcı adı ve şifre girin!")
            return

        conn = None
        try:
            conn = sqlite3.connect("arac_kiralama.db")
            cursor = conn.cursor()
            
            # Kullanıcıyı kontrol et
            cursor.execute("SELECT * FROM kullanıcılar WHERE kullanıcı_adı=? AND şifre=?", 
                         (kullanıcı_adı, şifre))
            kullanıcı = cursor.fetchone()
            
            if kullanıcı:
                QMessageBox.information(self, "Başarılı", "Giriş başarılı!")
                self.accept()  # Giriş başarılı, ana pencereye geç
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz kullanıcı adı veya şifre!")
                
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Veritabanı Hatası", f"Veritabanı hatası: {str(e)}")
        finally:
            if conn:
                conn.close()

    def kayit_ac(self):
        self.register_window = RegisterWindow()
        self.register_window.exec_()
class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(200, 200, 300, 200)
        self.setStyleSheet(STYLE_SHEET)

        self.kullanıcı_adı = QLineEdit()
        self.şifre = QLineEdit()
        self.şifre.setEchoMode(QLineEdit.Password)
        self.şifre_tekrar = QLineEdit()
        self.şifre_tekrar.setEchoMode(QLineEdit.Password)
        self.kayıt_buton = QPushButton("Kayıt Ol")

        layout = QFormLayout()
        layout.addRow("Kullanıcı Adı:", self.kullanıcı_adı)
        layout.addRow("Şifre:", self.şifre)
        layout.addRow("Şifre Tekrar:", self.şifre_tekrar)
        layout.addRow(self.kayıt_buton)

        self.setLayout(layout)
        self.kayıt_buton.clicked.connect(self.kayit_ol)

    def kayit_ol(self):
        kullanıcı_adı = self.kullanıcı_adı.text()
        şifre = self.şifre.text()
        şifre_tekrar = self.şifre_tekrar.text()

        if not kullanıcı_adı or not şifre:
            QMessageBox.warning(self, "Hata", "Kullanıcı adı ve şifre zorunludur!")
            return

        if şifre != şifre_tekrar:
            QMessageBox.warning(self, "Hata", "Şifreler uyuşmuyor!")
            return

        conn = sqlite3.connect("arac_kiralama.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("INSERT INTO kullanıcılar (kullanıcı_adı, şifre) VALUES (?, ?)", 
                         (kullanıcı_adı, şifre))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu kullanıcı adı zaten alınmış!")
        finally:
            conn.close()

class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Araç Kiralama ve Satın Alma Sistemi")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(STYLE_SHEET)  # CSS stilini uygula

        # Butonlar
        self.satin_al_buton = QPushButton("Araç Satın Alım", self)
        self.kiralama_buton = QPushButton("Araç Kiralama", self)
        self.randevu_buton = QPushButton("Kiralanmış Araçlar ve Randevu Oluşturma", self)
        self.biz_kimiz_buton = QPushButton("Biz Kimiz?", self)
        self.cikis_buton = QPushButton("Çıkış", self)

        # Butonlara tıklama olayları
        self.satin_al_buton.clicked.connect(self.satin_al_ac)
        self.kiralama_buton.clicked.connect(self.kiralama_ac)
        self.randevu_buton.clicked.connect(self.randevu_ac)
        self.biz_kimiz_buton.clicked.connect(self.biz_kimiz_ac)
        self.cikis_buton.clicked.connect(self.close)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.satin_al_buton)
        vbox.addWidget(self.kiralama_buton)
        vbox.addWidget(self.randevu_buton)
        vbox.addWidget(self.biz_kimiz_buton)
        vbox.addWidget(self.cikis_buton)

        self.setLayout(vbox)

    def satin_al_ac(self):
        self.satin_al_pencere = SatinAlPencere()
        self.satin_al_pencere.show()

    def kiralama_ac(self):
        self.kiralama_pencere = KiralamaPencere()
        self.kiralama_pencere.show()

    def randevu_ac(self):
        self.randevu_pencere = RandevuPencere()
        self.randevu_pencere.show()

    def biz_kimiz_ac(self):
        self.biz_kimiz_pencere = BizKimizPencere()
        self.biz_kimiz_pencere.show()

class BizKimizPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Biz Kimiz?")
        self.setGeometry(150, 150, 600, 400)
        self.setStyleSheet(STYLE_SHEET)  # CSS stilini uygula

        # Tab widget oluştur
        tab_widget = QTabWidget(self)

        # 1. Tab: Dükkanlarımız
        dukkanlar_tab = QWidget()
        dukkanlar_layout = QVBoxLayout()

        dukkanlar_group = QGroupBox("Dükkanlarımız ve Adreslerimiz")
        dukkanlar_text = QTextEdit()
        dukkanlar_text.setPlainText(
            "1. Şube: İstanbul, Beşiktaş\n"
            "2. Şube: Ankara, Çankaya\n"
            "3. Şube: İzmir, Karşıyaka\n"
            "4. Şube: Bursa, Nilüfer\n"
            "5. Şube: Antalya, Konyaaltı"
        )
        dukkanlar_text.setReadOnly(True)

        dukkanlar_layout.addWidget(dukkanlar_text)
        dukkanlar_group.setLayout(dukkanlar_layout)
        dukkanlar_tab.setLayout(QVBoxLayout())
        dukkanlar_tab.layout().addWidget(dukkanlar_group)

        # 2. Tab: Çalışanlarımız
        calisanlar_tab = QWidget()
        calisanlar_layout = QVBoxLayout()

        calisanlar_group = QGroupBox("Çalışanlarımız ve İletişim Bilgileri")
        calisanlar_text = QTextEdit()
        calisanlar_text.setPlainText(
            "1. Ahmet Yılmaz - ahmet@arackiralama.com - 555 123 45 67\n"
            "2. Ayşe Demir - ayse@arackiralama.com - 555 234 56 78\n"
            "3. Mehmet Kaya - mehmet@arackiralama.com - 555 345 67 89\n"
            "4. Zeynep Şahin - zeynep@arackiralama.com - 555 456 78 90\n"
            "5. Ali Can - ali@arackiralama.com - 555 567 89 01"
        )
        calisanlar_text.setReadOnly(True)

        calisanlar_layout.addWidget(calisanlar_text)
        calisanlar_group.setLayout(calisanlar_layout)
        calisanlar_tab.setLayout(QVBoxLayout())
        calisanlar_tab.layout().addWidget(calisanlar_group)

        # 3. Tab: Hakkımızda
        hakkimizda_tab = QWidget()
        hakkimizda_layout = QVBoxLayout()

        hakkimizda_group = QGroupBox("Hakkımızda")
        hakkimizda_text = QTextEdit()
        hakkimizda_text.setPlainText(
            "Biz Kimiz?\n"
            "Araç kiralama ve satış sektöründe 10 yılı aşkın deneyimimizle, müşterilerimize en kaliteli hizmeti sunuyoruz.\n\n"
            "Neden Bizi Tercih Etmelisiniz?\n"
            "- Geniş araç filosu\n"
            "- Uygun fiyatlar\n"
            "- Güvenilir ve deneyimli ekip\n"
            "- 7/24 müşteri desteği\n\n"
            "Misyonumuz:\n"
            "Müşteri memnuniyetini ön planda tutarak, sektörde lider olmak."
        )
        hakkimizda_text.setReadOnly(True)

        hakkimizda_layout.addWidget(hakkimizda_text)
        hakkimizda_group.setLayout(hakkimizda_layout)
        hakkimizda_tab.setLayout(QVBoxLayout())
        hakkimizda_tab.layout().addWidget(hakkimizda_group)

        # Tabları ekle
        tab_widget.addTab(dukkanlar_tab, "Dükkanlarımız")
        tab_widget.addTab(calisanlar_tab, "Çalışanlarımız")
        tab_widget.addTab(hakkimizda_tab, "Hakkımızda")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(tab_widget)
        self.setLayout(layout)

class OdemePenceresi(QDialog):
    def __init__(self, arac_bilgisi, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ödeme İşlemleri")
        self.setGeometry(200, 200, 400, 400)
        self.setStyleSheet(STYLE_SHEET)
        self.arac_bilgisi = arac_bilgisi
        
        # Ödeme bilgileri formu
        layout = QFormLayout()
        
        self.kart_no = QLineEdit()
        self.kart_no.setPlaceholderText("1234 5678 9012 3456")
        self.kart_sahibi = QLineEdit()
        self.son_kullanim = QLineEdit()
        self.son_kullanim.setPlaceholderText("AA/YY")
        self.cvv = QLineEdit()
        self.cvv.setPlaceholderText("123")
        self.cvv.setEchoMode(QLineEdit.Password)
        self.email = QLineEdit()
        self.email.setPlaceholderText("fatura@ornek.com")
        
        self.odeme_yap_buton = QPushButton("Ödeme Yap")
        self.odeme_yap_buton.clicked.connect(self.odeme_yap)
        
        layout.addRow(QLabel("Araç Bilgisi:"))
        layout.addRow(QLabel(arac_bilgisi))
        layout.addRow(QLabel("Kredi Kartı No:"), self.kart_no)
        layout.addRow(QLabel("Kart Sahibi:"), self.kart_sahibi)
        layout.addRow(QLabel("Son Kullanım Tarihi:"), self.son_kullanim)
        layout.addRow(QLabel("CVV:"), self.cvv)
        layout.addRow(QLabel("Fatura Email:"), self.email)
        layout.addRow(self.odeme_yap_buton)
        
        self.setLayout(layout)
    
    def odeme_yap(self):
        # Basit validasyonlar
        if (not self.kart_no.text() or not self.kart_sahibi.text() or 
            not self.son_kullanim.text() or not self.cvv.text() or 
            not self.email.text()):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return
        
        if len(self.cvv.text()) != 3 or not self.cvv.text().isdigit():
            QMessageBox.warning(self, "Hata", "Geçersiz CVV numarası!")
            return
        
        # Ödeme başarılı mesajı
        QMessageBox.information(self, "Başarılı", "Ödeme başarıyla tamamlandı!")
        
        # PDF fatura oluştur
        self.fatura_olustur()
        self.close()
    
    def fatura_olustur(self):
        # Fatura içeriği
        fatura_icerik = f"""
        <h1 style='text-align:center;'>ARAÇ KİRALAMA FATURASI</h1>
        <hr>
        <p><strong>Tarih:</strong> {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
        <p><strong>Fatura No:</strong> {datetime.now().strftime("%Y%m%d%H%M")}</p>
        <hr>
        <h3>Kiralanan Araç Bilgisi:</h3>
        <p>{self.arac_bilgisi.replace('\n', '<br>')}</p>
        <hr>
        <h3>Ödeme Bilgileri:</h3>
        <p><strong>Kart Sahibi:</strong> {self.kart_sahibi.text()}</p>
        <p><strong>Kart No:</strong> **** **** **** {self.kart_no.text()[-4:]}</p>
        <p><strong>Email:</strong> {self.email.text()}</p>
        <hr>
        <p style='text-align:right;'><strong>Toplam Tutar:</strong> {self.arac_bilgisi.split('TL')[0].split('-')[-1].strip()} TL</p>
        <hr>
        <p style='text-align:center;'>Teşekkür ederiz!</p>
        """
        
        # PDF oluştur
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        
        # Masaüstüne kaydet
        desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        pdf_path = os.path.join(desktop_path, f"Fatura_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        printer.setOutputFileName(pdf_path)
        
        doc = QTextDocument()
        doc.setHtml(fatura_icerik)
        doc.print_(printer)
        
        QMessageBox.information(self, "Başarılı", f"Fatura oluşturuldu:\n{pdf_path}")


class SatinAlPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Araç Satın Alım")
        self.setGeometry(150, 150, 800, 600)
        self.setStyleSheet(STYLE_SHEET)  # CSS stilini uygula

        # Filtreleme bölümü
        self.filtreleme_buton = QPushButton("Filtrele", self)
        self.filtreleme_buton.clicked.connect(self.filtreleme_ac)

        # Yeni araç ekleme butonu
        self.yeni_arac_buton = QPushButton("Yeni Araç Ekle", self)
        self.yeni_arac_buton.clicked.connect(self.yeni_arac_ac)

        # Araç listesi
        self.arac_listesi = QListWidget(self)
        self.aracları_yükle()

        # Buton
        self.satin_al_buton = QPushButton("Satın Al", self)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.filtreleme_buton)
        vbox.addWidget(self.yeni_arac_buton)
        vbox.addWidget(QLabel("Satılık Araçlar:"))
        vbox.addWidget(self.arac_listesi)
        vbox.addWidget(self.satin_al_buton)

        self.setLayout(vbox)
        self.satin_al_buton.clicked.connect(self.satin_al)

    def aracları_yükle(self, filtre=None):
        conn = sqlite3.connect("arac_kiralama.db")
        cursor = conn.cursor()

        sorgu = "SELECT * FROM araçlar WHERE durum = 'Satılık'"
        if filtre:
            sorgu += f" AND {filtre}"

        cursor.execute(sorgu)
        araçlar = cursor.fetchall()
        conn.close()

        self.arac_listesi.clear()
        for araç in araçlar:
            arac_bilgisi = (
                f"{araç[1]} {araç[2]} ({araç[3]}) - {araç[4]} TL\n"
                f"Yakıt Türü: {araç[6]}, Renk: {araç[7]}, Kilometre: {araç[8]}, Hasar: {araç[9]}"
            )
            self.arac_listesi.addItem(arac_bilgisi)

    def satin_al(self):
        secili_arac = self.arac_listesi.currentItem()
        if secili_arac:
            # Ödeme penceresini aç
            self.odeme_penceresi = OdemePenceresi(secili_arac.text())
            self.odeme_penceresi.exec_()
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir araç seçin!")

    def filtreleme_ac(self):
        self.filtreleme_pencere = FiltrelemePencere(self)
        self.filtreleme_pencere.show()

    def yeni_arac_ac(self):
        self.yeni_arac_pencere = YeniAracPencere(self)
        self.yeni_arac_pencere.show()

class YeniAracPencere(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Araç Ekle")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet(STYLE_SHEET)  # CSS stilini uygula

        # Form elemanları
        self.marka_input = QLineEdit(self)
        self.model_input = QLineEdit(self)
        self.yil_input = QSpinBox(self)
        self.yil_input.setRange(1900, 2023)
        self.fiyat_input = QLineEdit(self)
        self.yakit_combo = QComboBox(self)
        self.yakit_combo.addItems(["Benzin", "Dizel", "Elektrik", "Hibrit"])
        self.renk_input = QLineEdit(self)
        self.kilometre_input = QLineEdit(self)
        self.hasar_combo = QComboBox(self)
        self.hasar_combo.addItems(["Hayır", "Evet"])

        # Kaydet butonu
        self.kaydet_buton = QPushButton("Kaydet", self)
        self.kaydet_buton.clicked.connect(self.kaydet)

        # Layout
        form_layout = QFormLayout()
        form_layout.addRow("Marka:", self.marka_input)
        form_layout.addRow("Model:", self.model_input)
        form_layout.addRow("Yıl:", self.yil_input)
        form_layout.addRow("Fiyat:", self.fiyat_input)
        form_layout.addRow("Yakıt Türü:", self.yakit_combo)
        form_layout.addRow("Renk:", self.renk_input)
        form_layout.addRow("Kilometre:", self.kilometre_input)
        form_layout.addRow("Hasar Durumu:", self.hasar_combo)
        form_layout.addRow(self.kaydet_buton)

        self.setLayout(form_layout)

    def kaydet(self):
        marka = self.marka_input.text()
        model = self.model_input.text()
        yil = self.yil_input.value()
        fiyat = self.fiyat_input.text()
        yakit = self.yakit_combo.currentText()
        renk = self.renk_input.text()
        kilometre = self.kilometre_input.text()
        hasar = self.hasar_combo.currentText()

        if not marka or not model or not fiyat or not kilometre:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            fiyat = float(fiyat)
            kilometre = int(kilometre)
        except ValueError:
            QMessageBox.warning(self, "Hata", "Fiyat ve kilometre sayısal değerler olmalıdır!")
            return

        conn = sqlite3.connect("arac_kiralama.db")
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO araçlar (marka, model, yıl, fiyat, durum, yakıt_türü, renk, kilometre, hasar)
        VALUES (?, ?, ?, ?, 'Satılık', ?, ?, ?, ?)
        """, (marka, model, yil, fiyat, yakit, renk, kilometre, hasar))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Başarılı", "Yeni araç başarıyla eklendi!")
        self.parent().aracları_yükle()
        self.close()



class FiltrelemePencere(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Filtreleme")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet(STYLE_SHEET)  # CSS stilini uygula

        # Filtreleme kriterleri
        self.marka_combo = QComboBox(self)
        self.marka_combo.addItem("Tüm Markalar")
        self.marka_combo.addItems(["Toyota", "Honda", "Ford", "Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Renault", "Peugeot", "Hyundai", "Kia", "Fiat", "Opel", "Skoda", "Volvo", "Mazda", "Nissan", "Seat", "Chevrolet", "Dacia"])

        self.yakit_combo = QComboBox(self)
        self.yakit_combo.addItem("Tüm Yakıt Türleri")
        self.yakit_combo.addItems(["Benzin", "Dizel", "Elektrik", "Hibrit"])

        self.renk_combo = QComboBox(self)
        self.renk_combo.addItem("Tüm Renkler")
        self.renk_combo.addItems(["Beyaz", "Siyah", "Gri", "Mavi", "Kırmızı"])

        self.kilometre_min = QSpinBox(self)
        self.kilometre_min.setRange(0, 500000)
        self.kilometre_min.setValue(0)

        self.kilometre_max = QSpinBox(self)
        self.kilometre_max.setRange(0, 500000)
        self.kilometre_max.setValue(500000)

        self.hasar_check = QCheckBox("Hasarsız Araçlar", self)

        self.filtrele_buton = QPushButton("Filtrele", self)
        self.filtrele_buton.clicked.connect(self.filtrele)

        # Layout
        form_layout = QFormLayout()
        form_layout.addRow("Marka:", self.marka_combo)
        form_layout.addRow("Yakıt Türü:", self.yakit_combo)
        form_layout.addRow("Renk:", self.renk_combo)
        form_layout.addRow("Kilometre (Min):", self.kilometre_min)
        form_layout.addRow("Kilometre (Max):", self.kilometre_max)
        form_layout.addRow(self.hasar_check)
        form_layout.addRow(self.filtrele_buton)

        self.setLayout(form_layout)

    def filtrele(self):
        filtre = []
        if self.marka_combo.currentText() != "Tüm Markalar":
            filtre.append(f"marka = '{self.marka_combo.currentText()}'")
        if self.yakit_combo.currentText() != "Tüm Yakıt Türleri":
            filtre.append(f"yakıt_türü = '{self.yakit_combo.currentText()}'")
        if self.renk_combo.currentText() != "Tüm Renkler":
            filtre.append(f"renk = '{self.renk_combo.currentText()}'")
        if self.kilometre_min.value() > 0 or self.kilometre_max.value() < 500000:
            filtre.append(f"kilometre BETWEEN {self.kilometre_min.value()} AND {self.kilometre_max.value()}")
        if self.hasar_check.isChecked():
            filtre.append("hasar = 'Hayır'")

        filtre_sorgu = " AND ".join(filtre) if filtre else None
        self.parent().aracları_yükle(filtre_sorgu)
        self.close()

class KiralamaPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Araç Kiralama")
        self.setGeometry(150, 150, 600, 500)  # Yüksekliği artırdık
        self.setStyleSheet(STYLE_SHEET)

        # Araç listesi
        self.arac_listesi = QListWidget(self)
        self.aracları_yükle()

        # Tarih seçimi
        tarih_group = QGroupBox("Kiralama Tarihleri")
        tarih_layout = QFormLayout()
        
        self.baslangic_tarihi = QDateEdit(self)
        self.baslangic_tarihi.setDate(QDate.currentDate())
        self.baslangic_tarihi.setCalendarPopup(True)
        
        self.bitis_tarihi = QDateEdit(self)
        self.bitis_tarihi.setDate(QDate.currentDate().addDays(1))
        self.bitis_tarihi.setCalendarPopup(True)
        
        tarih_layout.addRow("Başlangıç Tarihi:", self.baslangic_tarihi)
        tarih_layout.addRow("Bitiş Tarihi:", self.bitis_tarihi)
        tarih_group.setLayout(tarih_layout)

        # Buton
        self.kirala_buton = QPushButton("Kirala", self)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Kiralık Araçlar:"))
        vbox.addWidget(self.arac_listesi)
        vbox.addWidget(tarih_group)
        vbox.addWidget(self.kirala_buton)

        self.setLayout(vbox)
        self.kirala_buton.clicked.connect(self.kirala)

    def aracları_yükle(self):
        conn = sqlite3.connect("arac_kiralama.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM araçlar WHERE durum = 'Kiralık'")
        araçlar = cursor.fetchall()
        conn.close()

        self.arac_listesi.clear()
        for araç in araçlar:
            arac_bilgisi = (
                f"{araç[1]} {araç[2]} ({araç[3]}) - {araç[4]} TL/gün\n"
                f"Yakıt Türü: {araç[6]}, Renk: {araç[7]}, Kilometre: {araç[8]}, Hasar: {araç[9]}"
            )
            self.arac_listesi.addItem(arac_bilgisi)

    def kirala(self):
        secili_arac = self.arac_listesi.currentItem()
        if not secili_arac:
            QMessageBox.warning(self, "Hata", "Lütfen bir araç seçin!")
            return
            
        baslangic = self.baslangic_tarihi.date()
        bitis = self.bitis_tarihi.date()
        
        if baslangic > bitis:
            QMessageBox.warning(self, "Hata", "Başlangıç tarihi bitiş tarihinden sonra olamaz!")
            return
            
        gun_sayisi = baslangic.daysTo(bitis)
        if gun_sayisi < 1:
            QMessageBox.warning(self, "Hata", "Minimum kiralama süresi 1 gündür!")
            return
            
        arac_bilgisi = f"{secili_arac.text()}\nKiralama Tarihleri: {baslangic.toString('dd.MM.yyyy')} - {bitis.toString('dd.MM.yyyy')}\nToplam Gün: {gun_sayisi}"
        
        # Ödeme penceresini aç
        self.odeme_penceresi = OdemePenceresi(arac_bilgisi)
        self.odeme_penceresi.exec_()




class RandevuPencere(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Kiralanmış Araçlar ve Randevu Oluşturma")
        self.setGeometry(150, 150, 600, 500)  # Yüksekliği artırdık
        self.setStyleSheet(STYLE_SHEET)

        # Kiralanmış araçlar listesi
        self.arac_listesi = QListWidget(self)
        self.aracları_yükle()

        # Randevu tarih seçimi
        randevu_group = QGroupBox("Randevu Bilgileri")
        randevu_layout = QFormLayout()
        
        self.randevu_tarihi = QDateEdit(self)
        self.randevu_tarihi.setCalendarPopup(True)
        
        randevu_layout.addRow("Randevu Tarihi:", self.randevu_tarihi)
        randevu_group.setLayout(randevu_layout)

        # Randevu oluşturma butonu
        self.randevu_buton = QPushButton("Randevu Oluştur", self)

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Kiralanmış Araçlar:"))
        vbox.addWidget(self.arac_listesi)
        vbox.addWidget(randevu_group)
        vbox.addWidget(self.randevu_buton)

        self.setLayout(vbox)
        self.randevu_buton.clicked.connect(self.randevu_olustur)

    def aracları_yükle(self):
        # Örnek kiralanmış araçlar (gerçek uygulamada veritabanından çekilir)
        self.arac_listesi.clear()
        self.arac_listesi.addItem("Toyota Corolla - 3 gün kaldı")  # Toyota için 6'sına kadar müsait
        self.arac_listesi.addItem("Honda Civic - 5 gün kaldı")      # Honda için 8'ine kadar müsait

    def randevu_olustur(self):
        secili_arac = self.arac_listesi.currentItem()
        if not secili_arac:
            QMessageBox.warning(self, "Hata", "Lütfen bir araç seçin!")
            return
            
        # Aracın yanında yazan gün sayısını alıyoruz (örneğin, "3 gün kaldı" kısmından 3'ü çekiyoruz)
        arac_metni = secili_arac.text()
        gun_sayisi = int(arac_metni.split(" ")[-3])  # '3 gün kaldı' kısmındaki 3 sayısını alıyoruz.
        
        # Randevu tarihi, bugünden itibaren aracın yanında yazan gün sayısı kadar ileriye ayarlanır
        en_erken_müsait_tarih = QDate.currentDate().addDays(gun_sayisi)

        # Kullanıcının seçtiği tarihi alıyoruz
        randevu_tarihi = self.randevu_tarihi.date()
        
        # Seçilen tarih, en erken müsait tarihten önceyse
        if randevu_tarihi < en_erken_müsait_tarih:
            QMessageBox.warning(self, "Hata", f"Bu araç {en_erken_müsait_tarih.toString('dd.MM.yyyy')} tarihinden önce müsait değil. Lütfen başka bir tarih seçin!")
            return

        # Eğer tarih uygun ise, randevu başarıyla oluşturulmuş olur
        QMessageBox.information(
            self, 
            "Başarılı", 
            f"{secili_arac.text()} için randevu oluşturuldu!\n"
            f"Tarih: {randevu_tarihi.toString('dd.MM.yyyy')}"
        )



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)  # Uygulama genelinde CSS stilini uygula

    # Giriş penceresi
    login = LoginWindow()
    if login.exec_() == QDialog.Accepted:
        # Ana pencereyi göster
        ana_pencere = AnaPencere()
        ana_pencere.show()
        sys.exit(app.exec_())