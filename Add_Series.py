import wx
from src import modules
from src import main_menu
from src import mangareader
import os
import re


class Add_series(wx.Frame):

    def __init__(self, parent, title):
        super(Add_series, self).__init__(parent, title=title, size=(700, 400))

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

        # text ctrl for the series name
        self.text_input_readable = wx.TextCtrl(self, size=(300, -1), style=wx.TE_READONLY | wx.TE_CENTER )
        self.left_sizer.Add(self.text_input_readable, 0, wx.ALL | wx.CENTER, 5)

        self.text_input = wx.TextCtrl(self, size=(200, -1))
        self.text_input.Bind(wx.EVT_TEXT, self.check_name)
        self.left_sizer.Add(self.text_input, 0, wx.ALL | wx.CENTER, 5)

        self.text_path = wx.TextCtrl(self, size=(300, -1))
        self.text_path.Bind(wx.EVT_TEXT, self.check_path)
        self.left_sizer.Add(self.text_path, 0, wx.ALL | wx.CENTER, 5)

        # list of Websites
        website_list = self.get_Websites()
        self.list_box = wx.ListBox(self, size=(200, 55), choices=website_list, style=wx.LB_SINGLE,
                                   name="Websites Available")
        self.list_box.Bind(wx.EVT_LISTBOX, self.chosen_website)
        self.center_sizer.Add(self.list_box, 0, wx.ALL | wx.CENTER, 5)

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
        add_selected_button = wx.Button(self, label='Add Selected', size=(150, 30))
        add_selected_button.Bind(wx.EVT_BUTTON, self.add_selected)
        self.right_sizer.Add(add_selected_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        add_all_button = wx.Button(self, label='Add All', size=(150, 30))
        add_all_button.Bind(wx.EVT_BUTTON, self.add_all)
        self.right_sizer.Add(add_all_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        remove_button = wx.Button(self, label='Remove', size=(150, 30))
        remove_button.Bind(wx.EVT_BUTTON, self.remove)
        self.right_sizer.Add(remove_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        download_button = wx.Button(self, label='Download', size=(150, 30))
        download_button.Bind(wx.EVT_BUTTON, self.download)
        self.right_sizer.Add(download_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        back_button = wx.Button(self, label='Back', size=(150, 30))
        back_button.Bind(wx.EVT_BUTTON, parent.back)
        self.right_sizer.Add(back_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        self.main_sizer.Add(self.left_sizer, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_LEFT)
        self.main_sizer.Add(self.center_sizer, flag=wx.EXPAND | wx.CENTER | wx.TOP | wx.ALIGN_CENTER)
        self.main_sizer.Add(self.right_sizer, flag=wx.EXPAND | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER)
        self.SetSizer(self.main_sizer)

    def check_path(self, event):
        if event.GetString() == '':
            self.text_input_readable.SetValue("Choose a download path")

    def name_validation(self, name):
        if self.list_box.GetSelection() == wx.NOT_FOUND :
            self.text_input_readable.SetValue("Choose a website")
        else:
            url = 'https://'+website+'/'
            content = modules.get_page(url+name).decode("utf-8")
            if 'Not Found' in content:
                self.text_input_readable.SetValue("Choose a valid name or change Website")
                self.list_box2.Clear()
            else:
                self.text_input_readable.SetValue("Valid name")
                self.list_box2.Clear()
                chap_list = modules.get_chapter_list(name, url)
                for i in chap_list:
                    self.list_box2.Append(i)

    def check_name(self, event):
        global name_m
        name_m = event.GetString()
        self.name_validation(name_m)

    def get_Websites(self):
        file = open('.\\src\\websites.txt', 'r')
        website_list = file.readlines()
        return website_list

    def chosen_website(self, event):
        global website
        website = self.list_box.GetString(self.list_box.GetSelection())
        if "\n" in website:
            website = website.split("\n")[0]
        if self.text_input.GetValue() != '':
            self.name_validation(self.text_input.GetValue())

    def add_selected(self, event):
        print("add selected")
        list_selected = [self.list_box2.GetString(i) for i in self.list_box2.GetSelections()]
        for i in list_selected:
            self.list_box3.Append(i)

    def add_all(self, event):
        print("add all")
        chap_list = [self.list_box2.GetString(i) for i in range(self.list_box2.GetCount())]
        for i in chap_list:
            self.list_box3.Append(i)

    def remove(self, event):
        print("remove selected")
        choice = self.list_box3.GetSelection()
        self.list_box3.Delete(choice)

    def download(self, event):
        print('download')
        if self.list_box2.GetCount() == 0:
            print('No chapters selected')
        else:
            given_path = self.text_path.GetValue()
            if given_path != '':
                chap_list = [self.list_box3.GetString(i) for i in range(self.list_box3.GetCount())]
                url = 'https://' + website + '/' + name_m
                if not os.path.exists("C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\" + name_m):
                    os.makedirs("C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\" + name_m)
                for i in chap_list:
                    chap_number = re.findall('\d+', i)[0]
                    self.text_input_readable.SetValue("Downloading chapter: " + chap_number)
                    chap_name = i.replace(' ', '_').replace(':', '')
                    chap_url = url + '/' + chap_number
                    if not os.path.exists("C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"+name_m+"\\"+chap_name):
                        os.makedirs("C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"+name_m+"\\"+chap_name)
                    mangareader.main(chap_url, "C:\\Users\\hgmnj\\Desktop\\MangaReader\\testFolder\\"+name_m+"\\"+
                                     chap_name+"\\")
                print("Download Done")
            else:
                self.text_input_readable.SetValue("Choose a valid path")

