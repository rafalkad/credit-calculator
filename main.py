import tkinter as tk

from controller.controller import CreditGUIController
from model.inmemo.SQLCredit import RepositoryCreditSQL
from model.inmemo.app_engine import Session
from view.View import CreditView

if __name__ == "__main__":
    session = Session()
    credit_repo = RepositoryCreditSQL(session)
    controller = CreditGUIController()
    view = CreditView(tk.Tk(), controller)

    controller.view = view

    view.root.mainloop()
