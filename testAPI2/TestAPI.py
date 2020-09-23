# For tutorial on JSON request see https://realpython.com/python-requests/

import requests
import tkinter as tk
import time
from threading import Thread

url = 'https://prenaud-raspi.dynamic-dns.net/input'
token = 'Eliot'
is_cam_movable = True


def verify_dict(data):
    """Returns True if data is of type dict, otherwise returns False"""
    if type(data) is dict:
        return True
    else:
        print("Error: data was not a dict, was instead {}".format(type(data)))
        return False


def five_sec_timer():
    time.sleep(5)
    global is_cam_movable
    is_cam_movable = True


def MoveCameraOwl():
    print("Camera: move to OWL")
    global is_cam_movable
    value = 4
    xValue = 147
    zValue = 66

    if not is_cam_movable:
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
    if not verify_dict(data):
        return

    # Print the data
    print(data)
    is_cam_movable = False
    Thread(target=five_sec_timer).start()


def MoveCameraLight():
    print("Camera: move to Howard")
    global is_cam_movable
    value = 4
    xValue = 16
    zValue = 57

    if not is_cam_movable:
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
    if not verify_dict(data):
        return

    # Print the data
    print(data)
    is_cam_movable = False
    Thread(target=five_sec_timer).start()


root = tk.Tk()

frame = tk.Frame(root, width=320, height=240)
frame.pack_propagate(False)

button = tk.Button(frame, text="Quit", fg="dark green", command=quit)
button.pack(side=tk.LEFT)

Camera_OWL = tk.Button(frame, text="OWL", command=MoveCameraOwl)
Camera_OWL.pack(side=tk.RIGHT)

Camera_LIGHT = tk.Button(frame, text="Howard", command=MoveCameraLight)
Camera_LIGHT.pack(side=tk.RIGHT)

frame.pack()
root.mainloop()

# if response.status_code == 200:
#    print('Success!')
# elif response.status_code == 404:
#    print('Not Found.')
