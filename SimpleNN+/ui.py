from tkinter import *
import re
from typing import Union
from PIL import ImageTk, Image

from numpy_nn import NNet
from pytorch_nn import NetWrapper

NET_OPTIONS = ["numpy handmade", "pytorch"]
NORMAL_MESSAGE = "Ready to work!"
ERROR_ARCHITECTURE = "ERROR! \nNetwork architecture \n should contain \n from 1 to 3 layers,\n and" \
                     "\nfrom 20 to 2000 neurons"
ERROR_EPOCH = "ERROR! \nEpoch num \n should be \n greater than 0 \n and less than 101"
NET_CREATED = "Neural network created!"
TRAINING_FINISHED = "Training finished!"


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
        self.train_button.grid(row=1, column=3, sticky="N")
        self.create_button.grid(row=1, column=2, sticky="N")
        self.test_button.grid(row=1, column=3)
        self.predict_button.grid(row=1, column=2)

        ## parameters
        self.model = None
        self.error = False

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
        epoch_num = self._parse_epoch_num()
        if epoch_num is None:
            self.error = True
            self.user_message.config(text=ERROR_EPOCH, fg="#f00")
            return
        for train_stats in self.model.train(epoch_num):
            self.user_message.config(text=train_stats, fg="#0f0")
        self.user_message.config(text=TRAINING_FINISHED, fg="#00f")

    def _test(self) -> None:
        test_result = self.model.test()
        self.user_message.config(text=test_result, fg="#0f0")

    def _create(self) -> None:
        if self.error:
            self.error = False
            self.user_message.config(text=NORMAL_MESSAGE, fg="#333")
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
        ...


if __name__ == '__main__':
    nnUI = NeuralNetworkUI()
