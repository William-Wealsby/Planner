import tkinter as tk
from tkinter import ttk
from json import loads, dumps #loads- json to string  // dumps- string to json
from os import mkdir
from os.path import exists
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen
import ssl
import calendar
import time


class window:

    def __init__(self, name, size):
        #creates tkinter app, sets size, title
        self.root = tk.Tk()
        self.root.geometry(size)
        self.root.title(name)
        self.root.grid()
        self.root.resizable(False, False)
        
        #creates notebook for frames and makes tabs invisible
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(pady = 10)
        self.style = ttk.Style()
        self.style.layout('TNotebook.Tab', [])
        self.style.configure("BW.TLabel", foreground = "black", background = "white")

        #creates menubar and assosiated menu & home tab
        self.menubar = tk.Menu(self.root)
        self.root.config(menu = self.menubar)

        self.homemenu = tk.Menu(self.menubar, tearoff=0)
        
    def end(self):
        self.root.quit()


class frame:

    def __init__(self, parent, name=str):
        #creates frame & adds the frame as a tab in the menubar, which can be interacted with
        self.parent = parent 
        self.name = name
        self.var = tk.StringVar()
        self.label = ttk.Frame(parent.notebook,borderwidth=0)
        self.label.grid(sticky='nesw',padx=5,pady=5)
        parent.notebook.add(self.label)
        self.index = parent.notebook.index(self.label)
        self.menu = tk.Menu(parent.menubar, tearoff=0)
        parent.menubar.add_cascade(label=self.name, menu=self.menu)
        self.menu.add_command(label=self.name, command=self.selecttab)

    def selecttab(self):
        self.parent.notebook.select(self.index)

    def clear(self, event=None):
        for widget in self.label.winfo_children():
            widget.destroy()


class label:

    def __init__(self, frames, msg, x=0, y=0, xspan=1, yspan=1,size='S'):
        if size == 'L':
            self.label = ttk.Label(frames.label, text=msg, borderwidth=0, relief='flat', font=('Ariel',25))
        elif size == 'M':
            self.label = ttk.Label(frames.label, text=msg, borderwidth=0, relief='flat', font=('Ariel',20))
        elif size == 'S':
            self.label = ttk.Label(frames.label, text=msg, borderwidth=0, relief='flat', font=('Ariel',15))
        self.label.grid(row=x, column=y, rowspan=xspan, columnspan=yspan,padx=5,pady=5)


class today_frame(frame):

    def __init__(self, parent, name):
        super().__init__(parent, name)
        self.make()
        self.update_weather()
        self.update_times()


    def update_times(self,event=None):
        current=datetime.now()
        cur_date=current.strftime('%A %D')
        cur_time=current.strftime('%H:%M')
        self.datelabel.label.config(text=cur_date)
        self.timelabel.label.config(text=cur_time)
        self.label.after(5000,self.update_times)


    def update_weather(self,event=None): #change lat and long in url for different locations: set to Oxford coordinates by default
        url = ("https://api.open-meteo.com/v1/forecast?latitude=51.75&longitude=1.25&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
        data=urlopen(url,context=ssl.create_default_context())
        weatherdata=loads(data.read())
        units = weatherdata['current_units']
        current_data = weatherdata['current']
        temp = str(current_data['temperature_2m'])+units['temperature_2m']
        speed = str(current_data['wind_speed_10m'])+units['wind_speed_10m']
        self.tempval.label.config(text=temp)
        self.windspeed.label.config(text=speed)
        self.label.after(1800000,self.update_weather)
        

    def make(self,event=None):
        zone='UTC+'+str(timezone.utc.utcoffset(None))[2::]
        self.sep0 = ttk.Separator(self.label,orient='horizontal')
        self.sep0.grid(row=0,column=0,columnspan=10,sticky='nsew')
        self.datelabel = label(self,'Date',0,1,2,3,'L')
        self.timelabel = label(self,'Time',2,1,2,2,'L')
        self.zonelabel = label(self,zone,2,3,2,1,'M')
        self.sep1 = ttk.Separator(self.label,orient='vertical')
        self.sep1.grid(row=0,rowspan=9,column=4,sticky='nsew')
        self.sep2 = ttk.Separator(self.label,orient='horizontal')
        self.sep2.grid(row=5,column=0,columnspan=10,sticky='nsew')
        self.weatherlabel0 = label(self,'Weather Report',0,6,2,4,'S') 
        self.templabel = label(self,'Temperature: ',2,6,1,2,'S')
        self.tempval = label(self,'',2,8,1,2,'S')
        self.windlabel = label(self,'Wind Speed: ',3,6,1,2,'S')
        self.windspeed = label(self,'',3,8,1,2,'S')


    def reminder(self,event=None):
        pass

    def lists(self,event=None):
        pass

    def stopwatch(self,event=None):
        pass

    def update(self, event=None): 
        self.clear()
        self.make()
        self.update_times()
        self.update_weather()
        if self.var.get() == '1':
            self.reminder()
        if self.var.get() == '2':
            self.lists()
        if self.var.get() == '3':
            self.stopwatch()


if __name__ == '__main__':
    main = window('Planner', '600x400')

    url = ('https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey=fc25dc062c924cdda0fac398095f5b21')
    

    # checks if folders and files exist
    #open all files; clocks.json,reminders.json;calendar.json,lists.json
    files={'Resources/clocks.json':0,'Resources/reminders.json':0,'Resources/calendar.json':0,'Resources/lists.json':0}
    if not exists('Resources'):
        mkdir('Resources')
    for file in files:
        if not exists(file):
            new=open(file,'x')
            new.close()
    for file in files:
        with open(file, 'rb') as data:
            files[file]=data
    
    today_frame = today_frame(main, 'Today')
    
    today_frame.var.set('0')
    today_frame.menu.add_separator()
    today_frame.menu.add_radiobutton(label='Reminders', variable=today_frame.var, value='1', command=today_frame.update) 
    today_frame.menu.add_radiobutton(label='Lists', variable=today_frame.var, value='2', command=today_frame.update) 
    today_frame.menu.add_radiobutton(label='Stopwatch', variable=today_frame.var, value='3', command=today_frame.update) 
    


    calendar_frame = frame(main, 'Calendar')
    reminders_frame = frame(main, 'Reminders')
    lists_frame = frame(main, 'Lists')
    timer_frame = frame(main, 'Stopwatch')
    
    

    main.menubar.add_cascade(label = 'Options', menu = main.homemenu)   
    main.homemenu.add_command(label = 'Help', command = None) 
    main.homemenu.add_command(label = 'About', command = None)
    main.homemenu.add_separator()
    main.homemenu.add_command(label = 'Exit', command = main.end)

    main.root.mainloop()
