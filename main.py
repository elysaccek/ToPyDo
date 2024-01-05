from gui import *

if __name__ == '__main__':
    tasks = Tasks(all_Tasks= None)

    file = FileControl("tasks.topydo")
    tasks = file.readFile()

    app = QApplication([])
    window = ToPyDo_Gui("ToPyDo", 800, 600, tasks, "tasks.topydo")

    window.show()
    sys.exit(app.exec_())
