import wx
from src import modules
from src import Add_Series, Remove_Series, Add_Chapter, Website_Management
import os


class Main_menu(wx.Frame):

    def __init__(self, parent, title):
        super(Main_menu, self).__init__(parent, title=title, size=(600, 400))

        self.panel = Panel(self)
        self.Show()

    def add_series(self, event):
        print("in add_series")
        new_window = Add_Series.Add_series(None, title='Add Series')
        new_window.Show()
        self.Close()

    def remove_series(self, event):
        print("in remove_series")
        new_window = Remove_Series.Remove_series(None, title='Remove Series')
        new_window.Show()
        self.Close()

    def add_chapter(self, event):
        print("in add_chapter")
        new_window = Add_Chapter.Add_chapter(None, title='Add Chapter')
        new_window.Show()
        self.Close()

    def website_management(self, event):
        print("in website_management")
        new_window = Website_Management.Website_management(None, title='Website Management')
        new_window.Show()
        self.Close()


class Panel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_sizer.SetMinSize((3 * (self.GetSize()[0] / 4), self.GetSize()[1]))
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.SetMinSize((self.GetSize()[0] / 4, self.GetSize()[1]))

        # list of mangas
        manga_list = self.populate_list()
        self.list_ctrl = wx.ListCtrl(
            self, size=(-1, 400),
            style=wx.LC_REPORT | wx.BORDER_SUNKEN
        )
        self.list_ctrl.InsertColumn(0, 'Manga', width=140)
        self.list_ctrl.InsertColumn(1, 'Chapters Downloaded', width=130)
        self.list_ctrl.InsertColumn(2, 'Total Chapters', width=90)
        for i in manga_list:
            self.list_ctrl.Append(i)
        self.left_sizer.Add(self.list_ctrl, 0, wx.ALL, 5)

        # buttons
        add_series_button = wx.Button(self, label='Add Series', size=(150, 30))
        add_series_button.Bind(wx.EVT_BUTTON, parent.add_series)
        self.right_sizer.Add((-1, 100))
        self.right_sizer.Add(add_series_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        remove_series_button = wx.Button(self, label='Remove Series', size=(150, 30))
        remove_series_button.Bind(wx.EVT_BUTTON, parent.remove_series)
        self.right_sizer.Add(remove_series_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        add_chapter_button = wx.Button(self, label='Add Chapter', size=(150, 30))
        add_chapter_button.Bind(wx.EVT_BUTTON, parent.add_chapter)
        self.right_sizer.Add(add_chapter_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        add_website_button = wx.Button(self, label='Website Management', size=(150, 30))
        add_website_button.Bind(wx.EVT_BUTTON, parent.website_management)
        self.right_sizer.Add(add_website_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        self.main_sizer.Add(self.left_sizer)
        self.main_sizer.Add(self.right_sizer)
        self.SetSizer(self.main_sizer)

    def on_press(self, event):
        print('in on_press')


    def populate_list(self):
        path = "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder"
        manga_list = os.listdir(path)

        output_list = []
        for i in manga_list:
            output_list.append((i, len(os.listdir(path+"\\"+i)),
                                modules.get_chapter_number(i, "https://www.mangareader.net/")))
        return output_list
