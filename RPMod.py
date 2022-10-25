# meta developer: @mm_mods

from .. import loader, utils
import string, pickle, re
from telethon.tl.types import Channel

conf_default = {
    "-s1": {  # СТИЛИ для действия
        "1": [False, "<b>bold/жирный</b>", "<b>", "</b>"],
        "2": [False, "<i>italic/курсив</i>", "<i>", "</i>"],
        "3": [False, "<u>underlined/подчеркнутый</u>", "<u>", "</u>"],
        "4": [False, "<s>strikethrough/зачёркнутый</s>", "<s>", "</s>"],
        "5": [
            False,
            "<tg-spoiler>spoiler/скрытый</tg-spoiler>",
            "<tg-spoiler>",
            "</tg-spoiler>",
        ],
    },
    "-s2": {  # СТИЛИ для "С репликой"
        "1": [True, "<b>bold/жирный</b>", "<b>", "</b>"],
        "2": [False, "<i>italic/курсив</i>", "<i>", "</i>"],
        "3": [False, "<u>underlined/подчеркнутый</u>", "<u>", "</u>"],
        "4": [False, "<s>strikethrough/зачёркнутый</s>", "<s>", "</s>"],
        "5": [
            False,
            "<tg-spoiler>spoiler/скрытый</tg-spoiler>",
            "<tg-spoiler>",
            "</tg-spoiler>",
        ],
    },
    "-s3": {  # СТИЛИ для реплики
        "1": [False, "<b>bold/жирный</b>", "<b>", "</b>"],
        "2": [False, "<i>italic/курсив</i>", "<i>", "</i>"],
        "3": [False, "<u>underlined/подчеркнутый</u>", "<u>", "</u>"],
        "4": [False, "<s>strikethrough/зачёркнутый</s>", "<s>", "</s>"],
        "5": [
            False,
            "<tg-spoiler>spoiler/скрытый</tg-spoiler>",
            "<tg-spoiler>",
            "</tg-spoiler>",
        ],
    },
    "-sE": {  # ЭМОДЗИ перед репликой
        "1": [True, "💬"],
        "2": [False, "💭"],
        "3": [False, "🗯"],
        "4": [False, "✉️"],
        "5": [False, "🔊"],
        "6": [False, "🏳️‍🌈"],
    },
    "-sS": {  # РАЗРЫВ строки в реплике
        "1": [True, "space/пробел", " "],
        "2": [False, "line break/разрыв строки", "\n"],
        "3": [False, "dot + space/точка + пробел", ". "],
        "4": [False, "comma + space/запятая + пробел", ", "],
    },
}


