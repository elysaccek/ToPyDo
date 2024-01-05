from guiHelper import *
from sendNotification import *

class ToPyDo_Gui(QMainWindow):
    # Class tanımlamaları
    _w = 0
    _h = 0
    _title = ""
    _tasks = None
    _selected_date = ""
    _selected_day = 0
    _selected_task = -1
    _file_Str = ""

    # Yapıcı Fonksiyon
    def __init__(self, title: str, w: int, h: int, tasks: Tasks, fileStr: str) -> None:
        super().__init__()

        # Pencere Özellikleri
        self._w = w
        self._h = h
        self._title = title

        # Görevlerin Depolandığı Class
        self._tasks = tasks
        self._file_Str = fileStr

        # Pencerenin ayarlanması
        self.setWindowTitle(self._title)
        self.setFixedSize(self._w, self._h)

        self.__center()         # Pencereyi Ekranın Ortasına Gönderir  
        self.__upperMenu()      # Pencere Üzerindeki Menüleri Ekler
        self.__setPage()        # Pencere İçeriğini Ekler

    # Pencere Ortalama Fonksiyonu
    def __center(self):
        screen = self.frameGeometry()
        screenCenter = QDesktopWidget().availableGeometry().center()
        screen.moveCenter(screenCenter)
        self.move(screen.topLeft())

    # --------------------------> Pencere Üst Menüsü İşlemleri -------------------------->
    def __upperMenu(self):
        menuBar = self.menuBar()

        file_Menu = menuBar.addMenu('File')

        # File menüsüne New File... Open File... Save ve Exit Butonları ekler
        new_File = QAction('New File...', self)
        new_File.triggered.connect(self.__newFileAction)
        file_Menu.addAction(new_File)

        open_File = QAction('Open File...', self)
        open_File.triggered.connect(self.__openFileAction)
        file_Menu.addAction(open_File)

        save_File = QAction('Save', self)
        save_File.triggered.connect(self.__saveFileAction)
        file_Menu.addAction(save_File)

        exit_ = QAction('Exit', self)
        exit_.triggered.connect(self.__exitAction)
        file_Menu.addAction(exit_)
    
    def __openFileAction(self):
        # Dosya açma penceresini açar
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "Topydo Dosyaları (*.topydo)", options=options)

        # Seçilen dosyanın yolunu FileControl classına yollar
        file = FileControl(file_name)
        # Dosyadaki görevleri kaydeder
        self._tasks = None
        self._tasks = file.readFile()

        # Her şeyi günceller
        self._selected_task = -1
        self.calendar.setSelectedDate(QDate.currentDate())
        self.table.Update(self._tasks, self.calendar.Day(), self.calendar.Date())
        self.editWidget.Clear()

    def __newFileAction(self):
        # Listeyi sıfırlar
        self._tasks = Tasks(None)

        # Her şeyi günceller
        self._selected_task = -1
        self.calendar.setSelectedDate(QDate.currentDate())
        self.table.Update(self._tasks, self.calendar.Day(), self.calendar.Date())
        self.editWidget.Clear()

    def __saveFileAction(self):
        file = FileControl(self._file_Str)
        file.writeFile(self._tasks)

    def __exitAction(self):
        sys.exit()
    # <-------------------------- Pencere Üst Menüsü İşlemleri <--------------------------
    
    # --------------------------> Pencere İçeriğinin Eklenmesi -------------------------->
    def __setPage(self):
        # Takvim çağrılır
        self.calendar = Calendar(self)
    
        # Takvimde gün tıklanmasında __celenndarClick çağrılır
        self.calendar.clicked[QDate].connect(self.__calendarClick)

        self._selected_date = self.calendar.Date()
        self._selected_day = self.calendar.Day()

        # Tablo Çağrılır
        self.table = Table(self)

        # Tablodaki hücrelere tıklamayı __on_cell_clicked'e bağlar
        self.table.cellClicked.connect(self.__on_cell_clicked) # Tıklanan Hücreyi alır

        # Edit Widgetini çağırır
        self.editWidget = EditWidget(self)

        # Edit Widget kaydetme ve güncelleme
        buttonNew = QPushButton("Yeni", self)
        buttonNew.setToolTip("Yeni Görev Olarak Kaydet")
        buttonNew.setGeometry(450, 530, 120, 40)
        buttonNew.clicked.connect(self.__newEditWidget)

        buttonSave = QPushButton("Kaydet", self)
        buttonSave.setToolTip("Görevi Düzenler")
        buttonSave.setGeometry(640, 530, 120, 40)
        buttonSave.clicked.connect(self.__saveEditWidget)
    
    def __newEditWidget(self):
        # Datayı günceller
        data = self.editWidget.Get()
        if data != -1:
            newTask = Task(data[0], data[1], data[2], (data[3] if data[4] else [None]), [])
            for day in data[2]:
                self._tasks.addTask(day-1, newTask)

            # Günceller
            self.table.Update(self._tasks, self._selected_day, self._selected_date)
            # Bildirim yollar
            sendNotification("todopy", "ToDoPy", "Görev başarıyla eklendi", 500)
        else:
            sendNotification("todopy", "ToDoPy", "Kırmızı alanları doldurunuz!!!", 500)

    def __saveEditWidget(self):
        if self._selected_task != -1:
            # Datayı günceller
            data = self.editWidget.Get()
            if data != -1:
                selected = self._tasks.getTask(self._selected_day, self._selected_task).getMaked()
                self._tasks.getTask(self._selected_day, self._selected_task).setTask(data[0], data[1], data[2], (data[3] if data[4] else None), selected)

                # Görevlerin günlerini düzenler
                for day in range(7):
                    if day+1 in data[2]:
                        self._tasks.addTask(day, self._tasks.getTask(self._selected_day, self._selected_task))
                    else:
                        self._tasks.removeTaskToVal(day, self._tasks.getTask(self._selected_day, self._selected_task))

                # Günceller
                self.table.Update(self._tasks, self._selected_day, self._selected_date)
                # Bildirim yollar
                sendNotification("todopy", "ToDoPy", "Görev başarıyla güncellendi", 500)
            else:
                sendNotification("todopy", "ToDoPy", "Kırmızı alanları doldurunuz!!!", 500)
    
    def __calendarClick(self, date: QDate):
        # Seçilen günü günceller
        self._selected_task = -1
        self._selected_date = date.toString("dd.MM.yyyy")
        self._selected_day = (date.dayOfWeek()-1)
        self.table.Update(self._tasks, self._selected_day, self._selected_date)      # Tabloyu günceller
        self.editWidget.Clear()                                 # Görev ayarlamalarını sınıflar
                
    def __on_cell_clicked(self, row, column):
        self._selected_task = row   # seçili görevigünceller
        # Column 1 ise işlev yapsın işaretleme işlevleri
        if column == 1:
            self.table.UpdateMaked(self._tasks.getTask(self._selected_day, row), row, self._selected_date)
            self._tasks.changeMaked(self._selected_day, row, self._selected_date)
        else:
            self.editWidget.Set(self._tasks.getTask(self._selected_day, row))
    # <-------------------------- Pencere İçeriğinin Eklenmesi <--------------------------