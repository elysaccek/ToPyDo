import sys
from PyQt5.QtCore import QDate

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget

from fileControl import *
from taskOperations import Tasks

# TAKVİM CLASSI
class Calendar(QCalendarWidget):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        # Takvimdeki ayrım çizgilerini kapatır
        self.setGridVisible(False)

        # Takvim başındaki hafta numarasını gizler
        self.setFirstDayOfWeek(1)
        self.setVerticalHeaderFormat(self.NoVerticalHeader)

        # Takvim boyutlandırma ve yerleştirme
        self.setFixedSize(QSize(400, 280))
        self.move(10,30)

    # Seçili tarih değerini str döndürür
    def Date(self) -> str:
        return self.selectedDate().toString("dd.MM.yyyy")

    # Seçili gün değerini int döndürür [0,6]
    def Day(self) -> int:
        return (self.selectedDate().dayOfWeek()-1)

# TABLO CLASSI
class Table(QTableWidget):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        # Sütün sayısı belirleme
        self.setColumnCount(2)

        # Tablodaki sütünların genişliklerinin ayarlanması
        self.setColumnWidth(1,100)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

        # Satır numaralandırmasını kapatma
        self.verticalHeader().setVisible(False)

        # Başlıklar
        self.setHorizontalHeaderLabels(["Görev", "Yapıldı Mı?"])

        # Tablo boyutlandırma ve yerleştirme
        self.setFixedSize(QSize(400, 250))
        self.move(10,320)
    
    def Update(self, tasks: Tasks, selectedDay: int ,selectedDate: str) -> None:
        # row değerini alır
        row = tasks.getDayTaskSize(selectedDay)
        self.setRowCount(row)

        for i in range(row):
            # Görevin ismini alır ve setItem ile ilk sutuna atar
            task = tasks.getTask(selectedDay, i)
            item = QTableWidgetItem(f"{task.getTitle()}")
            item.setFlags(Qt.ItemIsEnabled)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(i, 0, item)

            # Görevin durumunu alır ve setItem ile ikinci sutuna atar
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemIsEnabled)

            if task.isMaked(selectedDate):
                icon = QIcon('data/true.ico')
            else:
                icon = QIcon('data/false.ico')
            
            # iconun ayarlanması
            self.setItem(i, 1, item)
            self.setCellWidget(i, 1, self.__createCenteredImage(icon))
    
    # Görevin yapılma durumunu değiştirir
    def UpdateMaked(self, task: Task, row: int, selectedDate: str) -> None:
        # Eğer görev yapılmış ise görevi yapılmamış olarak değiştir
        if task.isMaked(selectedDate):
            new_icon = QIcon('data/false.ico')
        # Eğer görev yapılmamış ise görevi yapılmış olarak değiştir
        else:
            new_icon = QIcon('data/true.ico')

        # Yeni ico'yu yükler ve ortalar
        item = QTableWidgetItem()
        self.setItem(row, 1, item)
        self.setCellWidget(row, 1, self.__createCenteredImage(new_icon))
    
    # İconu ortalar
    def __createCenteredImage(self, icon):
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setPixmap(icon.pixmap(32, 32))  # İkon boyutunu ayarlamak için pixmap kullanır
        return label

# EDIT KISMININ CLASSI
class EditWidget(QWidget):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        self.setGeometry(420, 30, 370, 540)
        self.__CreateTitleLine()
        self.__CreateInfoLine()
        self.__CreateWeekDaysLine()
        self.__CreateDateSelectLine()

    # Tüm içeriği temizler
    def Clear(self) -> None:
        self.__errorClear()
        self.title_edit.setText("")
        self.info_edit.setText("")

        for day_Number in range(7):
            self.checkboxes_Days[day_Number].setChecked(False)

        self.date_checkbox.setChecked(False)
        self.date_edit.setDate(QDate.currentDate())

    # Task değişkenine göre tüm değerleri düzenler
    def Set(self, task: Task) -> None:
        self.__errorClear()
        self.title_edit.setText(task.getTitle())
        self.info_edit.setText(task.getInfo())

        for day_Number in range(7):
            if (day_Number+1) in task._Day:
                self.checkboxes_Days[day_Number].setChecked(True)
            else:
                self.checkboxes_Days[day_Number].setChecked(False)
        
        if task.getTime() != "":
            self.date_checkbox.setChecked(True)
            self.date_edit.setDate(QDate.fromString(task.getTime(), "dd.MM.yyyy"))
        else:
            self.date_checkbox.setChecked(False)
            self.date_edit.setDate(QDate.currentDate()) 

    def Get(self) -> list | int:
        cbl = []
        i = 0
        for cb in self.checkboxes_Days:
            if cb.isChecked():
                cbl.append(i+1)
            i += 1
        
        if self.title_edit.text() != "" and (cbl != [] or (self.date_edit.date().toString("dd.MM.yyyy") and self.date_checkbox.isChecked())):
            self.__errorClear()
            return [self.title_edit.text(), self.info_edit.toPlainText(), cbl, self.date_edit.date().toString("dd.MM.yyyy"), self.date_checkbox.isChecked()]
        else:
            # Eksik olan kısımı kırmızıya boyamak
            if self.title_edit.text() == "":
                self.title_label.setStyleSheet("color: red")
            if cbl == []:
                self.days_label.setStyleSheet("color: red")
            if not (self.date_edit.date().toString("dd.MM.yyyy") and self.date_checkbox.isChecked()):
                self.date_label.setStyleSheet("color: red")
            return -1
        
    def __errorClear(self) -> None:
        self.title_label.setStyleSheet("color: black")
        self.days_label.setStyleSheet("color: black")
        self.date_label.setStyleSheet("color: black")

    # Başlık düzenleme satırı
    def __CreateTitleLine(self) -> None:
        self.title_label = QLabel("Başlık", self)
        self.title_label.move(30, 30)

        self.title_edit = QLineEdit(self)
        self.title_edit.setText("")
        self.title_edit.setStyleSheet("border: 1px solid lightgrey; border-radius: 6px;")
        self.title_edit.setMaxLength(25)

        self.title_edit.setFixedSize(QSize(230,30))
        self.title_edit.move(100, 30)

    # İçerik düzenleme satırı
    def __CreateInfoLine(self) -> None:
        self.info_label = QLabel("İçerik", self)
        self.info_label.move(30, 90)

        self.info_edit = QTextEdit(self)
        self.info_edit.setPlainText("")

        self.info_edit.setFixedSize(QSize(230,90))
        self.info_edit.move(100, 90)

    # Haftanın günlerini seçim satırı
    def __CreateWeekDaysLine(self) -> None:
        self.days_label = QLabel("Günler", self)
        self.days_label.move(30, 210)

        days_of_week = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
        self.checkboxes_Days = []

        i = 0
        for cb in days_of_week:
            checkbox = QCheckBox(self)
            checkbox.move(100 + i*36, 210)
            self.checkboxes_Days.append(checkbox)
            i+=1
                    
    # Tarih seçim satırı
    def __CreateDateSelectLine(self) -> None:
        self.date_label = QLabel("Tarih", self)
        self.date_label.move(30, 260)

        self.date_edit = QDateEdit(self)
        self.date_edit.move(100, 260)

        # Takvimin varsayılan seçili tarihi bugun
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setFixedSize(130, 30)
        self.date_edit.setAlignment(Qt.AlignCenter)
        # Takvim popup'ını etkinleştirir
        self.date_edit.setCalendarPopup(True)

        self.date_checkbox = QCheckBox(self)
        self.date_checkbox.move(260, 260)