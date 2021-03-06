import telebot
from telebot import types
import torch
from conv_nnet import ClassificationConvNet, crop_borders
from pytorch_nn import ClassificationNet, compute_new_sample
import json
import aiml
import cv2
import numpy as np
from miniclips import Miniclips
import albumentations as A


def _set_properties(k):
    with open("standard/bot.config", 'r', encoding='utf-8') as f:
        for line in f:
            name, value = line.split('=')
            value = value.strip()
            k.setBotPredicate(name, value)


bot = telebot.TeleBot('5062128956:AAF9hNqI3LnLhi4E7Rbv-8p91DI5Mryw_ic')

## NNet
#model = ClassificationConvNet()
model = ClassificationNet(hidden_dims=[128, 64])
model.load_state_dict(torch.load("GREEK_net.pth", map_location=torch.device('cpu')))
model.eval()
with open('labels2names.json', 'r', encoding='utf-8') as f:
    labels2names = json.load(f)
output_activation = torch.nn.Softmax(dim=0)

##Clips
CLIPS_FLAG = False
clipsModel = Miniclips('data/facts.txt', 'data/productions.txt', 'book.clp')

## aiml
k = aiml.Kernel()
_set_properties(k)
k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")


@bot.message_handler(content_types=['photo'])
def photo(message):
    raw = message.photo[2].file_id
    name = raw + ".jpg"
    file_info = bot.get_file(raw)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(name, 'wb') as new_file:
        new_file.write(downloaded_file)
    image = cv2.cvtColor(cv2.imread(name), cv2.COLOR_BGR2GRAY)
    image[image <= 98] = 1
    image[image > 98] = 0
    image = crop_borders(image)

    transform =  A.Compose([
            A.Downscale(p=0.3),
            A.GaussianBlur(p=0.5),
            A.Resize(400, 400),
        ])

    #t = torch.unsqueeze(transform(image=image)["image"].float(), 0)
    t = torch.from_numpy(np.array(compute_new_sample(transform(image=image)["image"]))).float()
    outputs = model(t)
    print(outputs)
    preds = torch.argmax(output_activation(outputs), dim=0)
    print(preds)
    letter = labels2names[str(preds.item())]
    answer = "Думаю, это %s" % letter
    k.respond("тлен букве %s" % letter)
    bot.send_message(message.chat.id, answer)


@bot.message_handler(commands=["start"])
def start(m):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Книги")
    markup.add(item1)
    bot.send_message(m.chat.id,
                     'Добрый день, %s' % m.from_user.first_name +
                     '\nЯ самый лучший бот мира, написанный на божественном языке - Python' +
                     '\nМогу порекоммендовать книгу по Вашим предпочтениям - нажмите на кнопку книги\n' +
                     '\nМогу распознать 10 букв греческого алфавита - отправьте фото' +
                     '\nМогу просто поболтать(в основном на английском) - наберите сообщение',
                     reply_markup=markup)

@bot.message_handler(commands=["return"])
def start(m):
    global CLIPS_FLAG
    CLIPS_FLAG = False

@bot.message_handler(content_types=["text"])
def handle_text(message):
    global CLIPS_FLAG
    if message.text.strip() == 'Книги':
        CLIPS_FLAG = True
        answer = clipsModel.message()
    else:
        human_input = message.text.strip()
        if CLIPS_FLAG:
            answer = clipsModel.proceed(human_input)
        else:
            answer = k.respond(human_input)
    bot.send_message(message.chat.id, answer)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
