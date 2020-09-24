# For tutorial on JSON request see https://realpython.com/python-requests/

import requests
import tkinter as tk
import time
from threading import Thread

url = 'https://prenaud-raspi.dynamic-dns.net/input'
token = 'Eliot'
is_cam_movable = True


class Camera:
    def __init__(self):
        self.is_cam_movable = True

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


root = tk.Tk()
camera = Camera()

frame = tk.Frame(root, width=320, height=240)
frame.pack_propagate(False)

button = tk.Button(frame, text="Quit", fg="dark green", command=quit)
button.pack(side=tk.LEFT)

Camera_OWL = tk.Button(frame, text="OWL",
                       command=lambda: camera.move_camera(4, 147, 66))
Camera_OWL.pack(side=tk.RIGHT)

Camera_LIGHT = tk.Button(frame, text="Howard",
                         command=lambda: camera.move_camera(4, 16, 57))
Camera_LIGHT.pack(side=tk.RIGHT)

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
