import wx
from src import modules
from src import main_menu
from src import mangareader
import os
from urllib.parse import urlparse


class Website_management(wx.Frame):

    def __init__(self, parent, title):
        super(Website_management, self).__init__(parent, title=title, size=(500, 400))

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

        # text ctrl for the series name
        self.text_input_readable = wx.TextCtrl(self, size=(300, -1), style=wx.TE_READONLY | wx.TE_CENTER)
        self.text_input_readable.SetValue('Input website link like: https://www.site.com')
        self.left_sizer.Add(self.text_input_readable, 0, wx.ALL | wx.CENTER, 5)

        self.text_input = wx.TextCtrl(self, size=(300, -1))
        self.left_sizer.Add(self.text_input, 0, wx.ALL | wx.CENTER, 5)

        # list of Websites
        website_list = self.get_Websites()
        self.list_box = wx.ListBox(self, size=(300, 400), choices=website_list, style=wx.LB_SINGLE,
                                   name="Websites Available")
        self.left_sizer.Add(self.list_box, 0, wx.ALL | wx.CENTER, 5)

        # button list
        self.right_sizer.Add((-1, 100))
        add_selected_button = wx.Button(self, label='Add', size=(150, 30))
        add_selected_button.Bind(wx.EVT_BUTTON, self.add)
        self.right_sizer.Add(add_selected_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        remove_button = wx.Button(self, label='Remove', size=(150, 30))
        remove_button.Bind(wx.EVT_BUTTON, self.remove)
        self.right_sizer.Add(remove_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        back_button = wx.Button(self, label='Back', size=(150, 30))
        back_button.Bind(wx.EVT_BUTTON, parent.back)
        self.right_sizer.Add(back_button, 0, wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER | wx.ALIGN_CENTRE, 5)

        self.main_sizer.Add(self.left_sizer, flag=wx.EXPAND | wx.LEFT | wx.TOP | wx.ALIGN_LEFT)
        self.main_sizer.Add(self.right_sizer, flag=wx.EXPAND | wx.RIGHT | wx.TOP | wx.ALIGN_CENTER)
        self.SetSizer(self.main_sizer)

    def get_Websites(self):
        file = open('.\\src\\websites.txt', 'r')
        website_list = file.readlines()
        return website_list

    def add(self, event):
        print("add selected")
        website = self.text_input.GetValue()
        print(self.check_website(website))
        if self.check_website(website):
            file = open(os.getcwd()+'\src\websites.txt', 'a')
            file.write(website.split('//')[1]+"\n")
            file.close()
            self.list_box.Clear()
            for i in self.get_Websites():
                self.list_box.Append(i)

    def remove(self, event):
        print("remove selected")
        choice = self.list_box.GetSelection()
        website_list = self.get_Websites()
        output = ''
        for i in website_list:
            if i != self.list_box.GetString(choice):
                output += i
        file = open(os.getcwd() + '\src\websites.txt', 'w')
        file.write(output)
        file.close()
        self.list_box.Delete(choice)

    def check_website(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
