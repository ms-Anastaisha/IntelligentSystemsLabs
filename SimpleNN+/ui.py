from tkinter import *
import re
from typing import Union
from PIL import ImageTk, Image

from dataset import crop_borders, compute_sample
from numpy_nn import NNet
from pytorch_nn import NetWrapper
import cv2
import time

NET_OPTIONS = ["numpy handmade", "pytorch"]
NORMAL_MESSAGE = "Ready to work!"
ERROR_ARCHITECTURE = "ERROR! \nNetwork architecture \n should contain \n from 1 to 3 layers,\n and" \
                     "\nfrom 20 to 2000 neurons"
ERROR_EPOCH = "ERROR! \nEpoch num \n should be \n greater than 0 \n and less than 101"
NET_CREATED = "Neural network created!"
TRAINING_FINISHED = "Training finished!"
ERROR_NOT_CREATED = "ERROR! \n First you need \nto create\n and train \nneural network!"


class NeuralNetworkUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Нейронная сеть")
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='imgs/neural.png'))

        image_placeholder = ImageTk.PhotoImage(Image.open('imgs/placeholder.png'))

        ## labels
        net_label = Label(text="Net type", fg="#333")
        net_architecture_label = Label(text="Net architecture", fg="#333")
        net_epoch_label = Label(text="Epoch count", fg="#333")
        net_label.grid(row=0, column=2, sticky="N")
        net_architecture_label.grid(row=0, column=2)
        net_epoch_label.grid(row=0, column=2, sticky="S")
        self.user_message = Label(text="Ready to work", fg="#333")
        self.user_message.grid(row=2, column=2, columnspan=2, sticky="N")

        ## camera
        self.cap = cv2.VideoCapture(1)
        self.camera_input = Label(image=image_placeholder)
        self.camera_processed = Label(image=image_placeholder)
        self.camera_input.grid(column=0, row=0, rowspan=3)
        self.camera_processed.grid(column=1, row=0, rowspan=3)

        ## choice of network type
        self.net_choice = StringVar(self.window)
        self.net_choice.set(NET_OPTIONS[1])
        net_choice_menu = OptionMenu(self.window, self.net_choice, *NET_OPTIONS)
        net_choice_menu.grid(row=0, column=3, sticky="N")

        ## get architecture
        self.architecture_string = StringVar()
        architecture_input = Entry(self.window, textvariable=self.architecture_string)
        architecture_input.grid(row=0, column=3)

        ## get number of epochs
        self.epoch_string = StringVar()
        epoch_input = Entry(self.window, textvariable=self.epoch_string)
        epoch_input.grid(row=0, column=3, sticky="S")

        ## control buttons
        self.train_button = Button(self.window, text="Create", width=15, command=self._create)
        self.create_button = Button(self.window, text="Train", width=15, command=self._train)
        self.test_button = Button(self.window, text="Test", width=15, command=self._test)
        self.predict_button = Button(self.window, text="Predict", width=15, command=self._predict)
        self.camera_on_button = Button(self.window, text="Camera on", width=15, command=self._camera_on)
        self.camera_off_button = Button(self.window, text="Camera off", width=15, command=self._camera_off)

        self.train_button.grid(row=1, column=3, sticky="N")
        self.create_button.grid(row=1, column=2, sticky="N")
        self.test_button.grid(row=1, column=2)
        self.predict_button.grid(row=1, column=3)
        self.camera_on_button.grid(row=1, column=2, sticky="S")
        self.camera_off_button.grid(row=1, column=3, sticky="S")

        ## parameters
        self.model = None
        self.error = False
        self.camera_stop = False
        self.test_image = None
        self.train_flag = False

        self.window.mainloop()

    def _parse_architecture(self) -> Union[None, list]:
        architecture = self.architecture_string.get()
        hidden_layers_strings = architecture.split(";")
        hidden_layers = []
        if len(hidden_layers_strings) > 3:
            return None
        for hid in hidden_layers_strings:
            if re.match('^[0-9]+$', hid) is None:
                return None
            value = int(hid)
            if value < 20 or value > 2000:
                return None
            hidden_layers.append(value)
        return hidden_layers

    def _parse_epoch_num(self) -> Union[None, int]:
        val = self.epoch_string.get()
        flag = re.match('^[0-9]+$', val) is not None
        if flag:
            epoch_num = int(val)
            if 0 < epoch_num < 101:
                return epoch_num
        return None

    def _clear_text(self, entry) -> None:
        entry.delete(0, 'end')

    def _train(self) -> None:
        if self.error:
            self.error = False
            self.user_message.config(text=NORMAL_MESSAGE, fg="#333")
        if self.model is None:
            self.user_message.config(text=ERROR_NOT_CREATED, fg="#f00")
            self.error = True
            return
        epoch_num = self._parse_epoch_num()
        if epoch_num is None:
            self.error = True
            self.user_message.config(text=ERROR_EPOCH, fg="#f00")
            return
        start = time.time()
        for train_stats in self.model.train(epoch_num):
            print(train_stats)
            self.user_message.config(text=train_stats, fg="#07f")
            self.window.update()

        end = time.time() - start
        self.user_message.config(text=TRAINING_FINISHED + "\n Time elapsed: %.3f s" % end, fg="#00f")
        self.train_flag = True

    def _test(self) -> None:
        if self.error:
            self.error = False
            self.user_message.config(text=NORMAL_MESSAGE, fg="#333")
        if self.model is None or not self.train_flag:
            self.user_message.config(text=ERROR_NOT_CREATED, fg="#f00")
            self.error = True
            return
        test_result = self.model.test()
        self.user_message.config(text=test_result, fg="#07f")

    def _create(self) -> None:
        if self.error:
            self.error = False
            self.user_message.config(text=NORMAL_MESSAGE, fg="#333")
        self.train_flag = False
        architecture_type = self.net_choice.get()
        architecture = self._parse_architecture()
        if architecture is None:
            self.error = True
            self.user_message.config(text=ERROR_ARCHITECTURE, fg="#f00")
            return
        if architecture_type == NET_OPTIONS[0]:
            self.model = NNet(architecture)
        else:
            self.model = NetWrapper(architecture)
        self.user_message.config(text=NET_CREATED, fg="#00f")

    def _predict(self):
        if self.error:
            self.error = False
            self.user_message.config(text=NORMAL_MESSAGE, fg="#333")
        if self.model is None or not self.train_flag:
            self.user_message.config(text=ERROR_NOT_CREATED, fg="#f00")
            self.error = True
            return
        test_sample = compute_sample(self.test_image)
        prediction = self.model.predict(test_sample)
        self.user_message.config(text=prediction, fg="#07f")

    def _preprocess(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image[image <= 98] = 1
        image[image > 98] = 0

        image_bordered = crop_borders(image)
        if image_bordered.shape[0] > 100 and image_bordered.shape[1] > 100:
            image = image_bordered
        image = cv2.resize(image, (400, 400))
        image *= 255
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        cell_width, cell_height = 20, 20
        for i in range(image.shape[1] // cell_width + 1):
            image = cv2.line(image, (0, (i + 1) * cell_width), (image.shape[0], (i + 1) * cell_width), [255, 0, 0],
                             thickness=2)

        for j in range(image.shape[0] // cell_height + 1):
            image = cv2.line(image, ((j + 1) * cell_height, 0), ((j + 1) * cell_height, image.shape[1]), [255, 0, 0],
                             thickness=2)

        return image

    def _camera_on(self):
        self.camera_stop = False
        self.show_frame()

    def show_frame(self):
        ret, frame = self.cap.read()
        i = 0
        while not ret:
            ret, frame = self.cap.read()
            i += 1
            if i == 100:
                return
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        preprocessed = self._preprocess(frame)
        self.test_image = preprocessed
        img = Image.fromarray(cv2image)
        preprocessed_img = Image.fromarray(preprocessed)
        imgtk = ImageTk.PhotoImage(image=img)
        preprocessed_imgtk = ImageTk.PhotoImage(image=preprocessed_img)
        self.camera_input.imgtk = imgtk
        self.camera_processed.imgtk = preprocessed_imgtk
        self.camera_input.configure(image=imgtk)
        self.camera_processed.configure(image=preprocessed_imgtk)
        if not self.camera_stop:
            self.camera_input.after(10, self.show_frame)

    def _camera_off(self):
        self.camera_stop = True


if __name__ == '__main__':
    nnUI = NeuralNetworkUI()
