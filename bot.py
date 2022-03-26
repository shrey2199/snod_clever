# -*- coding: utf-8 -*-

import telebot
import telegram
import logging
import time
import random
import os
import fnmatch
from telegraph import Telegraph
import sys
import subprocess

# Helper Modules
from helpers.uptime import get_readable_time
from helpers.database import db_add_result, db_adddetails, db_createtable, db_get_details, db_update_pass, db_update_user, dbcheck, db_id_not_exist

# CREATE TABLE IN DB
db_createtable()

# UPTIME
botStartTime = time.time()

# CONFIG
from config import Config

BOT_TOKEN = Config.BOT_TOKEN
DATABASE_URI = Config.DATABASE_URI
WEBSITE_URL = Config.WEBSITE_URL

# BOT INIT & Keep Alive
bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

alive = subprocess.Popen(['python3', 'alive.py'])

# Telegraph
telegraph = Telegraph()

telegraph_acc = telegraph.create_account(
    short_name="DONS",
    author_name="DONS Revision Bot",
    author_url="https://github.com/shrey2199/DONS_Revision_Bot"
)

# USERS - List That Stores A Dictionary For Every User Keeping an Account Of Each Attempted Question until A Result is generated.
users = []

# BOT

### BOT COMMANDS

## '''/start command'''
@bot.message_handler(commands=['start'])
def start(m):
    uptime = get_readable_time((time.time() - botStartTime))
    global start_string
    start_string = f"Hi ! Welcome to *S.N.O.D Revision Bot*. A Revision Bot for Students of *Class 12*.\n\n*I'm Alive Since : *`{uptime}`\n\nUse /help To See Instructions and Bot Commands !!\n\n`This Bot Has been made with Collective Efforts from :-`*\n\t1. Shreyansh\n\t2. Omkar\n\t3. Nischay\n\t4. Divyansh*"
    id = str(m.from_user.id)
    if db_id_not_exist(m):
        startmes = bot.send_message(m.chat.id, text='Pls Reply To This Message With Your Name !')
        bot.register_for_reply(startmes, ask_name)
    else:
        global startmessage
        startmessage = bot.send_message(m.chat.id, start_string, parse_mode=telegram.ParseMode.MARKDOWN)
    num_user = 0
    for user in users:
        if str(m.from_user.id) in user.keys():
            num_user += 1
    if num_user == 0:
        users.append({id:'', "phy":[], "maths":[], "chem":[], "score":{"pscore":[], "mscore":[], "cscore":[]}})
    else:
        pass

#### '''FUNCTION THAT ASKS FOR NAME IF USER NOT IN DATABASE'''
def ask_name(m):
    name = m.text
    db_adddetails(m, name)
    uptime = get_readable_time((time.time() - botStartTime))
    global startmessage
    startmessage = bot.send_message(m.chat.id, start_string, parse_mode=telegram.ParseMode.MARKDOWN)

## '''/result command'''
@bot.message_handler(commands=['result'])
def results(m):
    result(m)

