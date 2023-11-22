import tkinter as tk
from tkinter import colorchooser
import colorsys
from tkinter import Scale, StringVar


def cmyk2rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return r, g, b


def rgb2cmyk(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255
    k = 1 - max(r, g, b)
    if k == 1:
        c = m = y = 0
    else:
        c = (1 - r - k) / (1 - k)
        m = (1 - g - k) / (1 - k)
        y = (1 - b - k) / (1 - k)
    return c, m, y, k


def rgb2hls(r, g, b):
    r = r / 255
    g = g / 255
    b = b / 255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    h = h * 360
    l = l * 100
    s = s * 100
    return h, l, s


def hls2rgb(h, l, s):
    h = h / 360
    l = l / 100
    s = s / 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    r = r * 255
    g = g * 255
    b = b * 255
    return r, g, b


def hex2rgb(color):
    color = color.lstrip('#')
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Colors")

        self.cmyk_labels = []
        self.rgb_labels = []
        self.hls_labels = []

        self.input_type_var = StringVar()
        self.input_sliders = []

        self.create_color_inputs()
        self.create_color_labels()

        self.root.mainloop()

        self.r = 0
        self.g = 0
        self.b = 0
        self.h = 0
        self.l = 0
        self.s = 0
        self.c = 0
        self.m = 0
        self.y = 0
        self.k = 0

    def create_color_inputs(self):
        input_type_frame = tk.Frame(self.root)
        input_type_frame.pack()
        input_type_label = tk.Label(input_type_frame, text="Input Type")
        input_type_label.grid(row=0, column=0)
        input_type_dropdown = tk.OptionMenu(input_type_frame, self.input_type_var, "CMYK", "RGB", "HLS",
                                            command=self.update_input_type)
        input_type_dropdown.grid(row=0, column=1)

        slider_frame = tk.Frame(self.root)
        slider_frame.pack(side=tk.LEFT)

        for i in range(4):
            self.input_sliders.append(Scale(slider_frame, from_=0, to=255, length=256, orient=tk.HORIZONTAL,
                                            command=self.update_slider_value))
            self.input_sliders[i].pack()

    def create_color_labels(self):
        labels_frame = tk.Frame(self.root)
        labels_frame.pack(side=tk.BOTTOM)

        cmyk_frame = tk.Frame(labels_frame)
        cmyk_frame.grid(row=0, column=0, padx=10)
        cmyk_label = tk.Label(cmyk_frame, text="CMYK:")
        cmyk_label.pack()
        for i in range(4):
            label = tk.Label(cmyk_frame, text="")
            label.pack()
            self.cmyk_labels.append(label)

        rgb_frame = tk.Frame(labels_frame)
        rgb_frame.grid(row=0, column=1, padx=10)
        rgb_label = tk.Label(rgb_frame, text="RGB:")
        rgb_label.pack()
        for i in range(3):
            label = tk.Label(rgb_frame, text="")
            label.pack()
            self.rgb_labels.append(label)

        hls_frame = tk.Frame(labels_frame)
        hls_frame.grid(row=0, column=2, padx=10)
        hls_label = tk.Label(hls_frame, text="HLS:")
        hls_label.pack()
        for i in range(3):
            label = tk.Label(hls_frame, text="")
            label.pack()
            self.hls_labels.append(label)

        palette_button = tk.Button(labels_frame, text="Sliders", command=self.choose_color)
        palette_button.grid(row=0, column=3, padx=10)

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.r, self.g, self.b = hex2rgb(color)
            self.c, self.m, self.y, self.k = rgb2cmyk(self.r, self.g, self.b)
            self.h, self.l, self.s = rgb2hls(self.r, self.g, self.b)
            self.r, self.g, self.b, self.h, self.l, self.s = round(self.r), round(self.g), round(self.b), round(
                self.h), round(self.l), round(self.s)
            self.set_background_color(self.r, self.g, self.b)
            self.update_cmyk_labels(self.c, self.m, self.y, self.k)
            self.update_rgb_labels(self.r, self.g, self.b)
            self.update_hls_labels(self.h, self.l, self.s)
            input_type = self.input_type_var.get()
            if input_type == "RGB":
                self.set_slider_values(self.r, self.g, self.b)
            elif input_type == "HLS":
                self.set_slider_values(self.h, self.l, self.s)
            else:
                self.set_slider_values(self.c * 100, self.m * 100, self.y * 100, self.k * 100)

    def set_slider_values(self, *varg):
        for i in range(len(varg)):
            self.input_sliders[i].set(varg[i])

    def update_input_type(self, event):
        input_type = self.input_type_var.get()
        if input_type == "CMYK":
            self.set_slider_conf(0, 100)
            self.input_sliders[3].pack()
            self.set_slider_values(self.c * 100, self.m * 100, self.y * 100, self.k * 100)
        elif input_type == "RGB":
            self.set_slider_conf(0, 255)
            self.input_sliders[3].pack_forget()
            self.set_slider_values(self.r, self.g, self.b)
        elif input_type == "HLS":
            self.set_slider_conf(0, 100)
            self.input_sliders[0].configure(from_=0, to=359)
            self.input_sliders[3].pack_forget()
            self.set_slider_values(self.h, self.l, self.s)

    def set_slider_conf(self, from__, to__):
        for i in range(4):
            self.input_sliders[i].configure(from_=from__, to=to__)

    def update_slider_value(self, value):
        input_type = self.input_type_var.get()
        if input_type == "CMYK":
            self.update_cmyk(None)
        elif input_type == "RGB":
            self.update_rgb(None)
        elif input_type == "HLS":
            self.update_hls(None)

    def update_cmyk(self, event):
        try:
            input_value = [int(slider.get()) / 100 for slider in self.input_sliders]
            if self.input_type_var.get() == "CMYK":
                self.c, self.m, self.y, self.k = input_value
                self.r, self.g, self.b = cmyk2rgb(self.c, self.m, self.y, self.k)
                self.h, self.l, self.s = rgb2hls(self.r, self.g, self.b)
                self.r, self.g, self.b, self.h, self.l, self.s = round(self.r), round(self.g), round(self.b), round(
                    self.h), round(self.l), round(self.s)
                self.set_background_color(self.r, self.g, self.b)
                self.update_cmyk_labels(self.c, self.m, self.y, self.k)
                self.update_rgb_labels(self.r, self.g, self.b)
                self.update_hls_labels(self.h, self.l, self.s)
        except ValueError:
            pass

    def update_rgb(self, event):
        try:
            input_value = [int(slider.get()) for slider in self.input_sliders[:-1]]
            if self.input_type_var.get() == "RGB":
                self.r, self.g, self.b = input_value
                self.c, self.m, self.y, self.k = rgb2cmyk(self.r, self.g, self.b)
                self.h, self.l, self.s = rgb2hls(self.r, self.g, self.b)
                self.r, self.g, self.b, self.h, self.l, self.s = round(self.r), round(self.g), round(self.b), round(
                    self.h), round(self.l), round(self.s)
                self.set_background_color(self.r, self.g, self.b)
                self.update_cmyk_labels(self.c, self.m, self.y, self.k)
                self.update_rgb_labels(self.r, self.g, self.b)
                self.update_hls_labels(self.h, self.l, self.s)
        except ValueError:
            pass

    def update_hls(self, event):
        try:
            input_value = [int(slider.get()) for slider in self.input_sliders[:-1]]
            if self.input_type_var.get() == "HLS":
                self.h, self.l, self.s = input_value
                self.r, self.g, self.b = hls2rgb(self.h, self.l, self.s)
                self.c, self.m, self.y, self.k = rgb2cmyk(self.r, self.g, self.b)
                self.r, self.g, self.b, self.h, self.l, self.s = round(self.r), round(self.g), round(self.b), round(
                    self.h), round(self.l), round(self.s)
                self.set_background_color(self.r, self.g, self.b)
                self.update_cmyk_labels(self.c, self.m, self.y, self.k)
                self.update_rgb_labels(self.r, self.g, self.b)
                self.update_hls_labels(self.h, self.l, self.s)
        except ValueError:
            pass

    def update_cmyk_labels(self, c, m, y, k):
        labels = self.cmyk_labels
        labels[0].configure(text=f"C: {c:.2f}")
        labels[1].configure(text=f"M: {m:.2f}")
        labels[2].configure(text=f"Y: {y:.2f}")
        labels[3].configure(text=f"K: {k:.2f}")

    def update_rgb_labels(self, r, g, b):
        labels = self.rgb_labels
        labels[0].configure(text=f"R: {r}")
        labels[1].configure(text=f"G: {g}")
        labels[2].configure(text=f"B: {b}")

    def update_hls_labels(self, h, l, s):
        labels = self.hls_labels
        labels[0].configure(text=f"H: {h}")
        labels[1].configure(text=f"L: {l}")
        labels[2].configure(text=f"S: {s}")

    def set_background_color(self, r, g, b):
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        self.root.configure(background=hex_color)


if __name__ == "__main__":
    app = App()
