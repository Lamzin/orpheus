# # -*- coding: utf-8 -*-

import os
import time
import telepot


import search
import config as cf


def handler(msg):

    # time_begin = time.time()
    # file_name = msg['voice']['file_id'] + '.ogg'
    # newFile = bot.getFile(msg['voice']['file_id'])
    # newFile.download('voices/{}'.format(file_name))

    # tracks = search.SearchApp().run(file_name, cf.FOLDER_BOT)
    # bot.sendMessage(chat_id=msg['chat_id'], text=str(time.time() - time_begin))
    # bot.sendMessage(chat_id=msg['chat_id'], text='\n'.join(tracks))
    print msg
    bot.sendAudio(chat_id=msg[u'chat'][u'id'], audio=open(os.path.join(cf.FOLDER_TEMP, 'foo.ogg'), 'rb'))


token = '217941149:AAEXCQ1BSKwPrFxJjpebolwoMoDIsS-ZTlM'
bot = telepot.Bot(token=token)
bot.notifyOnMessage(handler)

print 'Listening ...'

# Keep the program running.
while 1:
    time.sleep(10)