#### '''FUNCTION THAT COLLECTS THE QUESTIONS ANSWERED AND PREPARES A RESULT'''
def result(m):
    id = str(m.chat.id)
    y = [x for x in users if id in x.keys()][0]

    # Physics
    if len(y["score"]["pscore"]) != 0:
        pscore = f'{len([m for m in y["score"]["pscore"] if int(m["marks"]) == 1])} / {len(y["score"]["pscore"])}'
        phy_html = f"<br><p><b>You Physics Score : {pscore}</b></p><hr size='2'>"
        pq = 0
        for ques in y["score"]["pscore"]:
            pq += 1
            ques_html = f'''<p>
                            <b>{pq}.</b> {ques["question"]}<br><br>
                            <b>--------Your Answer : </b><code>{ques["my_opt"]}</code><br>
                            <b>--------Correct Answer : </b><code>{ques["correct_opt"]}</code><br>
                            <b>--------Marks Obtained : </b><b>{ques["marks"]}/1 {ques["emoji"]}</b><br>
                            <br>➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖<br>
                            </p>'''
            phy_html += ques_html

        telegraph_res = telegraph.create_page(
            title="Physics Results",
            html_content=phy_html,
            author_name='DONS Revision Bot',
            author_url='https://github.com/shrey2199/DONS_Revision_Bot'
        )
        telegraph_purl = f'https://telegra.ph/{telegraph_res["path"]}'

    else:
        telegraph_purl = "Did Not Attempt !"

        pscore = telegraph_purl

    # Maths
    if len(y["score"]["mscore"]) != 0:
        mscore = f'{len([m for m in y["score"]["mscore"] if int(m["marks"]) == 1])} / {len(y["score"]["mscore"])}'
        maths_html = f"<br><p><b>You Maths Score : {mscore}</b></p><hr size='2'>"
        pq = 0
        for ques in y["score"]["mscore"]:
            pq += 1
            ques_html = f'''<img src='{ques["question"]}'>
                            <p>
                            <b>{pq}.</b><br><br>
                            <b>--------Your Answer : </b><code>{ques["my_opt"]}</code><br>
                            <b>--------Correct Answer : </b><code>{ques["correct_opt"]}</code><br>
                            <b>--------Marks Obtained : </b><b>{ques["marks"]}/1 {ques["emoji"]}</b><br>
                            <br>➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖<br>
                            </p>'''
            maths_html += ques_html

        telegraph_res = telegraph.create_page(
            title="Mathematics Results",
            html_content=maths_html,
            author_name='DONS Revision Bot',
            author_url='https://github.com/shrey2199/DONS_Revision_Bot'
        )
        telegraph_murl = f'https://telegra.ph/{telegraph_res["path"]}'

    else:
        telegraph_murl = "Did Not Attempt !"

        mscore = telegraph_murl

    # Chemistry
    if len(y["score"]["cscore"]) != 0:
        cscore = f'{len([m for m in y["score"]["cscore"] if int(m["marks"]) == 1])} / {len(y["score"]["cscore"])}'
        chem_html = f"<br><p><b>You Chemistry Score : {cscore}</b></p><hr size='2'>"
        pq = 0
        for ques in y["score"]["cscore"]:
            pq += 1
            ques_html = f'''<img src='{ques["question"]}'>
                            <p>
                            <b>{pq}.</b><br><br>
                            <b>--------Your Answer : </b><code>{ques["my_opt"]}</code><br>
                            <b>--------Correct Answer : </b><code>{ques["correct_opt"]}</code><br>
                            <b>--------Marks Obtained : </b><b>{ques["marks"]}/1  {ques["emoji"]}</b><br>
                            <br>➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖<br>
                            </p>'''
            chem_html += ques_html

        telegraph_res = telegraph.create_page(
            title="Chemistry Results",
            html_content=chem_html,
            author_name='DONS Revision Bot',
            author_url='https://github.com/shrey2199/DONS_Revision_Bot'
        )
        telegraph_curl = f'https://telegra.ph/{telegraph_res["path"]}'

    else:
        telegraph_curl = "Did Not Attempt !"

        cscore = telegraph_curl

    # Inline Keyboard
    keyboard = telebot.types.InlineKeyboardMarkup()
    if len(y["score"]["mscore"]) != 0:
        keyboard.row(
            telebot.types.InlineKeyboardButton('Maths Result', url=telegraph_murl)
        )
    else:
        pass
    if len(y["score"]["pscore"]) != 0:
        keyboard.row(
            telebot.types.InlineKeyboardButton('Physics Result', url=telegraph_purl)
        )
    else:
        pass
    if len(y["score"]["cscore"]) != 0:
        keyboard.row(
            telebot.types.InlineKeyboardButton('Chemistry Result', url=telegraph_curl)
        )
    else:
        pass
    
    # Message TEXT
    Total_obtained = len([m for m in y["score"]["pscore"] if int(m["marks"]) == 1]) + len([m for m in y["score"]["mscore"] if int(m["marks"]) == 1]) + len([m for m in y["score"]["cscore"] if int(m["marks"]) == 1])
    Total_Attempted = len(y["score"]["pscore"]) + len(y["score"]["mscore"]) + len(y["score"]["cscore"])
    Total_Score = f'{Total_obtained} / {Total_Attempted}'
    result_str = f"*Here Is Your Result !!*\n\n*Your Total Score* : `{Total_Score}`\n\n  *Physics* : `{pscore}`\n  *Chemistry* : `{cscore}`\n  *Mathematics* : `{mscore}`"

    # ADD TO DATABASE
    db_add_result(m, telegraph_purl, telegraph_murl, telegraph_curl, Total_Score)

    # EMPTY UP THE Questions from Users Dictionary
    y['phy'] = []
    y['maths'] = []
    y['chem'] = []
    y["score"]["cscore"] = []
    y["score"]["mscore"] = []
    y["score"]["pscore"] = []

    # Message
    bot.send_message(chat_id=m.chat.id, text=result_str, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN, disable_web_page_preview=True)

