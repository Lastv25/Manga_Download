import wx
from src import modules
from src import main_menu
from src import mangareader
import os
import re
import tqdm


class Add_chapter(wx.Frame):

    def __init__(self, parent, title):
        super(Add_chapter, self).__init__(parent, title=title, size=(700, 400))

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
        self.center_sizer = wx.BoxSizer(wx.VERTICAL)
        self.center_sizer.SetMinSize((self.GetSize()[0] / 3, self.GetSize()[1]))
        self.right_sizer = wx.BoxSizer(wx.VERTICAL)
        self.right_sizer.SetMinSize((self.GetSize()[0] / 3, self.GetSize()[1]))

        # list of Websites
        website_list = self.get_Websites()
        self.list_box = wx.ListBox(self, size=(200, 55), choices=website_list, style=wx.LB_SINGLE,
                                   name="Websites Available")
        self.list_box.Bind(wx.EVT_LISTBOX, self.chosen_website)
        self.center_sizer.Add(self.list_box, 0, wx.ALL | wx.CENTER, 5)

        # list of Mangas
        manga_list = self.manga_names()
        self.list_box4 = wx.ListBox(self, size=(200, 55), choices=manga_list, style=wx.LB_SINGLE,
                                   name="Manga List")
        self.list_box4.Bind(wx.EVT_LISTBOX, self.check_name)
        self.left_sizer.Add(self.list_box4, 0, wx.ALL | wx.CENTER, 5)

        # list of Available Chapters
        self.list_box2 = wx.ListBox(self, size=(300, 400), choices=[], style=wx.LB_MULTIPLE,
                                   name="Chapters Available")
        self.left_sizer.Add(self.list_box2, 0, wx.ALL, 5)

        # list of Downloaded Chapters
        self.list_box3 = wx.ListBox(self, size=(200, 400), choices=[], style=wx.LB_SINGLE,
                                   name="Chapters Downloaded")
        self.center_sizer.Add(self.list_box3, 0, wx.ALL, 5)

        # button list
        self.right_sizer.Add((-1, 100))
        add_selected_button = wx.Button(self, label='Download Selected', size=(150, 30))
        add_selected_button.Bind(wx.EVT_BUTTON, self.download_selected)
        self.right_sizer.Add(add_selected_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        add_all_button = wx.Button(self, label='Download All', size=(150, 30))
        add_all_button.Bind(wx.EVT_BUTTON, self.download_all)
        self.right_sizer.Add(add_all_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        back_button = wx.Button(self, label='Back', size=(150, 30))
        back_button.Bind(wx.EVT_BUTTON, parent.back)
        self.right_sizer.Add(back_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        self.main_sizer.Add(self.left_sizer, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_LEFT)
        self.main_sizer.Add(self.center_sizer, flag=wx.EXPAND | wx.CENTER | wx.TOP | wx.ALIGN_CENTER)
        self.main_sizer.Add(self.right_sizer, flag=wx.EXPAND | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER)
        self.SetSizer(self.main_sizer)

    def name_def(self, name):
        path = "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"
        # Already downloaded chapter list
        chap_list = modules.tri_fusion(os.listdir(path + name), False)
        self.list_box3.Clear()
        for i in chap_list:
            self.list_box3.Append(i)

        # Chapters that can be downloaded
        try:
            url = 'https://' + website + '/'
            chap_list2 = modules.get_chapter_list(name, url)
            self.list_box2.Clear()
            for i in chap_list2:
                present = False
                for j in chap_list:
                    if i.replace(' ', '_').replace(':', '') == j:
                        present = True
                if not present:
                    self.list_box2.Append(i)
        except:
            print("Define Website")

    def check_name(self, event):
        global name_m
        name_m = event.GetString()
        self.name_def(name_m)


    def get_Websites(self):
        file = open('.\\src\\websites.txt', 'r')
        website_list = file.readlines()
        return website_list

    def chosen_website(self, event):
        global website
        website = self.list_box.GetString(self.list_box.GetSelection())
        if "\n" in website:
            website = website.split("\n")[0]
        try:
            self.name_def(name_m)
        except:
            pass

    def manga_names(self):
        path = "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"
        return os.listdir(path)

    def download(self, chap_list):
        url = 'https://' + website + '/' + name_m
        if not os.path.exists("C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\" + name_m):
            os.makedirs("C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\" + name_m)
        for i in range(len(chap_list)):
            chap_number = re.findall('\d+', chap_list[i])[0]
            chap_name = chap_list[i].replace(' ', '_').replace(':', '')
            chap_url = url + '/' + chap_number
            if "\t" in chap_name:
                chap_name = chap_name.replace("\t", "")
            elif "?" in chap_name:
                chap_name = chap_name.replace("?", "")
            elif '"' in chap_name:
                chap_name = chap_name.replace('"', "")
            if not os.path.exists("C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\" + name_m + "\\" + chap_name):
                os.makedirs("C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\" + name_m + "\\" + chap_name)
            mangareader.main(chap_url, "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\" + name_m + "\\" +
                             chap_name + "\\")
        print("Download Done")

    def download_all(self, event):
        print('download')
        chap_list = [self.list_box2.GetString(i) for i in range(self.list_box2.GetCount())]
        self.download(chap_list)

    def download_selected(self, event):
        print('download')
        chap_list = [self.list_box2.GetString(i) for i in self.list_box2.GetSelections()]
        self.download(chap_list)
