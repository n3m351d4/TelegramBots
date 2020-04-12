#!/usr/bin/python3
import json
import asyncio
import datetime
import argparse
from UserBotA import *
# Дполонительный файл с функциями, потому что лень скроллить один большой
from random import randint

from telethon import TelegramClient, events, functions, connection
from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest


class custom(dict):
    def __missing__(self, key): return 0

def get_full_name(user):
    if not user.first_name:
        return user.last_name
    elif not user.last_name:
        return user.first_name
    else:
        return "%s %s" % (user.first_name, user.last_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", default='Session.txt',
                        help="file with Telegram session data")
    args = parser.parse_args()

    ids_json_file = 'groups.json'  # will be created automatically
    chat_command = 'Немезида' #плоти донат
    chat_command2 = 'какеры' #вызов бота с игрой
    chat_command3 = '@N3M351DA' #плоти донат
    purge_command = 'Мне это надоело' #пурдж
    chat_command4 = 'top 50' #топ 50 слов
    chat_command5 = 'флудят' #топ активных
    chat_command6 = '/новость'
    chat_command7 = 'Новость ИБ'
    chat_command8 = 'Wikileaks'
    chat_command9 = ['немезида', 'немезиду', 'немезиды']
    chat_command10 = ['flag']
    chat_command11 = 'cvv'
    API_ID = -1  # CHANGE
    API_HASH = '-1'  # CHANGE
    ACC_ID = -1

    try:
        json_data = json.load(open(ids_json_file))
        chats = json_data["ids"]
        blacklist = json_data["peers"]
    except Exception as e:
        print("WARNING can't load chat list: %s" % e)
        chats = []
        blacklist = []

    client = TelegramClient(args.session, API_ID, API_HASH)
    client.start()

    async def ban_in_all_the_chats(peer):
        ban_until = datetime.datetime(2020, 12, 25)  # forever
        rights = ChatBannedRights(ban_until, view_messages=True)
        for chat in chats:
            await client(EditBannedRequest(chat, peer, rights))
        await asyncio.sleep(1)


    def save_json_data():
        json.dump({"ids": chats, "peers": blacklist}, open(ids_json_file, 'w'))
        print("Json data saved")


    async def on_new_message(event):
        global chats

        if event.message.message == purge_command:
            if event.message.from_id != ACC_ID: # Ваш ID аккаунта!
                await event.message.reply('Понимаю')
                return
            reply = await event.get_reply_message()
            temp = [event.id]
            for message in await client.get_messages(event.chat_id, min_id=reply.id - 1, max_id=event.id):
                temp.append(message.id)
            await client.delete_messages(event.chat_id, temp)
            await event.message.reply('Цыц')

        if event.message.message == chat_command:  # Replier mode
            if not event.chat_id in chats:
                chats.append(event.chat_id)
                print("Chat %d has been added" % event.chat_id)
                save_json_data()
            chat = await client.get_entity(event.chat_id)
            user = await client.get_entity(event.message.from_id)
            await event.message.reply('Я не могу отвечать во всех чатах подряд оставьте свое сообщение на donationalerts[.]com/r/n3m351d4 ! Спасибо!')

        if event.message.message == chat_command2:  # Replier mode
            if not event.chat_id in chats:
                chats.append(event.chat_id)
                print("Chat %d has been added" % event.chat_id)
                save_json_data()
            chat = await client.get_entity(event.chat_id)
            user = await client.get_entity(event.message.from_id)
            await event.message.reply('/apt')
            print(event.chat_id)
            chat = await client.get_entity(event.chat_id)
            print(chat)

        if event.message.message == chat_command3:  # Replier mode
            if not event.chat_id in chats:
                chats.append(event.chat_id)
                print("Chat %d has been added" % event.chat_id)
                save_json_data()
            chat = await client.get_entity(event.chat_id)
            user = await client.get_entity(event.message.from_id)
            await event.message.reply('Я не могу отвечать во всех чатах подряд оставьте свое сообщение на donationalerts[.]com/r/n3m351d4 ! Спасибо!')

        if event.message.message == chat_command4:  # Ваш ID аккаунта!
            if event.message.from_id == ACC_ID:
                words = custom()
                progress = await event.message.reply("Wait")
                total = 0
                async for msg in client.iter_messages(event.chat_id, limit=10000):
                    total += 1
                    if total % 2500 == 0:
                        await event.message.reply("Processed {} messages".format(total))
                    if msg.text:
                        for word in msg.text.split():
                            words[word.lower()] += 1
                global freq
                freq = sorted(words, key=words.get, reverse=True)
                out = ""
                for i in range(51):
                    out += "{}. {}:{}\n".format(i + 1, words[freq[i]], freq[i])
                await progress.edit(out, parse_mode=None)

        if event.message.message == chat_command5:
            if event.message.from_id == ACC_ID: # Ваш ID аккаунта!
                chat = await client.get_entity(event.chat_id)
                people = {}
                total = (await client.get_participants(event.chat_id, limit=0)).total
                count = 0
                async for m in client.iter_messages(event.chat_id, limit=400):
                    count +=1
                    print(count)
                    if not m.sender.bot:
                        if m.sender.id in people:
                            people[m.sender.id]["count"] += 1
                        else:
                            people[m.sender.id] = {"first_name":m.sender.username, "count":1}
                await event.message.reply(str(len(people) / total))
                msg = ""
                for uid in people:
                    msg += "{}:{}\n".format(people[uid]["first_name"], people[uid]["count"])
                await event.message.reply(msg)

        if event.message.message == chat_command6:
            if not event.chat_id in chats:
                chats.append(event.chat_id)
                print("Chat %d has been added" % event.chat_id)
                save_json_data()

            parts = [
                ['Злободневная шутка:'],
                ['ВНИМАНИЕ', 'СРОЧНО', 'Привет, ребят'],
                ['мне', 'нам'],
                ['тут только что'],
                ['позвонил', 'написал'],
                ['знакомый из министерства', 'знакомый хирург', 'брат', 'дядя', 'отец', 'родственник из Сибири'],
                ['и попросил'],
                ['никому не говорить', 'всем рассказать'],
                ['о том, что реальная информация'],
                ['Скрывается', 'преувеличена'],
                ['и в скором времени'],
                ['ПИЗДА', 'НЕ ПИЗДА'],
            ]
            text = []
            for part in parts:
                text.append(part[randint(0, len(part)-1)])
            text1 = ' '.join(text)
            await event.message.reply(text1)

        if event.message.message == chat_command7:
            if not event.chat_id in chats:
                chats.append(event.chat_id)
                print("Chat %d has been added" % event.chat_id)
                save_json_data()

            parts = [
                ['CISO и CEO', 'Эксперты', 'Специалисты', 'Исследователи', 'Хакеры', 'Пентестеры', 'APT', 'Инженеры', 'Аналитики', 'Кибервойска'],
                ['компании Информзащита', 'компании Positive Technologies', 'компании Digital Security', 'компании Group-IB', 'компании Ростелеком-Солар', 'компании Kaspersky', 'компании BI.ZONE', 'компании Инфосистемы Джет', 'компании PentestIT'],
                ['выявили', 'предсказали', 'обнаружили', 'атаковали', 'взломали', 'создали', 'придумали', 'нашли', 'внедрили', 'разработали'],
                ['своих клиентов', 'сайт ФСТЭК', 'генератор номеров карт', 'пользователей', 'Ашота из DeviceLock', 'кейген дл WinRAR', 'генератор Пинча', 'Интернет', 'гром-багу в Cisco', 'ARP Spoofing'],
            ]
            text = []
            for part in parts:
                text.append(part[randint(0, len(part)-1)])
            text1 = ' '.join(text)
            await event.message.reply(text1)

        if event.message.message == chat_command8:
            if not event.chat_id in chats:
                chats.append(event.chat_id)
                print("Chat %d has been added" % event.chat_id)
                save_json_data()
            parts = [
                ['осведомленный источник из', 'доверенный человек из', 'надежный источник из', 'известный диссидент и правозащитник из', 'анонимный источник из', 'информатор, близкий к руководству', 'наш постоянный информатор из', 'специальный представитель из', 'глубоко законспирированный агент из'],
                ['Верховного Совета', 'Верховной Рады', 'Кнессета', 'Палаты Лордов', 'парламента', 'Сейма', 'Государственной Думы', 'Сената', 'Конгресса', 'Бундестага', 'Меджелиса'],
                ['США,', 'Зимбабве,', 'Чехословакии,', 'Украины,', 'Афганистана,', 'Ирана,', 'Венесуэлы,', 'КНДР,', 'Белоруссии,', 'Великобритании,', 'Бирмы,', 'Эстонии,'],
                ['на прошлой неделе', 'вчера', 'в начале этого месяца', 'совсем недавно', 'после известных Вам событий', 'в связи с текущей ситуацией', 'еще до Рождества', 'два дня назад', 'сегодня утром'],
                ['Мистер Кребс', 'Товарищ Сачков', 'Товарищ Сталин', 'Виктор Янукович', 'Ким Чен Ир', 'Уго Чавес', 'Джон Маккейн','Усама Бин Ладен', 'Сильвио Берлускони', 'Александр Лукашенко', 'Махмуд Ахмадинеджад', 'Ярослав Качинский', 'Папа Бенедикт XVI', 'принц Чарльз', 'Михаил Саакашвили', 'Збигнев Бжезинский'],
                ['написал статью в \"Коммерсант\"', 'напился пьян', 'подавился булочкой', 'застрял в лифте', 'упал с велосипеда', 'подхватил корону', 'сделал хорошую мину при плохой игре', 'нецензурно выразился про нашего посла', 'опоздал на самолет', 'прыгнул с парашютом', 'завел аккаунт в Твиттере', 'научился играть на балалайке', 'отравился селедкой', 'научился шевелить ушами'],
                ['и, таким образом,', 'и, кроме того,', 'и, тем самым,', 'и откровенно', 'и вообще', 'и неожиданно', 'и в тайне', 'и, как многие считают,', 'и после этого', 'и публично', 'и вскоре'],
                ['надругался над демократией.', 'нарушил права человека.', 'поглумился над правозащитниками.', 'стал отрицать Голодомор.', 'посмеялся над свободой слова.', 'выразил антизападную позицию.', 'не ударил лицом в грязь.', 'поставил под сомнение западные ценности.', 'попал в глупую ситуацию.', 'привлек к себе внимание спецслужб.', 'стал похож на Джорджа Буша младшего.', 'признал вину Ходорковского.'],
                ['Влиятельный еженедельник', 'Оппозиционная газета', 'Демократическое издание', 'Малоизвестный журнал', 'Таблоид', 'Блог газеты', 'Официальный сайт издания', 'Продажный желтый листок', 'Бульварная газета', 'Элитное обозрение'],
                ['\"Иерусалимский Иедиот\"', '\"Русский Молдаван\"', '\"Ваджайна Инсайд\"', '\"Якши Сабантуй\"', '\"Газета Выброшена\"', '\"Зайцунг Фальшстартер\"', '\"Брэйв Виллидж Обсервер\"', '\"Панорома Лузерсвилла\"', '\"Молодой Эректорат\"'],
                ['косвенно подтверждает', 'косвенно опровергает', 'никак не комментирует', 'не подтверждает и не опровергает', 'горячо поддерживает', 'гневно осуждает', 'упорно игнорирует'],
                ['эту информацию.', 'этот случай.', 'этот инцидент.', 'этот конфуз.', 'эту ситуацию.', 'этот прецедент.'],
                ['Как и следовало ожидать,', 'Тем не менее,', 'Неожиданно для всех,', 'Сообщается что,', 'В довершение всего,', 'К всеобщему удовольствию,', 'В результате,', 'По обыкновению,'],
                ['спикер', 'глава', 'лидер', 'электрик', 'дворник', 'какер', 'вебмастер', 'наш человек из'],
                ['назвал произошедшее \"порнографией\".', 'заболел параноей и срочно госпитализирован.', 'не смог увернуться от брошенного в него ботинка.', 'долго крутил пальцем у виска.', 'от неожиданности впал в кому.', 'пытался укусить микрофон.', 'устроил публичный стрипиз.', 'продемонстрировал взлом жопы'],
            ]
            text = []
            for part in parts:
                text.append(part[randint(0, len(part)-1)])
            text1 = ' '.join(text)
            number = randint(1, 10000)
            await event.message.reply('Утечка Wikileaks #' + str(number) + '\n' + 'Как сообщает' + ' ' + text1 + ' (шутка)')

        if any(command in event.message.message.lower() for command in chat_command9):
            private = [-1, -1] # чаты из которых не хотите форвардить
            if any(id == event.chat_id for id in private):
                return
            if not event.chat_id in chats:
               chats.append(event.chat_id)
               print("Chat %d has been added" % event.chat_id)
               save_json_data()
            chat = await client.get_entity(event.chat_id)
            user = await client.get_entity(event.message.from_id)
            print(chat)

            chatname = chat.title
            chat = await client.get_entity(-1) # id чата или аккаунта куда форвардим
            await client.send_message(chat, 'Зафиксировали в ' + chatname)
            await event.forward_to(-1)

        if any(command in event.message.message.lower() for command in chat_command10):
            await privateparser(client,event)

        if event.message.message == chat_command11:
            await cvv(client, event)


    client.add_event_handler(on_new_message, events.NewMessage)
    client.run_until_disconnected()