## '''/id command - for getting ID and password to access Web UI'''
@bot.message_handler(commands=['id'])
def id(m):
    id_str = f"""*Here are Your Credentials :- *\n\n*Unique ID / UserName* : `{db_get_details(m)[3]}`\n*Password* : `{db_get_details(m)[4]}`\n\nUse It at [Revision Bot Website]({WEBSITE_URL}) to View Your Previous Results !
    \n🔑 To Change Your Credentials, Send /changeid to Bot ! """
    bot.send_message(m.chat.id, text=id_str, parse_mode=telegram.ParseMode.MARKDOWN)

## '''/changeid command - for changing ID and password'''
@bot.message_handler(commands=['changeid'])
def changeid(m):
    cng_id = bot.send_message(m.chat.id, text='Reply To This Message With Your New UserName.')
    bot.register_for_reply(cng_id, chng_user)

def chng_user(m):
    username = m.text
    db_update_user(m, username)
    chng_user_mes = bot.send_message(m.chat.id, text='UserName Changed Successfully !!\n\nNow, Reply To This Message With Your New Password.')
    bot.register_for_reply(chng_user_mes, chng_pass)

def chng_pass(m):
    password = m.text
    db_update_pass(m, password)
    new_id_str = f"*Here are Your New Credentials :- *\n\n*Unique ID / UserName* : `{db_get_details(m)[3]}`\n*Password* : `{db_get_details(m)[4]}`\n\nUse It at [Revision Bot Website]({WEBSITE_URL}) to View Your Previous Results !"
    chng_pass_mes = bot.send_message(m.chat.id, new_id_str, parse_mode=telegram.ParseMode.MARKDOWN)

## '''/help command'''
@bot.message_handler(commands=['help'])
def help(m):
    help_message = f'''*This is A Revision Bot for Class 12.*\n\n`The Bot will itself tell you HOW TO BE USED as you keep moving forward take the Tests.`
    \n*Bot Commands :-*
    /start - `To Display The Start Message !`
    /help - `To See the Instructions !`
    /revise - `To Begin The Revision !`
    \n*Instructions :-*
1. If You Accidentally Close Your Test instead of Generating The Result, You Can use /result to get your result of attempted Questions.\n
2. If You Want To Access Your Previous Results, Go To [Revision Bot Website]({WEBSITE_URL}) and enter the id obtained by using /id command.\n
3. You cannot continue Tests after Submitting and Generating The Results.

*THANKS FOR USING THE BOT !\n\nWE HOPE IT HELPS YOU !*
    '''
    bot.send_message(m.chat.id, help_message, parse_mode=telegram.ParseMode.MARKDOWN)

