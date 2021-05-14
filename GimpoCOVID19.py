from bs4 import BeautifulSoup
from telegram.ext import Updater, MessageHandler, Filters
import os
import requests
import ssl
import telegram
import threading
import urllib.request

targetURL = "https://www.gimpo.go.kr/portal/selectBbsNttList.do?key=999&bbsNo=292&integrDeptCode=&deptNm=&searchCtgry=&searchCnd=SJ&searchKrwd=%5B%EC%BD%94%EB%A1%9C%EB%82%9819%5D"
textName = 'recentInfo.txt'
periodSecond = 60

apiKey = '1824991885:AAHhY0w_cmos2xsNGnfRgGStGVfADi5q7rw'
chatID = 1683823322
bot = telegram.Bot(token=apiKey)

ssl._create_default_https_context = ssl._create_unverified_context

def HTMLParsing(url, tag, attributes):
    getpage= requests.get(url)
    getpageSoup= BeautifulSoup(getpage.text, 'html.parser')
    allClassTopsection= getpageSoup.findAll(tag, attrs=attributes)
    return allClassTopsection

def Notifying():
    htmlParser1 = HTMLParsing(targetURL, 'td', {'class':'p-subject'})

    for para1 in htmlParser1:
        title = str(para1).split('[코로나19]')[1].split('<')[0].strip()

        if not os.path.isfile('./' + textName):
            file = open(textName, 'w', encoding='utf-8')
            file.close
        
        file = open(textName, 'r', encoding='utf-8')
        
        if title != file.read().strip():
            file.close()
            file = open(textName, 'w', encoding='utf-8')
            file.write('%s' %(title))
                
            boardLink = 'https://www.gimpo.go.kr/portal/' + str(para1).split('href="')[1].split('"')[0].replace('&amp;','&')[2:]
            htmlParser2 = HTMLParsing(boardLink, 'td', {'title':'내용'})

            for para2 in htmlParser2:
                list1 = str(para2).split('[코로나19]')
                str1 = list1[len(list1)-1].split('</td>')[0]

                if str1.count('※') >= 1:
                    str1 = str1.split('※')[0]
                
                contents = str1.replace('<br/>','\n').strip() + '\n\n' + boardLink
                bot.sendMessage(chat_id=chatID, text=contents)
                break
        
        file.close()
        break

def Timer():
    timer = threading.Timer(periodSecond, Timer)
    timer.start()
    Notifying()

def ChatBotSender(bot, update):
    text = update.message.text
    chat_id = update.message.chat_id

    if text is not None and text != '':
        bot.send_message(chat_id=chat_id, text='죄송합니다. 이 챗봇은 대화를 지원하지 않습니다.')

#

updater = Updater(token=apiKey)
dispatcher = updater.dispatcher
updater.start_polling()
echoHandler = MessageHandler(Filters.text, ChatBotSender)
dispatcher.add_handler(echoHandler)
Timer()
print('서버가 실행되었습니다!')
