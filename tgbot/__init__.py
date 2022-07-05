import datetime
from email.message import Message
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,

)

import xlsxwriter

from telegram.ext import (
    Updater,
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler
)

from CONST import TOKEN
from bot.models import Post, User
from tgbot.constants import CHECK_POST, NAME, POST_MEDIA, POST_RECEIVERS, POST_TEXT, NUMBER


class Bot(Updater):
    def __init__(self):
        super().__init__(token=TOKEN)
        nots = ~Filters.regex("^(/start|/post)$")
        self.dispatcher.add_handler(
            ConversationHandler(
                [
                    CommandHandler('start', self.start),
                    CommandHandler('post', self.post)
                ],
                {
                    NAME: [
                        MessageHandler(Filters.text & nots, self.name)
                    ],
                    NUMBER: [
                        MessageHandler(Filters.contact & nots, self.number)
                    ],
                    POST_RECEIVERS: [
                        MessageHandler(Filters.text & nots, self.post_receivers)
                    ],
                    POST_MEDIA: [
                        MessageHandler(
                            (Filters.photo | Filters.video | Filters.document) & nots,
                            self.post_media
                        ),
                        CallbackQueryHandler(
                            self.post_media_skip,
                            pattern='send_only_text'
                        )
                    ],
                    POST_TEXT: [
                        MessageHandler(Filters.text & nots, self.post_text),
                        CallbackQueryHandler(
                            self.post_text_skip, pattern="post_text_skip")
                    ],
                    CHECK_POST: [
                        CallbackQueryHandler(
                            self.send_post, pattern="send_post"),
                        CallbackQueryHandler(self.post, pattern="restart_post")
                    ]
                },
                [
                    CommandHandler('start', self.start),
                    CommandHandler('post', self.post)
                ]
            )
        )
        self.dispatcher.add_handler(
            CommandHandler('data', self.data)
        )

        # detect ctrl + c with signal
        import signal
        signal.signal(signal.SIGINT, self.stop)

        self.start_polling()
        self.idle()

    def start(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        if db is None:
            context.user_data['user'] = db = User.objects.create(
                chat_id=user.id)
            user.send_message(
                'Iltimos ismingiz va familyangizni yuboring.', reply_markup=ReplyKeyboardRemove())
            return NAME
        elif not db.is_registered:
            context.user_data['user'] = User.objects.get(chat_id=user.id)
            if not db.name:
                user.send_message(
                    'Iltimos ismningiz va familyangizni yuboring.', reply_markup=ReplyKeyboardRemove())
                return NAME
            elif not db.number:
                user.send_message('Iltimos raqamingizni yuboring.', reply_markup=ReplyKeyboardMarkup(
                    [
                        [
                            KeyboardButton(
                                "Raqamni yuborish",
                                request_contact=True
                            )
                        ]
                    ],
                    resize_keyboard=True
                ))
                return NUMBER
        else:
            user.send_message(
                "Siz ro'yxatdan o'tib bo'lgansiz!"
            )

    def name(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        name = update.message.text
        if len(name.split(" ")) >= 2:
            context.user_data['user'].name = name
            context.user_data['user'].save()
            update.message.reply_text("Iltimos raqamingizni yuboring!", reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        KeyboardButton(
                            "Raqamni yuborish",
                            request_contact=True
                        )
                    ]
                ],
                resize_keyboard=True
            ))
            print('number')
            return NUMBER
        else:
            user.send_message(
                'Iltimos ismningiz va familyangizni yuboring.', reply_markup=ReplyKeyboardRemove())
            return NAME

    def number(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        print('sdfdfg')
        number = update.message.contact.phone_number
        context.user_data['user'].number = number
        context.user_data['user'].is_registered = True
        context.user_data['user'].reg_date = datetime.datetime.now()
        context.user_data['user'].save()
        post:Post = Post.objects.first()
        if post:
            post.send_to(user)
        return ConversationHandler.END

    def data(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        # user.send_message("Iltimos post uchun matn yuboring!")
        if db.is_admin:
            xlsx = self.make_stats()
            user.send_document(xlsx)

    def make_stats(self):
        data = xlsxwriter.Workbook("stats.xlsx")
        worksheet = data.add_worksheet()
        worksheet.write(0, 1, "chat_id")
        worksheet.write(0, 2, "name")
        worksheet.write(0, 3, "number")
        worksheet.write(0, 4, "is_registered")
        worksheet.write(0, 5, "is_admin")
        worksheet.write(0, 6, "start time")
        worksheet.write(0, 7, "reg date")

        users = User.all()
        for i in range(len(users)):
            user = users[i]
            print(user)
            worksheet.write(i+1, 1, user.chat_id)
            worksheet.write(i+1, 2, user.name)
            worksheet.write(i+1, 3, user.number)
            worksheet.write_boolean(i+1, 4, user.is_registered)
            worksheet.write_boolean(i+1, 5, user.is_admin)
            worksheet.write(
                i+1, 6, user.start_time.strftime("%Y-%m-%d %H:%M:%S") if user.start_time else "")
            worksheet.write(
                i+1, 7, user.reg_date.strftime("%Y-%m-%d %H:%M:%S") if user.reg_date else "")
        data.close()




        

        return open("stats.xlsx", 'rb')

    def post(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        if db.is_admin:
            context.user_data['post'] = {}
            context.user_data['select_users_message'] = user.send_message("Iltimos postni kimlarga yuborilishini tanlang!", reply_markup=ReplyKeyboardMarkup(
                [
                    [
                        "Hammaga"
                    ],
                    [
                        "Start bosgan lekin ro'yxatdan o'tmagan",
                        "Ro'yxatdan o'tganlarga"
                    ]
                ],
                resize_keyboard=True
            ))
            return POST_RECEIVERS

    def post_receivers(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        try:
            context.user_data['select_users_message'].delete()
        except Exception as e:
            print(e)
            pass
        context.user_data['post']['receivers'] = 0 if update.message.text == "Hammaga" else (
            1 if update.message.text == "Start bosgan lekin ro'yxatdan o'tmagan" else 2
        )
        user.send_message("Iltimos postni mediasini yuboring!", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Textning o'zini yuborish",
                        callback_data="send_only_text"
                    ),
                ]
            ]
        ))
        return POST_MEDIA

    def post_media(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        context.user_data['post']['media'] = update.message.photo[-1] or update.message.document or update.message.video or update.message.audio
        context.user_data['post']['media_type'] = 1 if update.message.photo else (
            2 if update.message.video else (
                3 if update.message.audio else 4
            )
        )

        if update.message.caption:
            context.user_data['post']['text'] = update.message.caption
            context.user_data['post']['entity'] = update.message.entities
            self.check_post(update, context)
            return CHECK_POST

        user.send_message("Iltimos postni matnini yuboring!", reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "matnsiz yuborish" ,
                        callback_data="post_text_skip"
                    )
                ]
            ]
        ))

        return POST_TEXT
    
    def post_media_skip(self, update:Update, context:CallbackContext):
        user, db = User.get(update)
        context.user_data['post']['media'] = None
        context.user_data['post']['media_type'] = 0
        user.send_message("Iltimos postni matnini yuboring!")
        return POST_TEXT

    def post_text(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        context.user_data['post']['text'] = update.message.text
        context.user_data['post']['entity'] = update.message.entities

        self.check_post(update, context)
        return CHECK_POST

    def post_text_skip(self, update: Update, context: CallbackContext):
        user, db = User.get(update)
        context.user_data['post']['text'] = ""
        context.user_data['post']['entity'] = []
        self.check_post(update, context)
        return CHECK_POST

    def check_post(self, update: Update, context: CallbackContext):
        user, db = User.get(update)

        if context.user_data['post']['media_type'] == 1:
            user.send_photo(
                context.user_data['post']['media'],
                caption=context.user_data['post']['text'],
                caption_entities=context.user_data['post']['entity'],
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Yuborish",
                                callback_data="send_post"
                            ),
                            InlineKeyboardButton(
                                "Qayta yaratish",
                                callback_data="restart_post"
                            )
                        ]
                    ]
                )
            )
        elif context.user_data['post']['media_type'] == 2:
            user.send_video(
                context.user_data['post']['media'],
                caption=context.user_data['post']['text'],
                caption_entities=context.user_data['post']['entity'],
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Yuborish",
                                callback_data="send_post"
                            ),
                            InlineKeyboardButton(
                                "Qayta yaratish",
                                callback_data="restart_post"
                            )
                        ]
                    ]
                )
            )
        elif context.user_data['post']['media_type'] == 3:
            user.send_audio(
                context.user_data['post']['media'],
                caption=context.user_data['post']['text'],
                caption_entities=context.user_data['post']['entity'],
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Yuborish",
                                callback_data="send_post"
                            ),
                            InlineKeyboardButton(
                                "Qayta yaratish",
                                callback_data="restart_post"
                            )
                        ]
                    ]
                )
            )
        elif context.user_data['post']['media_type'] == 4:
            user.send_document(
                context.user_data['post']['media'],
                caption=context.user_data['post']['text'],
                caption_entities=context.user_data['post']['entity'],
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "Yuborish",
                                callback_data="send_post"
                            ),
                            InlineKeyboardButton(
                                "Qayta yaratish",
                                callback_data="restart_post"
                            )
                        ]
                    ]
                )
            )
        else:
            user.send_message(context.user_data['post']['text'],
                              entities=context.user_data['post']['entity'],
                              reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Yuborish",
                            callback_data="send_post"
                        ),
                        InlineKeyboardButton(
                            "Qayta yaratish",
                            callback_data="restart_post"
                        )
                    ]
                ]
            )
            )

    def send_post(self, update: Update, context: CallbackContext):
        _user, db = User.get(update)
        print('sddfgdg')
        users = User.all() if context.user_data['post']['receivers'] == 0 else (
            User.objects.filter(is_registered=False) if context.user_data['post']['receivers'] == 1 else User.objects.filter(
                is_registered=True)
        )
        sent = 0
        not_sent = 0
        for user in users:
            try:
                if context.user_data['post']['media_type'] == 1:
                    self.bot.send_photo(
                        user.chat_id,
                        context.user_data['post']['media'],
                        caption=context.user_data['post']['text'],
                        caption_entities=context.user_data['post']['entity'],

                    )
                elif context.user_data['post']['media_type'] == 2:
                    self.bot.send_video(
                        user.chat_id,
                        context.user_data['post']['media'],
                        caption=context.user_data['post']['text'],
                        caption_entities=context.user_data['post']['entity'],

                    )
                elif context.user_data['post']['media_type'] == 3:
                    self.bot.send_audio(
                        user.chat_id,
                        context.user_data['post']['media'],
                        caption=context.user_data['post']['text'],
                        caption_entities=context.user_data['post']['entity'],

                    )
                elif context.user_data['post']['media_type'] == 4:
                    self.bot.send_document(
                        user.chat_id,
                        context.user_data['post']['media'],
                        caption=context.user_data['post']['text'],
                        caption_entities=context.user_data['post']['entity'],

                    )
                else:
                    self.bot.send_message(
                        user.chat_id, context.user_data['post']['text'],
                        entities=context.user_data['post']['entity'],
                    )
                sent += 1

            except Exception as e:
                print(e)
                not_sent += 1

        _user.send_message(
            f"""Foydalanuvchilar: {users.count()} nafar
            {sent} ta foydalanuvchi uchun post yuborildi.
            {not_sent} ta foydalanuvchi uchun post yuborilmadi."""
        )
        return -1