import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime


window = tk.Tk()
window.geometry("400x400")

def add():
    hour = hours.get()
    min = mins.get()
    if hour != " " and min != " ":
        strTime = hour + ":" + min + ":" + "00"
        time_list.insert(tk.END,strTime)
    else:
        messagebox.showwarning("Warning","Missing values")

def delete():
    try:
        deleteVar = time_list.curselection()[0]
        time_list.delete(deleteVar)
    except:
        messagebox.showwarning("Warning","Select a value")

def show():
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        if current_time in time_list.get(0,time_list.size()):
            print(current_time)
            break
    

time_list = tk.Listbox(window,height=5,width=50)
time_list.place(x=50,y=10)

timeLabel = tk.Label(window,text="Time")
timeLabel.place(x=50,y=150)

hourVar = tk.StringVar()
hours = ttk.Combobox(window,textvariable=hourVar,width=5,state="readonly")
hours.place(x=100,y=150)
tmp_hours = list(range(24))
hours_list = []
for value in tmp_hours:
    if len(str(value)) == 1:
        value = "0" + str(value)
        hours_list.append(value)
    else:
        hours_list.append(str(value))
hours.set("00")
hours["values"] = hours_list

minsVar = tk.StringVar()
mins = ttk.Combobox(window,textvariable=minsVar,width=5,state="readonly")
mins.place(x=170,y=150)
tmp_mins = list(range(60))
mins_list = []
for value in tmp_mins:
    if len(str(value)) == 1:
        value = "0" + str(value)
        mins_list.append(value)
    else:
        mins_list.append(str(value))
mins.set("00")
mins["values"] = mins_list

add_button = tk.Button(window, text = "Add", command=lambda:add())
add_button.place(x=50,y=200)

delete_button = tk.Button(window, text = "Delete", command=lambda:delete())
delete_button.place(x=50,y=250)

show_button = tk.Button(window, text = "Show Time", command=lambda:show())
show_button.place(x=50,y=300)

window.mainloop()