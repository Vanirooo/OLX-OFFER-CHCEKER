import requests
from time import sleep
import bs4
import customtkinter
from tkinter import *
from threading import Timer
import webbrowser
import http.client
import math

connect_timeout_s = 5

tag_indicies = []

class stopThreads:
    def globalv():
        global stopThread
        stopThread = False
    globalv()
    stopThread = stopThread

try:
    http.client._MAXHEADERS = 1000
    def handle(event):
        indextext = textbox.index("current")
        webbrowser.open(urlsFound[math.floor(float(indextext)) - 1])
    def search():
        global counter
        counter = 0
        if entry3.get() != None:
            connect_timeout_s = int(entry3.get())
        if entry.get() != None:
            url = 'https://www.olx.pl/d/oferty/q-' + entry.get() + '/?search%5Border%5D=created_at:desc'
        else:
            return
        if entry1.get() != None:
            price_choose = entry1.get()
        else:
            return
        if entry2.get() != None:
            keyword = entry2.get()
        else:
            o = 0
        if keyword != None:
            list1 = list(map(str, keyword.split()))
        isList = False
        global urlsFound
        urlsFound = []

        if len(list1) > 1:
            isList = True
        while True:
            if stopThreads.stopThread:
                textbox.delete('1.0', END)
                stopThreads.stopThread = False
                return
            req = requests.get(url)
            if req.status_code == 200:
            
                text = req.text
                text1 = ''
                text2 = 'https://www.olx.pl/d/oferta'        

                found = False

                indexes = []

                if keyword != '':
                    text2 = 'https://www.olx.pl/d/oferta'
                    soup = bs4.BeautifulSoup(text, 'html.parser')
                    if isList:
                        for keywrd in list1:
                            if text.__contains__(keywrd):
                                indexes.append(soup.find_all(lambda tag: tag.name == "h6" and keyword in tag.text))
                        for index1 in indexes:
                            if stopThreads.stopThread:
                                textbox.delete('1.0', END)
                                stopThreads.stopThread = False
                                return
                            found = False
                            text2 = 'https://www.olx.pl/d/oferta'
                            for indx in range(text.find(str(index1)) - 3500, text.find(str(index1))):
                                letter = text[indx]

                                if found:
                                    if letter == '"':
                                        break
                                    text2 += letter
                                else:
                                    text1 += letter
                                if text1.__contains__('/d/oferta'):
                                    text1 = ''
                                    found = True
                                if text1.__contains__('https://www.otomoto.pl'):
                                    text2 = 'https://www.otomoto.pl'
                                    text1 = ''
                                    found = True
                            test = requests.get(text2)
                            
                            if not urlsFound.__contains__(text2):
                                if test.status_code == 200:
                                    soup = bs4.BeautifulSoup(test.text, 'html.parser')
                                    if text2.__contains__('otomoto.pl'):
                                        priceSearch = soup.find('span', {"class": "offer-price__number"})
                                    else:
                                        priceSearch = soup.find('h3', {"class": "css-ddweki er34gjf0"})
                                    if priceSearch != None and not priceSearch.__contains__("Z"):
                                        price = priceSearch.text
                                        price1 = ''
                                        for i in price:
                                            if i == ' ':
                                                break
                                            price1 += i
                                            if price1.__contains__(' '):
                                                price1 = price1.replace(' ', '')
                                            if price1.__contains__(','):
                                                price1 = price1.replace(',', '.')
                                        price2 = float(price1)
                                        if round(float(price_choose)) >= price2:
                                            urlsFound.append(text2)
                                            counter += 1
                                            textbox.tag_config(f"hyper{counter}", foreground="lightblue", underline=1)
                                            textbox.tag_bind(f"hyper{counter}", "<Button-1>", handle)
                                            if text2.__contains__('otomoto.pl'):
                                                urlsFound.append(text2.replace('https://www.otomoto.pl/oferta/', '').replace('-', ' ').replace('.html', ''))
                                            else:
                                                textbox.insert(END, text2.replace('https://www.olx.pl/d/oferta/', '').replace('-', ' ').replace('.html', ''), tags=f'hyper{counter}')
                                            textbox.insert(END, text='\n')

                    else:
                        soup = bs4.BeautifulSoup(text, 'html.parser')
                        if text.__contains__(keyword):
                            indxes = soup.find_all(lambda tag: tag.name == "h6" and keyword in tag.text)
                            for index2 in indxes:
                                if stopThreads.stopThread:
                                    textbox.delete('1.0', END)
                                    stopThreads.stopThread = False
                                    return
                                found = False
                                text2 = 'https://www.olx.pl/d/oferta'
                                for indx in range(text.find(str(index2)) - 3500, text.find(str(index2))):
                                    letter = text[indx]

                                    if found:
                                        if letter == '"':
                                            break
                                        text2 += letter
                                    else:
                                        text1 += letter
                                    if text1.__contains__('/d/oferta'):
                                        text1 = ''
                                        found = True
                                    if text1.__contains__('https://www.otomoto.pl'):
                                        text2 = 'https://www.otomoto.pl'
                                        text1 = ''
                                        found = True
                                test = requests.get(text2)
                                
                                if not urlsFound.__contains__(text2):
                                    if test.status_code == 200:
                                        soup = bs4.BeautifulSoup(test.text, 'html.parser')
                                        if text2.__contains__('otomoto.pl'):
                                            priceSearch = soup.find('span', {"class": "offer-price__number"})
                                        else:
                                            priceSearch = soup.find('h3', {"class": "css-ddweki er34gjf0"})
                                        if priceSearch != None and not priceSearch.__contains__("Z"):
                                            price = priceSearch.text
                                            price1 = ''
                                            for i in price:
                                                if i == ' ':
                                                    break
                                                price1 += i
                                                if price1.__contains__(' '):
                                                    price1 = price1.replace(' ', '')
                                                if price1.__contains__(','):
                                                    price1 = price1.replace(',', '.')
                                            price2 = float(price1)
                                            if round(float(price_choose)) >= price2:
                                                urlsFound.append(text2)
                                                counter += 1
                                                textbox.tag_config(f"hyper{counter}", foreground="lightblue", underline=1)
                                                textbox.tag_bind(f"hyper{counter}", "<Button-1>", handle)
                                                if text2.__contains__('otomoto.pl'):
                                                    urlsFound.append(text2.replace('https://www.otomoto.pl/oferta/', '').replace('-', ' ').replace('.html', ''))
                                                else:
                                                    textbox.insert(END, text2.replace('https://www.olx.pl/d/oferta/', '').replace('-', ' ').replace('.html', ''), tags=f'hyper{counter}')
                                                textbox.insert(END, text='\n')
                else:
                    soup = bs4.BeautifulSoup(text, 'html.parser')
                    indxes = soup.find_all('h6', {"class":"css-16v5mdi er34gjf0"})
                    for index2 in indxes:
                        if stopThreads.stopThread:
                            textbox.delete('1.0', END)
                            stopThreads.stopThread = False
                            return
                        found = False
                        text2 = 'https://www.olx.pl/d/oferta'
                        for indx in range(text.find(str(index2)) - 3500, text.find(str(index2))):
                            letter = text[indx]

                            if found:
                                if letter == '"':
                                    break
                                text2 += letter
                            else:
                                text1 += letter
                            if text1.__contains__('/d/oferta'):
                                text1 = ''
                                found = True
                            if text1.__contains__('https://www.otomoto.pl'):
                                text2 = 'https://www.otomoto.pl'
                                text1 = ''
                                found = True
                        test = requests.get(text2)
                        if not urlsFound.__contains__(text2):
                            if test.status_code == 200:
                                soup = bs4.BeautifulSoup(test.text, 'html.parser')
                                if text2.__contains__('otomoto.pl'):
                                    priceSearch = soup.find('span', {"class": "offer-price__number"})
                                else:
                                    priceSearch = soup.find('h3', {"class": "css-ddweki er34gjf0"})
                                if priceSearch != None:
                                    price = priceSearch.text
                                    price1 = ''
                                    if priceSearch != None and not priceSearch.__contains__("Z"):
                                        for i in price:
                                            if i == ' ':
                                                break
                                            price1 += i
                                            if price1.__contains__(' '):
                                                price1 = price1.replace(' ', '')
                                            if price1.__contains__(','):
                                                price1 = price1.replace(',', '.')
                                        price2 = float(price1)
                                        if round(float(price_choose)) >= price2:
                                            urlsFound.append(text2)
                                            counter += 1
                                            textbox.tag_config(f"hyper{counter}", foreground="lightblue", underline=1)
                                            textbox.tag_bind(f"hyper{counter}", "<Button-1>", handle)                                            
                                            if text2.__contains__('otomoto.pl'):
                                                urlsFound.append(text2.replace('https://www.otomoto.pl/oferta/', '').replace('-', ' ').replace('.html', ''))
                                            else:
                                                textbox.insert(END, text2.replace('https://www.olx.pl/d/oferta/', '').replace('-', ' ').replace('.html', ''), tags=f'hyper{counter}')
                                            textbox.insert(END, text='\n')
            req.close()
            sleep(connect_timeout_s)

    customtkinter.set_appearance_mode('dark')
    customtkinter.set_default_color_theme('green')

    def start():    
        t = Timer(1, search)
        t.start()

    def on_quit():
        root.quit()
        exit()
    def stop():
        stopThreads.stopThread = True
    def clear():
        textbox.delete('1.0', END)
    root = customtkinter.CTk()

    root.protocol("WM_DELETE_WINDOW", on_quit)

    root.geometry('1000x700')
    root.resizable(False, False)
    root.title('OOC - Website Offer Checker')

    frame = customtkinter.CTkFrame(master=root)
    frame.pack(pady=20,padx=60,fill='both', expand=True)

    entry = customtkinter.CTkEntry(master=frame, placeholder_text='enter a searchword:')
    entry.pack(pady=12, padx=10)

    entry1 = customtkinter.CTkEntry(master=frame, placeholder_text='max price:')
    entry1.pack(pady=12, padx=10)

    entry2 = customtkinter.CTkEntry(master=frame, placeholder_text='keywords (optional):')
    entry2.pack(pady=12, padx=10)

    entry3 = customtkinter.CTkEntry(master=frame, placeholder_text='enter timeout (sec)')
    entry3.pack(pady=12, padx=10)

    button = customtkinter.CTkButton(master=frame, text='Search...', command=start)
    button.pack(pady=12, padx=10)

    stopbtn = customtkinter.CTkButton(master=frame, text='Stop...', command=stop)
    stopbtn.pack(pady=12, padx=10)
    
    clearbtn = customtkinter.CTkButton(master=frame, text='Clear urls', command=clear)
    clearbtn.pack(pady=12, padx=10)
    
    textbox = customtkinter.CTkTextbox(frame,  width=500, height=300)
    textbox.pack(padx=10, pady=12)

    root.mainloop()
except:
    print('Something went wrong!')
