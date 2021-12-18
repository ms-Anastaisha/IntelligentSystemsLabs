from tkinter import *
from tkinter.font import Font
import aiml
import os


class ChatBotUI:
    def __init__(self):
        ## tkinter configuration
        self.window = Tk()
        self.window.title("Самый лучший чатбот мира(потому что на python)")
        self.window.tk.call('wm', 'iconphoto', self.window._w, PhotoImage(file='chatbot.png'))
        self.myFont = Font(family="Helvetica", size=14)
        self.window.resizable(False, False)
        self.window.bind('<Return>', self._send)

        ##aiml
        BRAIN_FILE = "brain.dump"
        self.k = aiml.Kernel()
        if os.path.exists(BRAIN_FILE):
            print("Loading from brain file: " + BRAIN_FILE)
            self.k.loadBrain(BRAIN_FILE)
        else:
            print("Parsing aiml files")
            self.k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
            print("Saving brain file: " + BRAIN_FILE)
            self.k.saveBrain(BRAIN_FILE)

        ## control buttons
        self.button_send = Button(self.window, text="Отправить", command=self._send, width=30,
                                  font=self.myFont)
        self.button_send.grid(column=1, row=1)

        ## texts outputs
        self.message = StringVar()
        self.message_input = Entry(self.window, textvariable=self.message, font=self.myFont, width=70)

        self._text = Text(self.window, height=30, width=100, font=self.myFont)
        self._text.config(bg="#F0F8FF", fg="#000")

        self._text.grid(column=0, row=0, columnspan=2)
        self.message_input.grid(row=1, column=0)

        self._text.configure(state="disabled")

        self.window.mainloop()

    def _send(self, event=None):
        human_input = self.message.get()
        self.message_input.delete(0, 'end')
        response = self.k.respond(human_input)
        self._text.configure(state="normal")
        self._text.insert(INSERT, "You: %s\n" % human_input)
        self._text.insert(INSERT, "Bot: %s\n" % response)
        self._text.configure(state="disabled")


if __name__ == '__main__':
    ChatBotUI()
