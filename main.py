from tkinter import *
from global_var import init
from view.login import Login

if __name__ == '__main__':
    init()
    main_window = Tk()
    Login(main_window)
    main_window.mainloop()