@loader.tds
class RPMod(loader.Module):
    """A little upgraded mod of module of @trololo_1."""

    strings = {
        'name': 'LiMERPMod',
        'separator…': '<b>Here\'s an emoji separator, but no emoji. eh</b>',
        'name?': '<b>Where\'s the name of the RP command?</b>',
        'action?': '<b>Where\'s the action of the RP command?</b>',
        'aarf': '<b>RP commands can\'t be named "all"</b>',
        'added1': "<b>Command '<code>{}</code>' succesfully added with emoji '{}'!</b>",
        'added2': "<b>Command '<code>{}</code>' succesfully added!</b>",
        'weresall': '<b>You\'ve not entered separator or have\'nt entered anything at all.</b>',
        'cleared': '<b>RP commands succesfully cleared!</b>',
        'arg?': '<b>Where\'s the argument?</b>',
        'deleted': '<b>RP command <code>{}</code> succesfully deleted!</b>',
        'notfound': '<b>Command <code>{}</code> not found!</b>',
        'on': '<b>RP commands are now on!</b>',
        'off': '<b>RP commands are now off!</b>',
        'mode': '<b>Mode is now <code>{}</code>!</b>',
        'send': 'sending messages',
        'edit': 'editing messages',
        's-t-wrong': '<b>Something went wrong!</b>',
        'nick-changed': '<b>RP nickname of {} succesfully changed to <code>{}</code>!</b>',
        'count': '<b>You have <code>{}</code> commands</b>',
        'error-with-type': '<b>Error: <code>{}</code></b>',
        'itsnotfile': '<b>It\'s not a file!</b>',
        'actualised': '<b>RP commands succesfully actualised!</b>',
        'chat-excluded': '<b>Chat {} succesfully excluded!</b>',
        'chat-included': '<b>Chat {} succesfully included!</b>',
        'id-wrong': '<b>Wrong ID!</b>',
        'empty-exclude': '<b>Excluded chats list is empty!</b>',
        'excluded-chats': '<b>Excluded chats:</b>',
        'on-in-chat': '<b>RP commands are now on for members of this chat!</b>',
        'off-in-chat': '<b>RP commands are now off for members of this chat!</b>',
        'who-have': '<b>Who have RP commands access:</b>',
        'chats-s': '<b>Chats:</b>',
        'users-s': '<b>Users:</b>',
        'on-for-usr': '<b>RP commands are now on for <code>{}</code>!</b>',
        'off-for-usr': '<b>RP commands are now off for <code>{}</code>!</b>',
        'whatschanged': '''🍋 <b>LIME</b> (1.1) — mod of RPMod (@trololo_1) by @mm_mods
        What\'s changed?
        • No limits now!
        • No check for emoji validity now — add custom emojies…
        • No buggy import now, everyone can use the module.
        • Additions and replicas now save there\'s case.
        Enjoy!''',
        'with-replica': 'With replica:',
        'backup-args-help': '<b>Usage:</b>\n.rpback [-b to save| -l to load (with reply)]',
        'arg-unknown': '<b>Unknown argument!</b>',
        'num-unknown': '<b>Unknown number!</b>',
        'done': '<b>Done!</b>',
        'less-then-2': '<b>Less then 2 arguments!</b>',
        'config': '⚙️ <b>Setting up the template for command:</b>\n-s1 --- turn on/off style for action:\n{s1}\n-s2 '
                  '--- same as s1, but for "With replica" text:\n{}\n-s3 --- same as s2, but for replica:\n{}\n-sE '
                  '--- choose emoji before replica:\n{}\n-sS --- choose symbol for line break in reply:\n{'
                  '}\n\nExample:\n<code>.rpconf -s1 2</code>',
        'config1': '⚙️ <b>Setting up the template for command:',
    }

    strings_ru = {
        'name': 'LiMERPMod',
        'separator…': '<b>Вот разделитель, но нет эмодзи. епт</b>',
        'name?': '<b>Где имя РП-команды?</b>',
        'action?': '<b>Где действие РП-команды?</b>',
        'aarf': '<b>РП-команды не могут называться "all"</b>',
        'added1': "<b>Команда '<code>{}</code>' успешно добавлена с эмодзи '{}'!</b>",
        'added2': "<b>Команда '<code>{}</code>' успешно добавлена!</b>",
        'weresall': '<b>Вы не ввели разделитель или ничего не ввели вообще.</b>',
        'cleared': '<b>РП-команды успешно очищены!</b>',
        'arg?': '<b>Где аргумент?</b>',
        'deleted': '<b>РП-команда <code>{}</code> успешно удалена!</b>',
        'notfound': '<b>Команда <code>{}</code> не найдена!</b>',
        'on': '<b>РП-команды теперь включены!</b>',
        'off': '<b>РП-команды теперь выключены!</b>',
        'mode': '<b>Режим теперь <code>{}</code>!</b>',
        'send': 'отправку сообщений',
        'edit': 'редактирование сообщений',
        's-t-wrong': '<b>Что-то пошло не так!</b>',
        'nick-changed': '<b>Ник {} успешно изменен на <code>{}</code>!</b>',
        'count': '<b>У вас <code>{}</code> команд</b>',
        'error-with-type': '<b>Ошибка: <code>{}</code></b>',
        'itsnotfile': '<b>Это не файл!</b>',
        'actualised': '<b>РП-команды успешно обновлены!</b>',
        'chat-excluded': '<b>Чат {} успешно исключен!</b>',
        'chat-included': '<b>Чат {} успешно включен!</b>',
        'id-wrong': '<b>Неверный ID!</b>',
        'empty-exclude': '<b>Список исключённых чатов пуст!</b>',
        'excluded-chats': '<b>Исключённые чаты:</b>',
        'on-in-chat': '<b>РП-команды теперь включены для участников этого чата!</b>',
        'off-in-chat': '<b>РП-команды теперь выключены для участников этого чата!</b>',
        'who-have': '<b>Кто имеет доступ к РП-командам:</b>',
        'chats-s': '<b>Чаты:</b>',
        'users-s': '<b>Пользователи:</b>',
        'on-for-usr': '<b>РП-команды теперь включены для <code>{}</code>!</b>',
        'off-for-usr': '<b>РП-команды теперь выключены для <code>{}</code>!</b>',
        'whatschanged': '''🍋 <b>LIME</b> (1.1) — модуль RPMod (@trololo_1) от @mm_mods
        Что изменилось?
        • Больше нет ограничений!
        • Больше нет проверки на валидность эмодзи — добавляйте кастомные эмодзи…
        • Больше нет багов с импортом — теперь модуль может использовать каждый.
        • Дополнения и реплики теперь сохраняют свой регистр.
        Наслаждайтесь!''',
        'with-replica': 'С репликой:',
        'backup-args-help': '<b>Использование:</b>\n.rpback [-b для сохранения| -l для загрузки (с ответом)]',
        'arg-unknown': '<b>Неизвестный аргумент!</b>',
        'num-unknown': '<b>Неизвестная цифра!</b>',
        'done': '<b>Готово!</b>',
        'less-than-2': '<b>Меньше двух аргументов передано.</b>',
        'config': '⚙️ <b>Настройка шаблона для команды:</b>\n-s1 --- включить/выключить стиль для действия:\n{}\n-s2 '
                  '--- аналогично для s1, но действует на текст "С репликой":\n{}\n-s3 --- аналогично для s2, '
                  'но действует на саму реплику:\n{}\n-sE --- выбор эмодзи перед репликой:\n{}\n-sS --- выбор символа '
                  'для разрыва строк в реплике:\n{}\n\nПример:\n<code>.rpconf -s1 2</code>',
        'config1': '⚙️ <b>Настройка шаблона для команды:',
        '_cls_doc': 'Слегка улучшенный мод на модуль от @trololo_1.',
        '_cmd_doc_dobrp': 'Создать РП-команду. Аргументы: <команда>/<действие>[/<эмодзи>]',
        '_cmd_doc_delrp': 'Удалить РП-команду. Аргументы: <команда>',
        '_cmd_doc_rplist': 'Показать список РП-команд.',
        '_cmd_doc_rpconf': 'Настроить шаблон для РП-команд. Аргументы: <параметр> <значение>',
        '_cmd_doc_rpback': 'Сохранить/загрузить РП-команд. Аргументы: -b/-l',
        '_cmd_doc_rpnick': 'Изменить ник для РП-команд. Аргументы: <ник> или без ника, чтобы его сбросить. '
                           'В ответ на сообщение нужного пользователя.',
        '_cmd_doc_rpblock': 'Заблокировать/разблокировать РП-команды в чате. Аргументы: <айди чата>. '
                            'Можно и без него, чтобы сменить настройки в этом чате.',
        '_cmd_doc_rpmod': 'Изменить режим РП-команд.',
        '_cmd_doc_useraccept': 'Допустить или нет пользователя/чат в РП-команды. Аргументы: <айди пользователя/чата>. '
                               'Можно без ответа и аргумента, тогда действие будет выполнена над текущим чатом. '
                               'Можно просто без аргумента , тогда действие будет выполнено над пользователем из ответа.',
        '_cmd_doc_mmminfo': 'Показать информацию о моде.',
    }

    async def client_ready(self, client, db):
        self.db = db
        if not self.db.get("RPMod", "exlist", False):
            self.db.set("RPMod", "exlist", [])
        if not self.db.get("RPMod", "status", False):
            self.db.get("RPMod", "status", 1)
        if not self.db.get("RPMod", "rprezjim", False):
            self.db.set("RPMod", "rprezjim", 1)
        if not self.db.get("RPMod", "rpnicks", False):
            self.db.set("RPMod", "rpnicks", {})
        if not self.db.get("RPMod", "rpcomands", False):
            self.db.set("RPMod", "rpcomands", {})
        if not self.db.get("RPMod", "rpemoji", False):
            self.db.set("RPMod", "rpemoji", {})
        if not self.db.get("RPMod", "useraccept", False):
            self.db.set("RPMod", "useraccept", {"chats": [], "users": []})
        elif type(self.db.get("RPMod", "useraccept")) == type([]):
            self.db.set(
                "RPMod",
                "useraccept",
                {"chats": [], "users": self.db.get("RPMod", "useraccept")},
            )
        if self.db.get("RPMod", "rpconfigurate", False):  # ДЛЯ разных версий модуля.
            self.db.set(
                "RPMod",
                "rpconfigurate",
                self.merge_dict(conf_default, self.db.get("RPMod", "rpconfigurate")),
            )

    async def dobrpcmd(self, message):
        """Use: .dobrp (command) / (action) / (emoji) to add command. You can do it without emoji."""
        args = utils.get_args_raw(message)
        dict_rp = self.db.get("RPMod", "rpcomands")

        try:
            key_rp = str(args.split("/")[0]).strip()
            value_rp = str(args.split("/", maxsplit=2)[1]).strip()
            lenght_args = args.split("/")
            count_emoji = 0

            if len(lenght_args) >= 3:
                emoji_rp = str(message.text.split("/", maxsplit=2)[2]).strip()
                dict_emoji_rp = self.db.get("RPMod", "rpemoji")
                r = emoji_rp
                lst = []
                count_emoji = 1
                if not emoji_rp or not emoji_rp.strip():
                    await utils.answer(
                        message, self.strings("separator…")
                    )
                    return
            key_len = [len(x) for x in key_rp.split()]

            if not key_rp or not key_rp.strip():
                await utils.answer(message, self.strings("name?"))
            elif not value_rp or not value_rp.strip():
                await utils.answer(
                    message, self.strings("action")
                )
            elif key_rp == "all":
                await utils.answer(
                    message, self.strings("aarf"),
                )
            elif count_emoji == 1:
                dict_emoji_rp[key_rp] = emoji_rp
                dict_rp[key_rp] = value_rp
                self.db.set("RPMod", "rpcomands", dict_rp)
                self.db.set("RPMod", "rpemoji", dict_emoji_rp)
                await utils.answer(
                    message,
                    self.strings("added1").format(key_rp, emoji_rp),
                )
            else:
                dict_rp[key_rp] = value_rp
                self.db.set("RPMod", "rpcomands", dict_rp)
                await utils.answer(
                    message,
                    self.strings("added2").format(key_rp),
                )
        except:
            await utils.answer(
                message, self.strings("weresall"),
            )

    async def delrpcmd(self, message):
        """Use: .delrp (command) to delete command.\n Use: .delrp all to delete all commands."""
        args = utils.get_args_raw(message)
        dict_rp = self.db.get("RPMod", "rpcomands")
        dict_emoji_rp = self.db.get("RPMod", "rpemoji")
        key_rp = str(args)
        count = 0
        if key_rp == "all":
            dict_rp.clear()
            dict_emoji_rp.clear()
            self.db.set("RPMod", "rpcomands", dict_rp)
            self.db.set("RPMod", "rpemoji", dict_emoji_rp)
            await utils.answer(message, self.strings("cleared"))
            return
        elif not key_rp or not key_rp.strip():
            await utils.answer(message, self.strings("name?"))
        else:
            try:
                if key_rp in dict_emoji_rp:
                    dict_rp.pop(key_rp)
                    dict_emoji_rp.pop(key_rp)
                    self.db.set("RPMod", "rpcomands", dict_rp)
                    self.db.set("RPMod", "rpemoji", dict_emoji_rp)
                else:
                    dict_rp.pop(key_rp)
                    self.db.set("RPMod", "rpcomands", dict_rp)
                await utils.answer(
                    message, self.strings("deleted").format(key_rp),
                )
            except KeyError:
                await utils.answer(message, self.strings("notfound"))

    async def rpmodcmd(self, message):
        """Use: .rpmod to turn on/off RP mode.\nUse: .rpmod toggle to change mode to send or edit message."""
        status = self.db.get("RPMod", "status")
        rezjim = self.db.get("RPMod", "rprezjim")
        args = utils.get_args_raw(message)
        if not args:
            if status == 1:
                self.db.set("RPMod", "status", 2)
                await utils.answer(message, self.strings("off"))
            else:
                self.db.set("RPMod", "status", 1)
                await utils.answer(message, self.strings("on"))
        elif args.strip() == "toggle":
            if rezjim == 1:
                self.db.set("RPMod", "rprezjim", 2)
                await utils.answer(
                    message, self.strings("mode").format(self.strings("send"))
                )
            else:
                self.db.set("RPMod", "rprezjim", 1)
                await utils.answer(
                    message, self.strings("mode").format(self.strings("edit"))
                )
        else:
            await utils.answer(message, self.strings("s-t-wrong"))

    async def rplistcmd(self, message):
        """Use: .rplist to see list of RP commands."""
        com = self.db.get("RPMod", "rpcomands")
        emojies = self.db.get("RPMod", "rpemoji")
        l = len(com)
        listComands = self.strings("count").format(l)
        if len(com) == 0:
            await utils.answer(message, self.strings("count").format(l))
            return
        for i in com:
            if i in emojies.keys():
                listComands += f"\n• <b><code>{i}</code> - {com[i]} |</b> {emojies[i]}"
            else:
                listComands += f"\n• <b><code>{i}</code> - {com[i]}</b>"
        await utils.answer(message, listComands)

    async def rpnickcmd(self, message):
        """Use: .rpnick (nick) to change nick to user or yourself. With -l argument will show all nicks."""
        args = utils.get_args_raw(message).strip()
        reply = await message.get_reply_message()
        nicks = self.db.get("RPMod", "rpnicks")
        if args == "-l":
            str_nicks = "• " + "\n •".join(
                " --- ".join([f"<code>{user_id}</code>", f"<b>{nick}</b>"])
                for user_id, nick in nicks.items()
            )
            return await utils.answer(message, str_nicks)
        if not reply:
            user = await message.client.get_entity(message.sender_id)
        else:
            user = await message.client.get_entity(reply.sender_id)
        if not args:
            if str(user.id) in nicks:
                nicks.pop(str(user.id))
            self.db.set("RPMod", "rpnicks", nicks)
            return await utils.answer(
                message,
                self.strings("nick-changed").format(user.id, user.first_name),
            )
        lst = []
        nick = ""
        nicks[str(user.id)] = args
        self.db.set("RPMod", "rpnicks", nicks)
        await utils.answer(
            message,
            self.strings("nick-changed").format(user.id, args),
        )

    async def rpbackcmd(self, message):
        """Backup RP commands.\n .rpback to see arguments."""
        args = utils.get_args_raw(message).strip()
        comands = self.db.get("RPMod", "rpcomands")
        emojies = self.db.get("RPMod", "rpemoji")
        file_name = "RPModBackUp.pickle"
        id = message.to_id
        reply = await message.get_reply_message()
        if not args:
            await utils.answer(
                message,
                self.strings("backup-args-help"),
            )
        if args == "-b":
            try:
                await message.delete()
                dict_all = {"rp": comands, "emj": emojies}
                with open(file_name, "wb") as f:
                    pickle.dump(dict_all, f)
                await message.client.send_file(id, file_name)
            except Exception as e:
                await utils.answer(message, f"<b>Ошибка:\n</b>{e}")
        elif args == "-r" and reply:
            try:
                if not reply.document:
                    await utils.answer(message, self.strings("itsnotafile"))
                await reply.download_media(file_name)
                with open(file_name, "rb") as f:
                    data = pickle.load(f)
                rp = data["rp"]
                emj = data["emj"]
                result_rp = dict(comands, **rp)
                result_emj = dict(emojies, **emj)
                self.db.set("RPMod", "rpcomands", result_rp)
                self.db.set("RPMod", "rpemoji", result_emj)
                await utils.answer(message, self.strings("actualised"))
            except Exception as e:
                await utils.answer(message, self.strings("error-with-type").format(e))

    async def rpblockcmd(self, message):
        """Use: .rpblock to add/remove exception (use in needed chat).\nUse: .rpblock list to see exceptions.\nUse .rpblock (id) to remove chat from exceptions."""
        args = utils.get_args_raw(message)
        ex = self.db.get("RPMod", "exlist")
        if not args:
            a = await message.client.get_entity(message.to_id)
            if a.id in ex:
                ex.remove(a.id)
                self.db.set("RPMod", "exlist", ex)
                try:
                    name = a.title
                except:
                    name = a.first_name
                await utils.answer(
                    message,
                    self.strings("chat-included").format(name),
                )
            else:
                ex.append(a.id)
                self.db.set("RPMod", "exlist", ex)
                try:
                    name = a.title
                except:
                    name = a.first_name
                await utils.answer(
                    message,
                    self.strings("chat-excluded").format(name),
                )
        elif args.isdigit():
            args = int(args)
            if args in ex:
                ex.remove(args)
                self.db.set("RPMod", "exlist", ex)
                a = await message.client.get_entity(args)
                try:
                    name = a.title
                except:
                    name = a.first_name
                await utils.answer(
                    message,
                    self.strings("chat-excluded").format(name),
                )
            else:
                try:
                    a = await message.client.get_entity(args)
                except:
                    await utils.answer(message, self.strings("is-wrong"))
                ex.append(args)
                self.db.set("RPMod", "exlist", ex)
                try:
                    name = a.title
                except:
                    name = a.first_name
                await utils.answer(message, self.strings("id-wrong"),
                )
        elif args == "list":
            ex_len = len(ex)
            if ex_len == 0:
                await utils.answer(message, self.strings("empty-exclude"))
                return
            sms = self.strings("excluded-chats")
            for i in ex:
                try:
                    a = await message.client.get_entity(i)
                except:
                    await utils.answer(message, self.strings("id-wrong"))
                    return
                try:
                    name = a.title
                except:
                    name = a.first_name
                sms += f"\n• <b><u>{name}</u> --- </b><code>{i}</code>"
            await utils.answer(message, sms)
        else:
            await utils.answer(message, self.strings("s-t-wrong"))

    async def useracceptcmd(self, message):
        """Adding/removing users/chats, allowed to use your commands.\n .useraccept {id/reply}\nTo add chat use without reply and args."""
        reply = await message.get_reply_message()
        args = utils.get_args_raw(message)
        userA = self.db.get("RPMod", "useraccept")
        if not reply and not args and message.is_group:
            chat = message.chat
            if chat.id not in userA["chats"]:
                userA["chats"].append(chat.id)
                return await utils.answer(
                    message,
                    self.strings("on-in-chat").format(chat.title),
                )
            else:
                userA["chats"].remove(chat.id)
                return await utils.answer(
                    message,
                    self.strings("off-in-chat").format(chat.title),
                )
        elif args == "-l":
            sms = self.strings("who-have")
            for k, v in userA.items():
                if k == "chats":
                    sms += self.strings("chats-s")
                else:
                    sms += self.strings("users-s")
                for i in v:
                    try:
                        user = (
                            (await message.client.get_entity(int(i))).title
                            if k == "chats"
                            else (await message.client.get_entity(int(i))).first_name
                        )
                        sms += f"\n<b>• <u>{user}</u> ---</b> <code>{i}</code>"
                    except:
                        sms += f"\n<b>•</b> <code>{i}</code>"
            await utils.answer(message, sms)
        elif args or reply:
            args = int(args) if args.isdigit() else reply.sender_id
            if args in userA["users"]:
                userA["users"].remove(args)
                self.db.set("RPMod", "useraccept", userA)
                await utils.answer(
                    message,
                    self.strings("off-for-usr").format(args)
                )
            elif args in userA["chats"]:
                userA["chats"].remove(args)
                self.db.set("RPMod", "useraccept", userA)
                await utils.answer(
                    message, self.strings("off-in-chat").format(args)
                )
            elif (
                    args not in userA["chats"]
                    and type(await message.client.get_entity(args)) == Channel
            ):
                userA["chats"].append(args)
                self.db.set("RPMod", "useraccept", userA)
                await utils.answer(
                    message, self.strings("on-in-chat").format(args)
                )
            else:
                userA["users"].append(args)
                self.db.set("RPMod", "useraccept", userA)
                await utils.answer(
                    message,
                    self.strings("on-for-usr").format(args),
                )
        else:
            await utils.answer(message, self.strings("s-t-wrong"))

    async def rpconfcmd(self, message):
        """Setting up the template for rp"""
        conf = self.db.get("RPMod", "rpconfigurate", conf_default)
        args = utils.get_args_raw(message)
        if not args:
            sms = self.strings("config1")
            s1 = "\n".join(
                [
                    " | ".join([key, value[1], "✅" if value[0] else "❌"])
                    for key, value in conf["-s1"].items()
                ]
            )
            s2 = "\n".join(
                [
                    " | ".join([key, value[1], "✅" if value[0] else "❌"])
                    for key, value in conf["-s2"].items()
                ]
            )
            s3 = "\n".join(
                [
                    " | ".join([key, value[1], "✅" if value[0] else "❌"])
                    for key, value in conf["-s3"].items()
                ]
            )
            sE = "\n".join(
                [
                    " | ".join([key, value[1], "✅" if value[0] else "❌"])
                    for key, value in conf["-sE"].items()
                ]
            )
            sS = "\n".join(
                [
                    " | ".join([key, value[1], "✅" if value[0] else "❌"])
                    for key, value in conf["-sS"].items()
                ]
            )
            msg_text = self.strings("config2").format(s1, s2, s3, sE, sS)
            return await utils.answer(message, msg_text)
        args = args.split(" ")
        if len(args) <= 1:
            return await utils.answer(message, self.strings("less-then-2"))
        try:
            if args[0] == "-s1" or args[0] == "-s2" or args[0] == "-s3":
                if conf[args[0]][args[1]][0]:
                    conf[args[0]][args[1]][0] = False
                else:
                    conf[args[0]][args[1]][0] = True
            elif args[0] == "-sE" or args[0] == "-sS":
                for i in conf[args[0]].keys():
                    conf[args[0]][i][0] = False
                conf[args[0]][args[1]][0] = True
            else:
                return await utils.answer(message, self.strings("arg-unknown"))
        except:
            return await utils.answer(message, self.strings("num-unknown"))
        self.db.set("RPMod", "rpconfigurate", conf)
        await utils.answer(message, self.strings("done"))

    async def mmminfocmd(self, message):
        """Read mod information and updates."""
        await utils.answer(message, self.strings("whatschanged"))
    async def watcher(self, message):
        try:
            status = self.db.get("RPMod", "status")
            comand = self.db.get("RPMod", "rpcomands")
            rezjim = self.db.get("RPMod", "rprezjim")
            emojies = self.db.get("RPMod", "rpemoji")
            ex = self.db.get("RPMod", "exlist")
            nicks = self.db.get("RPMod", "rpnicks")
            users_accept = self.db.get("RPMod", "useraccept")
            conf = self.db.get("RPMod", "rpconfigurate", conf_default)

            chat_rp = await message.client.get_entity(message.to_id)
            if status != 1 or chat_rp.id in ex:
                return
            me_id = (await message.client.get_me()).id

            if (
                message.sender_id not in users_accept["users"]
                and message.sender_id != me_id
                and chat_rp.id not in users_accept["chats"]
            ):
                return
            me = await message.client.get_entity(message.sender_id)

            if str(me.id) in nicks.keys():
                nick = nicks[str(me.id)]
            else:
                nick = me.first_name
            if ' ' in message.text and '\n' not in message.text:
                args = message.text.split(' ', 1)[0].casefold()+' '+message.text.split(' ', 1)[1]
            elif '\n' in message.text:
                arl = message.text.split('\n', 1)
                if ' ' in arl[0]:
                    args = arl[0].split(' ', 1)[0].casefold() + ' ' + arl[0].split(' ', 1)[1] + '\n' + arl[1]
                else:
                    args = arl[0].casefold()+'\n'+arl[1]
            else:
                args = message.text.casefold()
            lines = args.splitlines()
            tags = lines[0].split(" ")
            if not tags[-1].startswith("@"):
                reply = await message.get_reply_message()
                user = await message.client.get_entity(reply.sender_id)
            else:
                if not tags[-1][1:].isdigit():
                    user = await message.client.get_entity(tags[-1])
                else:
                    user = await message.client.get_entity(int(tags[-1][1:]))
                lines[0] = lines[0].rsplit(" ", 1)[0]
            detail = lines[0].split(" ", maxsplit=1)
            if len(detail) < 2:
                detail.append(" ")
            if detail[0] not in comand.keys():
                return
            detail[1] = " " + detail[1]
            user.first_name = (
                nicks[str(user.id)] if str(user.id) in nicks else user.first_name
            )
            sE = "".join(
                [
                    "".join([value[1] if value[0] else ""])
                    for key, value in conf["-sE"].items()
                ]
            )
            s1 = [
                "".join(
                    [value[2] if value[0] else "" for value in conf["-s1"].values()]
                ),
                "".join(
                    [
                        value[3] if value[0] else ""
                        for value in dict(reversed(list(conf["-s1"].items()))).values()
                    ]
                ),
            ]
            s2 = [
                "".join(
                    [value[2] if value[0] else "" for key, value in conf["-s2"].items()]
                ),
                "".join(
                    [
                        value[3] if value[0] else ""
                        for value in dict(reversed(list(conf["-s2"].items()))).values()
                    ]
                ),
            ]
            s3 = [
                "".join(
                    [value[2] if value[0] else "" for key, value in conf["-s3"].items()]
                ),
                "".join(
                    [
                        value[3] if value[0] else ""
                        for value in dict(reversed(list(conf["-s3"].items()))).values()
                    ]
                ),
            ]
            sS = "".join(
                [
                    "".join([value[2] if value[0] else ""])
                    for key, value in conf["-sS"].items()
                ]
            )

            rpMessageSend = ""
            if detail[0] in emojies.keys():
                rpMessageSend += emojies[detail[0]] + " | "
            rpMessageSend += f"<a href=tg://user?id={me.id}>{nick}</a> {s1[0]}{comand[detail[0]]}{s1[1]} <a href=tg://user?id={user.id}>{user.first_name}</a>{detail[1]}"
            if len(lines) >= 2:
                rpMessageSend += "\n{0} {1[0]}{2}{1[1]} {3[0]}{4}{3[1]}".format(
                    sE, s2, self.strings("with-replica"), s3, sS.join(lines[1:])
                )
            if rezjim == 1:
                return await utils.answer(message, rpMessageSend)
            else:
                return await message.respond(rpMessageSend)
        except:
            pass

    def merge_dict(self, d1, d2):
        d_all = {**d1, **d2}
        for key in d_all:
            d_all[key] = {**d1[key], **d_all[key]}
        return d_all
