import requests
import pandas as pd
import re
import argparse
import tkinter as tk
from tkinter.filedialog import askopenfilename
import json

class TelegramBot():

    def __init__(self) -> None:
        arg = self.parseArgs()
        self.get_input(arg)
        self.tinker_tab()

    def parseArgs(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("--configJson", required = True, help = "path to config JSON")
        args = vars(ap.parse_args())
        return args

    def get_input(self, args):
        if not args["configJson"]:
            raise Exception("Please provide config Json file path")

        jsonFile = open(args["configJson"], "r")
        data = json.load(jsonFile)
        self.token = data["token"]

    def broadcast_msg(self, chanList, msg):
        for channelID in chanList:
            to_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML'.format(self.token, channelID, msg)
            requests.get(to_url)

    def clean(self, txt):
        txt = re.sub(r"&", "and", txt)
        txt = re.sub("\'s", " is", txt)
        txt = re.sub("\'re", " are", txt)
        txt = re.sub("\'t", " not" , txt)
        return txt

    def UploadAction(self, event=None):
        filename = askopenfilename()
        print('Selected:', filename[-4:])
        if filename[-3:] == "txt":
            # Change text of label
            self.label1['text'] = filename
        elif filename[-4:] == "xlsx":
            self.label2['text'] = filename

    def SendToGroups(self):
        # groups data
        df = pd.read_excel(self.label2['text'])
        channelList = list(df['ChannelID'])

        # read the text file
        with open(self.label1['text'], 'r', encoding="utf8") as file:
            msg = file.read()
        msg = self.clean(msg)
        if len(msg)>=4000:
            self.label4['text'] = "The post is too large! Kindly divide it into two msgs."
        else:
            self.broadcast_msg(channelList, msg)

    def tinker_tab(self):
        root= tk.Tk()
        button1 = tk.Button(text='Select text file', command=self.UploadAction, bg='brown', fg='white')
        button1.pack(padx=2, pady=5)
        self.label1 = tk.Label(text='Please choose a text file with post content in it')
        self.label1.pack(padx=2, pady=2)

        button2 = tk.Button(text='Select excel file', command=self.UploadAction, bg='brown', fg='white')
        button2.pack(padx=2, pady=5)
        self.label2 = tk.Label(text='Please choose an excel file with Group details')
        self.label2.pack(padx=2, pady=2)

        label0 = tk.Label(text='')
        label0.pack(padx=2, pady=2)

        button4 = tk.Button(text='Send to all Groups', command=self.SendToGroups, bg='brown', fg='white')
        button4.pack(padx=2, pady=5)
        self.label4 = tk.Label(text='Send the post to all Groups')
        self.label4.pack(padx=2, pady=2)

        root.geometry("500x300")
        root.mainloop()

if __name__ == "__main__":
# python .\telegram_bot.py --configJson ./inputs/config.json
    obj = TelegramBot()

