# For tutorial on JSON request see https://realpython.com/python-requests/

import requests
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
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

    @staticmethod
    def verify_dict(data):
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

    def move_camera(self, value, x_value, z_value):
        """Moves the camera to location specified in value/xValue/zValue"""
        print("Moving Camera")

        if not self.is_cam_movable:
            print("Error: You can\'t do that yet! Please wait.")
            return

        response = requests.get(url, params={
            'value': str(value),
            'xyval': str(x_value),
            'zval': str(z_value),
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
        self.stats_run = True

    @staticmethod
    def verify_dict(data):
        """Returns True if data is of type dict, otherwise returns False"""
        if type(data) is dict:
            return True
        else:
            print("Error: data was not a dict, was instead "
                  "{}".format(type(data)))
            return False

    def stop(self):
        print("\nstatistic stopped.")
        self.update_label("                                                        ")
        self.update_label("statistics stopped")
        self.stats_run = False

    @staticmethod
    def update_label(status_text):
        Label(frame, text="Status: " + status_text, fg="#C0C0C0", bg='#303030').place(x=130, y=320)

    def read_statistics(self, value):
        def read_owlbot():
            """Reads temperature and wind speed"""
            print("Reading statistics from Owlbot into file owlbot_stats.csv\n")

            with open('owlbot_stats.csv', newline='', mode='w') as stats_file:
                fieldnames = ['Time in seconds', 'Trunk temp', 'Branch temp']
                stats_writer = csv.writer(stats_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                stats_writer.writerow(fieldnames)

                time_stamp_str = ""
                self.stats_run = True
                reading_count = 0

                while self.stats_run:

                    if not self.stats_run:
                        break

                    date_time_obj = datetime.now()
                    time_stamp_str_new = date_time_obj.strftime("%H:%M:%S")

                    if time_stamp_str_new != time_stamp_str:
                        response = requests.get(url, params={
                            'value': str(value),
                            'token': token
                        })

                        data = response.json()

                        time_stamp_str = time_stamp_str_new
                        reading_count += 1
                        printable_text = f'{reading_count}: TT: {data[0][6]} BT: {data[1][6]} TW: {data[2][6]} ' \
                                         f'BW: {data[3][6]}'

                        if self.stats_run:
                            self.update_label(printable_text)
                            print(printable_text)
                            stats_writer.writerow([reading_count, data[0][6], data[1][6]])

        Thread(target=read_owlbot).start()


root = tk.Tk()

root.title("Owlbot Python GUI")
root.iconbitmap('owlbot.ico')
root.config(bg="red")

camera = Camera()
statistics = Statistics()

frame = tk.Canvas(root, width=640, height=480)
frame.pack_propagate(False)

frame.config(bg='#303030')

token_label = Label(frame, text="Token", fg="white", bg='#303030').place(x=20, y=50)
camera_position_label = Label(frame, text="Camera position", fg="white", bg='#303030').place(x=20, y=120)
statistics_label = Label(frame, text="Statistics", fg="white", bg='#303030').place(x=20, y=290)


entry_token = Entry(root).place(x=72, y=51)
token_button = tk.Button(frame, text="Set", fg='black',  bg="#F0F0F0",
                         command=lambda: camera.set_token(entry_token.get())).place(x=210, y=49)
stop_stats_button = tk.Button(frame, text="Stop", fg='black',  bg="#F0F0F0",
                              command=lambda: statistics.stop()).place(x=130, y=380)

image_background = Image.open("Owlbot.jpg")
image_button = image_background.resize((120, 95))
image_for_button = ImageTk.PhotoImage(image_button)
camera_owl = tk.Button(frame, text="", image=image_for_button, compound="left",
                       command=lambda: camera.move_camera(4, 145, 62))
camera_owl.place(x=20, y=150)

image_eliot = Image.open("Eliot.png")
image_for_eliot = image_eliot.resize((85, 95))
eliot_image = ImageTk.PhotoImage(image_for_eliot)
camera_eliot = tk.Button(frame, text="", image=eliot_image, compound="left",
                         command=lambda: camera.move_camera(4, 95, 80))
camera_eliot.place(x=170, y=150)

image_chirpy = Image.open("Chirpy.png")
image_for_chirpy = image_chirpy.resize((105, 95))
chirpy_image = ImageTk.PhotoImage(image_for_chirpy)
camera_chirpy = tk.Button(frame, text="", image=chirpy_image, compound="left",
                          command=lambda: camera.move_camera(4, 55, 63))
camera_chirpy.place(x=280, y=150)

image_mat = Image.open("Mat.png")
image_for_mat = image_mat.resize((80, 95))
mat_image = ImageTk.PhotoImage(image_for_mat)
camera_mat = tk.Button(frame, text="", image=mat_image, compound="left",
                       command=lambda: camera.move_camera(4, 34, 56))
camera_mat.place(x=415, y=150)

image_howard = Image.open("Howard.png")
image_for_howard = image_howard.resize((95, 120))
howard_image = ImageTk.PhotoImage(image_for_howard)
camera_howard = tk.Button(frame, text="", image=howard_image, compound="left",
                          command=lambda: camera.move_camera(4, 16, 57))
camera_howard.place(x=520, y=150)

image_stats = Image.open("stats.png")
image_for_stats = image_stats.resize((95, 95))
stats_image = ImageTk.PhotoImage(image_for_stats)
get_stats = tk.Button(frame, text="", image=stats_image, compound="left",
                      command=lambda: statistics.read_statistics(5))
get_stats.place(x=20, y=320)
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
