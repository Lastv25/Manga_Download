import wx
from src import modules
from src import main_menu
import errno
import os
import stat
import shutil


def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


class Remove_series(wx.Frame):

    def __init__(self, parent, title):
        super(Remove_series, self).__init__(parent, title=title, size=(500, 400))

        self.panel = Panel(self)
        self.Show()

    def back(self, event):
        print("back button")
        new_window = main_menu.Main_menu(None, title='Add Series')
        new_window.Show()
        self.Close()


class Panel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.left_sizer = wx.BoxSizer(wx.VERTICAL)
        self.left_sizer.SetMinSize((self.GetSize()[0] / 3, self.GetSize()[1]))
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.SetMinSize((self.GetSize()[0] / 3, self.GetSize()[1]))

        # list of Downloaded Series
        manga_list = self.manga_names()
        self.list_box2 = wx.ListBox(self, size=(300, 80), choices=manga_list, style=wx.LB_SINGLE,
                                   name="Series Downloaded")
        self.list_box2.Bind(wx.EVT_LISTBOX, self.check_name)
        self.left_sizer.Add(self.list_box2, 0, wx.ALL, 5)

        # list of Downloaded Chapters
        self.list_box = wx.ListBox(self, size=(300, 400), choices=[], style=wx.LB_MULTIPLE,
                                   name="Chapters Downloaded")
        self.left_sizer.Add(self.list_box, 0, wx.ALL, 5)


        # button list
        self.right_sizer.Add((-1, 100))
        add_selected_button = wx.Button(self, label='Remove Selected', size=(150, 30))
        add_selected_button.Bind(wx.EVT_BUTTON, self.remove_selected)
        self.right_sizer.Add(add_selected_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        add_all_button = wx.Button(self, label='Remove Series', size=(150, 30))
        add_all_button.Bind(wx.EVT_BUTTON, self.remove_series)
        self.right_sizer.Add(add_all_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        back_button = wx.Button(self, label='Back', size=(150, 30))
        back_button.Bind(wx.EVT_BUTTON, parent.back)
        self.right_sizer.Add(back_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        self.main_sizer.Add(self.left_sizer, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_LEFT)
        self.main_sizer.Add(self.right_sizer, flag=wx.EXPAND | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER)
        self.SetSizer(self.main_sizer)

    def check_name(self, event):
        print("checking name")
        path = "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"
        manga_list = os.listdir(path)
        input = event.GetString()
        if input in manga_list:
            self.fill_listBOx(input)
        else:
            self.list_box.Clear()

    def remove_selected(self, event):
        print("remove selected")
        path = "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"
        input = self.list_box2.GetString(self.list_box2.GetSelection())
        list_selected = [self.list_box.GetString(i) for i in self.list_box.GetSelections()]
        for i in list_selected:
            shutil.rmtree(path+input+"\\"+i, ignore_errors=False, onerror=handleRemoveReadonly)
        self.list_box.Clear()
        self.fill_listBOx(input)

    def remove_series(self, event):
        print("remove series")
        path = "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"
        input = self.list_box2.GetString(self.list_box2.GetSelection())
        shutil.rmtree(path + input, ignore_errors=False, onerror=handleRemoveReadonly)
        self.list_box.Clear()
        self.list_box2.Clear()

    def fill_listBOx(self, name):
        path = "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"
        chapter_list = modules.tri_fusion(os.listdir(path + name), False)
        for i in chapter_list:
            self.list_box.Append(i)

    def manga_names(self):
        path = "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"
        return os.listdir(path)