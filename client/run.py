from PIL import ImageGrab, Image
import os
import io
import time
import exrex
import requests
import base64

# GTK Imports
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

SERVER_ADDRESS = os.environ.get('SERVER_ADDRESS', 'http://hahascreenshotsgoburrrr.xyz')


def main():
    def upload_screenshot(app):
        b64ss = takeScreenshot()

        r = requests.post(
            '{}/upload'.format(SERVER_ADDRESS), 
            json={'image': b64ss})
        
        if 300 > r.status_code > 199:
            res = r.json()
            return "{}/get/{}".format(SERVER_ADDRESS, res.get('slug', ''))
        raise Exception()

    def on_active(app):
        win = Gtk.ApplicationWindow(application=app)
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)

        grid = Gtk.Grid()

        label = Gtk.Label(label="SCREENSHOTS GO BURRRR\nYOU HAVE NEVER SEEN SCREENSHOTS BURRRR LIKE THIS EVER BEFORE!")

        btn = Gtk.Button(label="Take Screenshot")
        btn.connect('clicked', lambda x: clipboard.set_text(upload_screenshot(app), -1))

        # Adding elements to the grid
        grid.attach(label, 0, 0, 1, 1)
        grid.attach(btn, 0, 1, 1, 1)

        grid.set_margin_top(10)
        grid.set_margin_left(10)
        grid.set_margin_right(10)
        grid.set_margin_bottom(10)

        label.set_margin_bottom(10)

        win.add(grid)
        win.show_all()

    app = Gtk.Application(application_id = 'com.imagebin.ScreenshotUtil')
    app.connect('activate', on_active)
    app.run(None)


def takeScreenshot():
    mem_file = io.BytesIO()

    img = ImageGrab.grab()
    img.save(mem_file, format="PNG")

    mem_file.seek(0)
    img_bytes = mem_file.read()

    base64_encoded_img = base64.b64encode(img_bytes)
    base64_encoded_img_string = base64_encoded_img.decode('ascii')

    return base64_encoded_img_string


if __name__ == "__main__":
    main()
