# For tutorial on JSON request see https://realpython.com/python-requests/

import requests
import time
import tkinter as tk

url = 'https://prenaud-raspi.dynamic-dns.net/input'
token = 'Eliot'


def verify_dict(data):
    """Returns True if data is of type dict, otherwise returns False"""
    if type(data) is dict:
        print("Error: data was not a dict, was instead {}".format(type(data)))
        return True
    else:
        return False


def MoveCameraOwl():
    print("Camera: move to OWL")
    value = 4
    xValue = 147
    zValue = 66

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
    time.sleep(5)


def MoveCameraLight():
    print("Camera: move to Howard")
    value = 4
    xValue = 16
    zValue = 57

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
    time.sleep(5)


root = tk.Tk()

frame = tk.Frame(root, width=320, height=240)
frame.pack_propagate(False)

button = tk.Button(frame,
                   text="Quit",
                   fg="dark green",
                   command=quit)
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