## '''/revise command'''
@bot.message_handler(commands=['revise'])
def revise(m):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('Start Revision', callback_data='start'),
        telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
    )
    re_string = f"Hey {m.from_user.first_name} !\n\n*Let's Begin The Revision.*\n\nGo For The `Start Revision` Button Below !"
    re_message = bot.send_message(m.chat.id, re_string, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
    id = str(m.from_user.id)
    if str(sys.platform).startswith('win'):
        if str(id) in os.listdir():
            cmd = f"rmdir /s/q {id} && mkdir {id} && xcopy Questions\ {id}\Questions\ /E/H"
        else:
            cmd = f"mkdir {id} && xcopy Questions\ {id}\Questions\ /E/H"
    else:
        cmd = f"mkdir -p {id} && cp -r Questions {id}/."
    os.popen(cmd)
    num_user = 0
    for user in users:
        if str(m.from_user.id) in user.keys():
            user.update({id:re_message.message_id})
            num_user += 1
    if num_user == 0:
        users.append({id:re_message.message_id, "phy":[], "maths":[], "chem":[], "score":{"pscore":[], "mscore":[], "cscore":[]}})
    else:
        pass

#================================================================================================================================

# QUERY HANDLING (FROM HERE ON IS THE PART WHERE THE BUTTONS AND THEIR RESPONSE IS MANAGED)

# Query Handler - Converts Callback Data into Queries that can be inferred By Other Functions
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

# Execution of Various Functions based on CallBack DATA
def get_callback(query):
    bot.answer_callback_query(query.id)
    if data == 'start':
        update_message(query.message)
    elif data.startswith("num"):
        num_Revision(query.message)
        update_message(query.message)
    elif data == 'maths':
        maths_Revision(query.message)
        maths_message(query.message)
    elif data == 'chemistry':
        chem_Revision(query.message)
        chem_message(query.message)
    elif data == 'physics':
        phy_Revision(query.message)
        phy_message(query.message)
    elif data == 'ma' or data == 'mb' or data == 'mc' or data == 'md':
        maths_message(query.message)
    elif data == 'pa' or data == 'pb' or data == 'pc' or data == 'pd':
        phy_message(query.message)
    elif data == 'ca' or data == 'cb' or data == 'cc' or data == 'cd':
        chem_message(query.message)
    elif data == 'gen_result':
        result(query.message)
    else:
        update_message(query.message)

# Function That Manages Number of Questions
def num_Revision(m):
    if data.startswith("num"):
        global n
        n = int(data[3:])
    else:
        pass

# MATHEMATICS FUNCTIONS

## '''Function To Return Questions and The Buttons On Them'''
def maths_Revision(m):
    global qno
    y = [x for x in users if str(m.chat.id) in x.keys()]
    id = str(m.chat.id)
    dirpath = f'{id}/Questions/Maths/'
    nof = len(fnmatch.filter(os.listdir(dirpath), '*.txt'))
    if len(y[0]["maths"]) != n:
        qno = random.choice([i for i in range(1,nof+1) if i not in y[0]["maths"]])
        y[0]["maths"].append(qno)
        global q_path
        q_path = f'{dirpath}{str(qno)}.txt'
        with open(file=q_path, mode='r') as ques:
            ques_list = ques.read().splitlines()
            global question
            question = ques_list[0]
            global corr_opt
            corr_opt = ques_list[1]
            subject = ques_list[2]
            chapter = ques_list[3]
        message_text = f"*Subject : *{subject}\n*Chapter : *{chapter}\n\nChoose The Correct Option : "
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('A', callback_data='ma'),
            telebot.types.InlineKeyboardButton('B', callback_data='mb'),
            telebot.types.InlineKeyboardButton('C', callback_data='mc'),
            telebot.types.InlineKeyboardButton('D', callback_data='md')
        )
        global photo_mes
        bot.edit_message_text(message_text,
            m.chat.id, message_id=y[0][str(m.chat.id)],
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        photo_mes = bot.send_photo(m.chat.id, photo=question, reply_markup=keyboard)
        y[0].update({"mphoto":str(photo_mes.message_id)})
    elif len(y[0]["maths"]) == n:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
                telebot.types.InlineKeyboardButton('Generate Result', callback_data='gen_result')
        )
        bot.edit_message_text("`Revision Finished !!`",
            m.chat.id, message_id=y[0][str(m.chat.id)], reply_markup=keyboard,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

## '''Function That Manages The Message Sent on Pressing An Options and Detects The Answer'''
def maths_message(m):
    if data == 'ma' or data =='mb' or data=='mc'or data=='md':
        y = [x for x in users if str(m.chat.id) in x.keys()]
        try:
            bot.delete_message(m.chat.id, message_id=y[0]["mphoto"])
        except:
            pass
        if data == "m" + corr_opt:
            pg = "Correct Answer !!"
            bot.edit_message_text(pg,
                m.chat.id, message_id=y[0][str(m.chat.id)],
                reply_markup=math_key(pg, m),
                parse_mode=telegram.ParseMode.MARKDOWN
            )

            my_opt = f"{data[1].upper()}"
            correct_opt = my_opt
            mscore_dict = {"qno":qno, "question":question, "my_opt":my_opt, "correct_opt":correct_opt, "marks":1, "emoji":"✔️"}
            y[0]["score"]["mscore"].append(mscore_dict)
        else:
            pg = "Wrong Answer !!"
            bot.edit_message_text(pg,
                m.chat.id, message_id=y[0][str(m.chat.id)],
                reply_markup=math_key(pg, m),
                parse_mode=telegram.ParseMode.MARKDOWN
            )

            correct_opt = f"{corr_opt.upper()}"
            my_opt = f"{data[1].upper()}"
            mscore_dict = {"qno":qno, "question":question, "my_opt":my_opt, "correct_opt":correct_opt, "marks":0, "emoji":"❌"}
            y[0]["score"]["mscore"].append(mscore_dict)
    else:
        pass

## '''Function That Manages Keyboard Layout after Option is Chosen'''
def math_key(pg, m):
    y = [x for x in users if str(m.chat.id) in x.keys()]
    if len(y[0]["maths"]) < n:
        if data == corr_opt:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Next', callback_data='maths'),
                telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
            )
            return keyboard
        else:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Next', callback_data='maths'),
                telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
            )
            return keyboard
    elif len(y[0]["maths"]) == n:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Submit', callback_data='maths'),
            telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
        )
        if len(y[0]['phy']) != n:
            keyboard.row(
                telebot.types.InlineKeyboardButton('Continue to Physics', callback_data='physics')
            )
        else:
            pass
        if len(y[0]['chem']) != n:
            keyboard.row(
                telebot.types.InlineKeyboardButton('Continue to Chemistry', callback_data='chemistry')
            )
        else:
            pass
        keyboard.row(
            telebot.types.InlineKeyboardButton('Generate Result', callback_data='gen_result')
        )
        return keyboard
    else:
        pass

