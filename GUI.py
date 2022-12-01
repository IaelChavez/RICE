import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog

import customtkinter
import cv2
from PIL import Image, ImageTk

TKINTER_WIDGETS = {}

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
CONFIG_DIRECTORY = os.path.join(CURRENT_DIRECTORY, "Config")
IMAGES_DIRECTORY = os.path.join(CONFIG_DIRECTORY, "Images")

class App(customtkinter.CTk):
    global TKINTER_WIDGETS

    WIDTH = 1385
    HEIGHT = 720

    def __init__(self):
        super().__init__()

        self.title("Analisis de Arroz")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Opciones",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Abrir Archivo",
                                                command=self.select_image)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Abrir Camara",
                                                command=self.button_event)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Modo:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Dark", "Light"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.label_2 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Imagen Original",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_2.grid(row=0, column=0, pady=5, padx=5)

        img = Image.open(os.path.join(IMAGES_DIRECTORY, "fondo.png"))
        img_resized = img.resize((700, 500))
        img = ImageTk.PhotoImage(img_resized)

        TKINTER_WIDGETS['label_img'] = customtkinter.CTkLabel(master=self.frame_right, image=img)
        TKINTER_WIDGETS['label_img'].image = img
        TKINTER_WIDGETS['label_img'].grid(row=1, column=0, padx=10, pady=10)


        self.label_3 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Imagen Analizada",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_3.grid(row=0, column=1, pady=5, padx=5)

        img2 = Image.open(os.path.join(IMAGES_DIRECTORY, "fondo.png"))
        img_resized2 = img2.resize((700, 500))
        img2 = ImageTk.PhotoImage(img_resized2)

        TKINTER_WIDGETS['label_img'] = customtkinter.CTkLabel(master=self.frame_right, image=img2)
        TKINTER_WIDGETS['label_img'].image = img2
        TKINTER_WIDGETS['label_img'].grid(row=1, column=1, padx=10, pady=10)

        self.label_4 = customtkinter.CTkLabel(master=self.frame_right,
                                              text="Numero de Objetos: ",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_4.grid(row=2, column=1, pady=5, padx=5)

        # set default values
        self.optionmenu_1.set("Dark")

    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def select_image(self):
        path = filedialog.askopenfilename()
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (11, 11), 0)
        canny = cv2.Canny(blur, 35, 70)
        dilated = cv2.dilate(canny, (1, 1), iterations=0)
        cnt, hierarchy = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        rgb2 = cv2.drawContours(rgb, cnt, -1, (0, 255, 0), 2)

        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)

        rgb2 = Image.fromarray(rgb2)
        rgb2 = ImageTk.PhotoImage(rgb2)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()