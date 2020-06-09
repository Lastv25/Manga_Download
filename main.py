

import wx
from src import main_menu


def main():
    app = wx.App()
    ex = main_menu.Main_menu(None, title='Main Menu')
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
