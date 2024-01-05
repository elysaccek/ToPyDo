from random import randint

class Task:
    # Task class'ının değişkenleri
    _Title = ""
    _Info = ""
    _Day = []
    _ID = -1
    _Time = ""
    _Make = []

    # Yapıcı fonksiyon
    def __init__(self, Title: str, Info: str, Day: list[int], Time: str, Make: list[str]) -> None:
        self._Title = Title
        self._Info = Info
        self._Day = Day
        self._Time = Time
        self._Make = Make

        # ID random belirlenir
        self._ID = randint(100000000,999999999)

    # Görevin değişkenlerini değiştirmek
    def setTask(self, Title: str, Info: str, Day: list[int], Time: str, Make: list[str]) -> None:
        self._Title = Title
        self._Info = Info
        self._Day = Day
        self._Time = Time

        self._Make = Make

        # ID random belirlenir
        self._ID = randint(100000000,999999999)

    # ID değiştirme
    def setID(self, ID: int) -> int:
        if(ID >= 100000000 or ID <= 999999999):
            self._ID = ID
            return 0
        else:
            return -1

    # Tarihe göre yapılıp yapılmadığını döndürmek    
    def isMaked(self, Date: str) -> bool:
        if Date in self._Make:
            return True
        else:
            return False

    # Tarihin durumunu değiştirmek
    def changeMaked(self, Date: str) -> None:
        if Date in self._Make:
            self._Make.remove(Date)
        else:
            self._Make.append(Date)
    
    # Başlığı döndürür
    def getTitle(self) -> str:
        return self._Title
    
    # İçeriği döndürür
    def getInfo(self) -> str:
        return self._Info
    
    # Zamanı döndürür
    def getTime(self) -> str:
        return self._Time

    # Make dizisini döndürür
    def getMaked(self) -> list:
        return self._Make
    
    # Day dizisini döndürür
    def getDay(self) -> list:
        return self._Day

class Tasks:
    # Görevleri saklayan 2D array 8. array belirli günü olan görevler
    _all_Tasks = [[],[],[],[],[],[],[],[]]

    # __init__ constructor fonksiyonu hiçbir değer almaya bilir
    # veya all_Tasks değeri list[list[Task | None]] olacak şekilde
    # 2D array değeri alabilir
    def __init__(self, all_Tasks: list[list[Task]] | None) -> None:
        if all_Tasks != None:
            self._all_Tasks = all_Tasks
        else:
            self._all_Tasks = [[],[],[],[],[],[],[],[],[]]

    # addTask fonksiyonu gün numarası ve görev değişkeni alıp 
    # _all_Tasks arrrayindeki gerekli güne görevi eklemekte
    def addTask(self, day_Number: int, task : Task) -> None:
        if task not in self._all_Tasks[day_Number]:
            self._all_Tasks[day_Number].append(task)

    # removeTask fonksiyonu ise gün numarası ve görev numarası
    # değişkenlerini alıp gerekli görevi silmekte
    def removeTask(self, day_Number: int, task_Number: int) -> None:
        self._all_Tasks[day_Number].pop(task_Number)

    # task ile silme yapar
    def removeTaskToVal(self, day_Number: int, task: Task) -> None:
        print(day_Number)
        if task in self._all_Tasks[day_Number]:
            self._all_Tasks[day_Number].remove(task)

    # Yapılma durumunu değiştirir
    def changeMaked(self, day_Number: int, task_Number: int, date: str) -> None:
        (self._all_Tasks[day_Number])[task_Number].changeMaked(date)

    # Görevi döndürür
    def getTask(self, day_Number: int, task_Number: int) -> Task:
        task = (self._all_Tasks[day_Number])[task_Number]
        return task
    
    # Gün numarasına göre kaç adet görev var döndürür
    def getDayTaskSize(self, day_Number: int) -> int:
        return len(self._all_Tasks[day_Number])
    
    # Tüm görevleri düzenler ve döndürür
    def getAllTask(self) -> list:
        empty_list = []

        for i in range(8):
            for task in self._all_Tasks[i]:
                if task not in empty_list:
                    empty_list.append(task)
        
        return empty_list