# PHYSICS FUNCTIONS

## '''Function To Return Questions and The Buttons On Them'''
def phy_Revision(m):
    global qno
    y = [x for x in users if str(m.chat.id) in x.keys()]
    id = str(m.chat.id)
    dirpath = f'{id}/Questions/Physics/'
    nof = len(fnmatch.filter(os.listdir(dirpath), '*.txt'))
    if len(y[0]["phy"]) != n:
        qno = random.choice([i for i in range(1,nof+1) if i not in y[0]["phy"]])
        y[0]["phy"].append(qno)
        global q_path
        q_path = f'{dirpath}{str(qno)}.txt'
        with open(file=q_path, mode='r') as ques:
            ques_list = ques.read().splitlines()
            global question
            question = ques_list[0]
            global opt_a
            opt_a = ques_list[1]
            global opt_b
            opt_b = ques_list[2]
            global opt_c
            opt_c = ques_list[3]
            global opt_d
            opt_d = ques_list[4]
            global corr_opt
            corr_opt = ques_list[5]
            subject = ques_list[6]
            chapter = ques_list[7]
        message_text = f"*Subject : *{subject}\n*Chapter : *{chapter}\n\n*Question : *{question}\n\nA.  {opt_a}\nB.  {opt_b}\nC.  {opt_c}\nD.  {opt_d}\n"
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('A', callback_data='pa'),
            telebot.types.InlineKeyboardButton('B', callback_data='pb'),
            telebot.types.InlineKeyboardButton('C', callback_data='pc'),
            telebot.types.InlineKeyboardButton('D', callback_data='pd')
        )
        bot.edit_message_text(message_text,
            m.chat.id, message_id=y[0][str(m.chat.id)],
            reply_markup=keyboard,
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    elif len(y[0]["phy"]) == n:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
                telebot.types.InlineKeyboardButton('Generate Result', callback_data='gen_result')
        )
        bot.edit_message_text("`Revision Finished !!`",
            m.chat.id, message_id=y[0][str(m.chat.id)], reply_markup=keyboard,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

## '''Function That Manages The Message Sent on Pressing An Options and Detects The Answer'''
def phy_message(m):
    if data == 'pa' or data =='pb' or data=='pc'or data=='pd':
        y = [x for x in users if str(m.chat.id) in x.keys()]
        if data == "p" + corr_opt:
            pg = "Correct Answer !!"
            bot.edit_message_text(pg,
                m.chat.id, message_id=y[0][str(m.chat.id)],
                reply_markup=phy_key(pg, m),
                parse_mode=telegram.ParseMode.MARKDOWN
            )

            myoval = globals()[f"opt_{data[1]}"]
            myoval = myoval.lstrip("`").rstrip("`")
            my_opt = f"{data[1].upper()}. {myoval}"

            correct_opt = my_opt
            pscore_dict = {"qno":qno, "question":question.replace("<","&lt;").replace(">","&gt;"), "my_opt":my_opt.replace("<","&lt;").replace(">","&gt;"), "correct_opt":correct_opt.replace("<","&lt;").replace(">","&gt;"), "marks":1, "emoji":"✔️"}
            y[0]["score"]["pscore"].append(pscore_dict)
        else:
            pg = "Wrong Answer !!"
            bot.edit_message_text(pg,
                m.chat.id, message_id=y[0][str(m.chat.id)],
                reply_markup=phy_key(pg, m),
                parse_mode=telegram.ParseMode.MARKDOWN
            )

            myoval = globals()[f"opt_{data[1]}"]
            myoval = myoval.lstrip("`").rstrip("`")
            my_opt = f"{data[1].upper()}. {myoval}"
            
            coval = globals()[f"opt_{corr_opt}"]
            coval = coval.lstrip("`").rstrip("`")
            correct_opt = f"{corr_opt.upper()}. {coval}"

            pscore_dict = {"question":question.replace("<","&lt;").replace(">","&gt;"), "qno":qno, "my_opt":my_opt.replace("<","&lt;").replace(">","&gt;"), "correct_opt":correct_opt.replace("<","&lt;").replace(">","&gt;"), "marks":0, "emoji":"❌"}
            y[0]["score"]["pscore"].append(pscore_dict)
    else:
        pass

## '''Function That Manages Keyboard Layout after Option is Chosen'''
def phy_key(pg, m):
    y = [x for x in users if str(m.chat.id) in x.keys()]
    if len(y[0]["phy"]) < n:
        if data == corr_opt:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Next', callback_data='physics'),
                telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
            )
            return keyboard
        else:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Next', callback_data='physics'),
                telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
            )
            return keyboard
    elif len(y[0]["phy"]) == n:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Submit', callback_data='physics'),
            telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
        )
        if len(y[0]['maths']) != n:
            keyboard.row(
                telebot.types.InlineKeyboardButton('Continue to Maths', callback_data='maths')
            )
        else:
            pass
        if len(y[0]['chem']) != n:
            keyboard.row(
                telebot.types.InlineKeyboardButton('Continue to Chemistry', callback_data='chemistry')
            )
        else:
            pass
        keyboard.row(
            telebot.types.InlineKeyboardButton('Generate Result', callback_data='gen_result')
        )
        return keyboard
    else:
        pass

