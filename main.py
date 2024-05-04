import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QFileDialog
from ytvideodownloader import Ui_YoutubeVideoDownloader_Form
from pytube import YouTube

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_YoutubeVideoDownloader_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_download.clicked.connect(self.Download)
        self.setFixedSize(400, 300)

    # İndirme fonksiyonu
    def Download(self):
        link = self.ui.lineEdit_URL.text().strip()
        is_mp3_selected = self.ui.checkBox_MP3.isChecked()
        is_mp4_selected = self.ui.checkBox_MP4.isChecked()

        if not link:
            QMessageBox.warning(self, "Hata", "Lütfen bir URL girin!")
            return

        if is_mp3_selected and is_mp4_selected:
            QMessageBox.warning(self, "Hata", "Lütfen sadece bir format seçin!")
            return
        elif not is_mp3_selected and not is_mp4_selected:
            QMessageBox.warning(self, "Hata", "Lütfen bir format seçin!")
            return

        # Kullanıcıya dosyanın kaydedileceği konumu seçtirme
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(self, "Kaydedilecek Klasörü Seç", options=options)

        if folder:
            download_folder = folder
        else:
            download_folder = "~/Desktop"  # Varsayılan olarak masaüstüne kaydet

        yt = YouTube(link)
        if is_mp3_selected:
            stream = yt.streams.filter(only_audio=True).first()
        else:
            stream = yt.streams.get_highest_resolution()

        file_path = f"{download_folder}/{yt.title}.{stream.subtype}"  # Dosya yolu ve adı
        stream.download(output_path=download_folder, filename=yt.title)  # Dosyayı indirme

        # Dosya yolu üzerinde bir HTML linki oluştur
        file_link = f'<a href="file://{file_path}">{yt.title}.{stream.subtype}</a>'
        QMessageBox.information(self, "İndirme Tamamlandı", f"Video başarıyla indirildi. Dosyayı buradan açabilirsiniz:<br>{file_link}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())
