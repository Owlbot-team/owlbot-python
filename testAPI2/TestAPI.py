# For tutorial on JSON request see https://realpython.com/python-requests/

import requests
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image  # pillow library
import time
from threading import Thread
import csv
from datetime import datetime

url = 'https://owlbot.loginto.me/input'
token = ""
is_cam_movable = True


class Camera:
    def __init__(self):
        self.is_cam_movable = True
        self.token = ""

    def set_token(self, value):
        self.token = value
        print(f'token: {value}')

    def verify_dict(self, data):
        """Returns True if data is of type dict, otherwise returns False"""
        if type(data) is dict:
            return True
        else:
            print("Error: data was not a dict, was instead "
                  "{}".format(type(data)))
            return False

    def five_sec_timer(self):
        """Times for 5 seconds"""
        time.sleep(5)
        self.is_cam_movable = True

    def move_camera(self, value, xValue, zValue):
        """Moves the camera to location specified in value/xValue/zValue"""
        print("Moving Camera")

        if not self.is_cam_movable:
            print("Error: You can\'t do that yet! Please wait.")
            return

        response = requests.get(url, params={
            'value': str(value),
            'xyval': str(xValue),
            'zval': str(zValue),
            'token': token
        })

        # Get the response data
        data = response.json()

        # Verify that it's a dictionary
        if not self.verify_dict(data):
            return

        # Print the data
        print(data)
        self.is_cam_movable = False
        Thread(target=self.five_sec_timer).start()


class Statistics:
    def __init__(self):
        self.read_stat = True
 
    def verify_dict(self, data):
        """Returns True if data is of type dict, otherwise returns False"""
        if type(data) is dict:
            return True
        else:
            print("Error: data was not a dict, was instead "
                  "{}".format(type(data)))
            return False

    def one_sec_timer(self):
        """Times for 1 second"""
        time.sleep(1)
        self.read_stat = True

    def read_statistics(self, value):
        """Reads temperature and wind speed"""
        print("Reading statistics")

        if not self.read_stat:
            print("Error: You can\'t do that yet! Please wait.")
            return

        with open('stats_file.csv', newline='', mode='w') as stats_file:
            fieldnames = ['Time in seconds', 'Trunk temp', 'Branch temp']
            stats_writer = csv.writer(stats_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            stats_writer.writerow(fieldnames)
          
            keep_reading = True
            timestampStr = ""
            readingCount = 0

            while keep_reading:
                try:
                    dateTimeObj = datetime.now()
                    timestampStrNew = dateTimeObj.strftime("%H:%M:%S")

                    if timestampStrNew != timestampStr:
                        response = requests.get(url, params={
                            'value': str(value),
                            'token': token
                        })

                        # Get the response data
                        data = response.json()

                        # Print the data
                        # print(data)

                        timestampStr = timestampStrNew
                        readingCount += 1

                        print(f'{readingCount}: TT: {data[0][6]} BT: {data[1][6]} TW: {data[2][6]} BW: {data[3][6]}')
                        # for now, just record the temperatures
                        stats_writer.writerow([readingCount, data[0][6], data[1][6]])

                        # Start the timer
                        self.read_stat = False
                        Thread(target=self.one_sec_timer).start()

                except KeyboardInterrupt:
                    keep_reading = False
                    print("Stopped reading!")



root = tk.Tk()

root.title("Owlbot Python GUI")     # Add a title
root.iconbitmap('owlbot.ico')

root.config(bg="red")

camera = Camera()
statistics = Statistics()

frame = tk.Canvas(root, width=640, height=480)
frame.pack_propagate(False)

root.wm_attributes('-transparentcolor', 'grey')
frame.config(bg='grey')
name = Label(frame, text="Token", fg="white", bg='grey').place(x=30, y=50)
e1 = Entry(root)
e1.place(x=72, y=51)
button = tk.Button(frame, text="submit", activebackground="pink", activeforeground="blue",
                   command=lambda: camera.set_token(e1.get())).place(x=220, y=49)

imgOwlbot = Image.open("Owlbot.jpg")
new_image = imgOwlbot.resize((620, 460))
imgOwlbot2 = ImageTk.PhotoImage(new_image)
frame.create_image(10, 10, anchor='nw', image=imgOwlbot2)

imgOwl = Image.open("Owlbot.jpg")
new_image = imgOwl.resize((120, 95))
imgOwl2 = ImageTk.PhotoImage(new_image)
Camera_Owl = tk.Button(frame, text="", image=imgOwl2, compound="left",
                       command=lambda: camera.move_camera(4, 145, 62))
Camera_Owl.place(x=20, y=200)


imgEliot = Image.open("Eliot.png")
new_image = imgEliot.resize((85, 95))
imgEliot2 = ImageTk.PhotoImage(new_image)
Camera_Eliot = tk.Button(frame, text="", image=imgEliot2, compound="left",
                         command=lambda: camera.move_camera(4, 95, 80))
Camera_Eliot.place(x=170, y=200)

imgChirpy = Image.open("Chirpy.png")
new_image = imgChirpy.resize((105, 95))
imgChirpy2 = ImageTk.PhotoImage(new_image)
Camera_Chirpy = tk.Button(frame, text="", image=imgChirpy2, compound="left",
                          command=lambda: camera.move_camera(4, 55, 63))
Camera_Chirpy.place(x=280, y=200)

imgMat = Image.open("Mat.png")
new_image = imgMat.resize((80, 95))
imgMat2 = ImageTk.PhotoImage(new_image)
Camera_Mat = tk.Button(frame, text="", image=imgMat2, compound="left",
                       command=lambda: camera.move_camera(4, 34, 56))
Camera_Mat.place(x=415, y=200)

imgHoward = Image.open("Howard.png")
new_image = imgHoward.resize((95, 120))
imgHoward2 = ImageTk.PhotoImage(new_image)
Camera_HOWARD = tk.Button(frame, text="", image=imgHoward2, compound="left",
                          command=lambda: camera.move_camera(4, 16, 57))
Camera_HOWARD.place(x=520, y=200)

imgStats = Image.open("stats.png")
new_image = imgStats.resize((95, 95))
imgStats2 = ImageTk.PhotoImage(new_image)
Get_STATS = tk.Button(frame, text="", image=imgStats2, compound="left",
                      command=lambda: statistics.read_statistics(5))
Get_STATS.place(x=20, y=320)




frame.pack()
root.mainloop()

# if response.status_code == 200:
#    print('Success!')
# elif response.status_code == 404:
#    print('Not Found.')
# OWL:
# value: 4
# xValue: 147
# zValue: 66
# LIGHT:
# value: 4
# xValue: 16
# zValue: 57