# CHEMISTRY FUNCTIONS

## '''Function To Return Questions and The Buttons On Them'''
def chem_Revision(m):
    global qno
    y = [x for x in users if str(m.chat.id) in x.keys()]
    id = str(m.chat.id)
    dirpath = f'{id}/Questions/Chemistry/'
    nof = len(fnmatch.filter(os.listdir(dirpath), '*.txt'))
    if len(y[0]["chem"]) != n:
        qno = random.choice([i for i in range(1,nof+1) if i not in y[0]["chem"]])
        y[0]["chem"].append(qno)
        global q_path
        q_path = f'{dirpath}{str(qno)}.txt'
        with open(file=q_path, mode='r') as ques:
            ques_list = ques.read().splitlines()
            global question
            question = ques_list[0]
            global corr_opt
            corr_opt = ques_list[1]
            subject = ques_list[2]
            chapter = ques_list[3]
        message_text = f"*Subject : *{subject}\n*Chapter : *{chapter}\n\nChoose The Correct Option : "
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('A', callback_data='ca'),
            telebot.types.InlineKeyboardButton('B', callback_data='cb'),
            telebot.types.InlineKeyboardButton('C', callback_data='cc'),
            telebot.types.InlineKeyboardButton('D', callback_data='cd')
        )
        global photo_mes
        bot.edit_message_text(message_text,
            m.chat.id, message_id=y[0][str(m.chat.id)],
            parse_mode=telegram.ParseMode.MARKDOWN
        )
        photo_mes = bot.send_photo(m.chat.id, photo=question, reply_markup=keyboard)
        y[0].update({"cphoto":str(photo_mes.message_id)})
    elif len(y[0]["chem"]) == n:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
                telebot.types.InlineKeyboardButton('Generate Result', callback_data='gen_result')
        )
        bot.edit_message_text("`Revision Finished !!`",
            m.chat.id, message_id=y[0][str(m.chat.id)], reply_markup=keyboard,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

## '''Function That Manages The Message Sent on Pressing An Options and Detects The Answer'''
def chem_message(m):
    if data == 'ca' or data =='cb' or data=='cc'or data=='cd':
        y = [x for x in users if str(m.chat.id) in x.keys()]
        try:
            bot.delete_message(m.chat.id, message_id=y[0]["cphoto"])
        except:
            pass
        if data == "c" + corr_opt:
            pg = "Correct Answer !!"
            bot.edit_message_text(pg,
                m.chat.id, message_id=y[0][str(m.chat.id)],
                reply_markup=chem_key(pg, m),
                parse_mode=telegram.ParseMode.MARKDOWN
            )
            my_opt = f"{data[1].upper()}"
            correct_opt = my_opt
            cscore_dict = {"qno":qno, "question":question, "my_opt":my_opt, "correct_opt":correct_opt, "marks":1, "emoji":"✔️"}
            y[0]["score"]["cscore"].append(cscore_dict)
        else:
            pg = "Wrong Answer !!"
            bot.edit_message_text(pg,
                m.chat.id, message_id=y[0][str(m.chat.id)],
                reply_markup=chem_key(pg, m),
                parse_mode=telegram.ParseMode.MARKDOWN
            )

            correct_opt = f"{corr_opt.upper()}"
            my_opt = f"{data[1].upper()}"
            cscore_dict = {"qno":qno, "question":question, "my_opt":my_opt, "correct_opt":correct_opt, "marks":0, "emoji":"❌"}
            y[0]["score"]["cscore"].append(cscore_dict)
    else:
        pass

## '''Function That Manages Keyboard Layout after Option is Chosen'''
def chem_key(pg, m):
    y = [x for x in users if str(m.chat.id) in x.keys()]
    if len(y[0]["chem"]) < n:
        if data == corr_opt:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Next', callback_data='chemistry'),
                telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
            )
            return keyboard
        else:
            keyboard = telebot.types.InlineKeyboardMarkup()
            keyboard.row(
                telebot.types.InlineKeyboardButton('Next', callback_data='chemistry'),
                telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
            )
            return keyboard
    elif len(y[0]["chem"]) == n:
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Submit', callback_data='chemistry'),
            telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
        )
        if len(y[0]['maths']) != n:
            keyboard.row(
                telebot.types.InlineKeyboardButton('Continue to Maths', callback_data='maths')
            )
        else:
            pass
        if len(y[0]['phy']) != n:
            keyboard.row(
                telebot.types.InlineKeyboardButton('Continue to Physics', callback_data='physics')
            )
        else:
            pass
        keyboard.row(
            telebot.types.InlineKeyboardButton('Generate Result', callback_data='gen_result')
        )
        return keyboard
    else:
        pass


