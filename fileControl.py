import json
from taskOperations import *

class FileControl:
    _file_Dir = ""
    def __init__(self, file_Dir : str) -> None:
        self._file_Dir = file_Dir

    # Dosyayı okur ve Tasks olarak döndürür
    def readFile(self) -> Tasks:
        tasks = Tasks(all_Tasks= None)
        with open(self._file_Dir, 'r') as file:
            tasks_data = json.load(file)
                
        for task_data in tasks_data:
            task_create = Task(task_data["TT"], task_data["TI"], task_data["TD"], task_data["TTm"], task_data["TM"])

            for task_day in task_data["TD"]:
                tasks.addTask(task_day-1, task_create)

        return tasks

    # Taskları alır ve kaydeder
    def writeFile(self, tasks : Tasks) -> None:
        all_data = []
        for task in tasks.getAllTask():
            new_data = {
                "TT": "",
                "TI": "",
                "TD": [],
                "TTm": "",
                "TM": []
            }

            # new_data içeriği doldurulur
            new_data["TT"] = task.getTitle()
            new_data["TI"] = task.getInfo()
            new_data["TD"] = task.getDay()
            new_data["TTm"] = task.getTime()
            new_data["TM"] = task.getMaked()
            
            # new_data all_data ya eklenir
            all_data.append(new_data)

            with open(self._file_Dir, 'w') as dosya:
                json.dump(all_data, dosya, indent=4)
        