# Function To Update Messages Other Than That of Questions
def update_message(m):
    y = [x for x in users if str(m.chat.id) in x.keys()]
    if data.startswith("num"):
        pg = "Choose A Subject !!"
        bot.edit_message_text(pg,
            m.chat.id, message_id=y[0][str(m.chat.id)],
            reply_markup=update_keyboard(pg),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    elif data == 'start':
        pg = "Choose Number of Questions Per Subject !!"
        bot.edit_message_text(pg,
            m.chat.id, message_id=y[0][str(m.chat.id)],
            reply_markup=update_keyboard(pg),
            parse_mode=telegram.ParseMode.MARKDOWN
        )
    elif data == 'closestart':
        bot.delete_message(m.chat.id, message_id=y[0][str(m.chat.id)])
    else:
        pass

# Function To Manage Changes in Keyboards of Messages other than that of Questions
def update_keyboard(pg):
    if data == 'start':
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('5', callback_data='num5'),
            telebot.types.InlineKeyboardButton('10', callback_data='num10'),
            telebot.types.InlineKeyboardButton('15', callback_data='num15'),
            telebot.types.InlineKeyboardButton('20', callback_data='num20'),
            telebot.types.InlineKeyboardButton('25', callback_data='num25'),
            telebot.types.InlineKeyboardButton('30', callback_data='num30')
        )     
        return keyboard   
    elif data.startswith("num"):
        keyboard = telebot.types.InlineKeyboardMarkup()
        keyboard.row(
            telebot.types.InlineKeyboardButton('Maths', callback_data='maths')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Physics', callback_data='physics')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('Chemistry', callback_data='chemistry')
        )
        keyboard.row(
            telebot.types.InlineKeyboardButton('❌ Close ❌', callback_data='closestart')
        )
        return keyboard
    else:
        pass

# Query Handler - Converts Callback Data into Queries that can be inferred By Other Functions
@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    global data
    data = query.data
    get_callback(query)

# Bot Polling - Prevents Python Script from Stopping 
bot.polling(none_stop=True)