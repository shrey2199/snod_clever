from config import Config
import psycopg2
import telebot
import logging
from datetime import datetime
import pytz

# CONFIG
from config import Config

BOT_TOKEN = Config.BOT_TOKEN
DATABASE_URI = Config.DATABASE_URI

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

'''DATABASE FUNCTIONS'''

def dbcheck(m):
    '''Connecting with URI'''
    conn = psycopg2.connect(DATABASE_URI)

    '''Creating Cursor'''
    cur = conn.cursor()

    '''Fetch Data From Table'''
    cmd = "SELECT tg_id, name FROM revise ORDER BY name"
    cur.execute(cmd)
    rows = cur.fetchall()
    rows_list = [list(row) for row in rows]

    if len(rows_list) != 0:
        mes_str = ''
        for row in rows_list:
            mes_str += (f"{row[0]} - {row[1]}\n")
    else:
        mes_str = 'No Entries Found !'

    '''Close Cursor'''
    cur.close()

    '''Send Message'''
    bot.send_message(m.chat.id, mes_str)

def db_createtable():
    '''Connecting with URI'''
    conn = psycopg2.connect(DATABASE_URI)

    '''Creating Cursor'''
    cur = conn.cursor()

    '''Create A Table Revise'''
    cmd = "create table if not exists revise(serial_id SERIAL PRIMARY KEY, tg_id INTEGER NOT NULL, name VARCHAR(255) NOT NULL, username VARCHAR, password VARCHAR)"
    cur.execute(cmd)
    conn.commit()

    '''Create A Table Results'''
    cmd = "create table if not exists results(serial_id SERIAL , tg_id INTEGER NOT NULL, datetime VARCHAR, phy VARCHAR, chem VARCHAR, maths VARCHAR, total_marks VARCHAR)"
    cur.execute(cmd)
    conn.commit()

    '''Close Cursor'''
    cur.close()

def db_id_not_exist(m, table='revise'):
    '''Connecting with URI'''
    conn = psycopg2.connect(DATABASE_URI)

    '''Creating Cursor'''
    cur = conn.cursor()

    '''Fetch Data From Table'''
    cmd = f"SELECT tg_id, name FROM {table} WHERE tg_id = {int(m.chat.id)}"
    cur.execute(cmd)
    rows = cur.fetchall()
    rows_list = [list(row) for row in rows]

    '''Close Cursor'''
    cur.close()

    '''Return Values'''
    if len(rows_list) == 0:
        return 1
    else:
        return 0

def db_adddetails(m, name):
    '''Connecting with URI'''
    conn = psycopg2.connect(DATABASE_URI)

    '''Creating Cursor'''
    cur = conn.cursor()

    if db_id_not_exist(m):
        '''Insert Data In Table'''
        tg_id = m.chat.id
        cmd = "INSERT INTO revise(tg_id, name, username, password) VALUES(%s,%s,%s,%s)"
        cur.execute(cmd, (tg_id, name, tg_id, name))
        conn.commit()
    else:
        pass

    '''Close Cursor'''
    cur.close()

def db_get_details(m):
    '''Connecting with URI'''
    conn = psycopg2.connect(DATABASE_URI)

    '''Creating Cursor'''
    cur = conn.cursor()

    '''Fetch Data From Table'''
    cmd = f"SELECT * FROM revise WHERE tg_id = {int(m.chat.id)}"
    cur.execute(cmd)
    rows = cur.fetchone()

    '''Close Cursor'''
    cur.close()

    return rows

def db_add_result(m, purl, murl, curl, total):
    name = db_get_details(m)
    dt = datetime.now(pytz.timezone('Asia/Kolkata'))
    tg_id = m.chat.id

    '''Connecting with URI'''
    conn = psycopg2.connect(DATABASE_URI)

    '''Creating Cursor'''
    cur = conn.cursor()

    '''Insert Data In Table'''
    cmd = "INSERT INTO results(tg_id, datetime, phy, chem, maths, total_marks) VALUES(%s,%s,%s,%s,%s,%s)"
    cur.execute(cmd, (tg_id, str(dt), str(purl), str(curl), str(murl), str(total)))
    conn.commit()

    '''Close Cursor'''
    cur.close()

def db_update_user(m, username):
    '''Connecting with URI'''
    conn = psycopg2.connect(DATABASE_URI)

    '''Creating Cursor'''
    cur = conn.cursor()

    '''Insert Data In Table'''
    cmd = """UPDATE revise
                SET username = %s
                WHERE tg_id = %s"""
    cur.execute(cmd, (username, str(m.chat.id)))
    conn.commit()

    '''Close Cursor'''
    cur.close()

def db_update_pass(m, password):
    '''Connecting with URI'''
    conn = psycopg2.connect(DATABASE_URI)

    '''Creating Cursor'''
    cur = conn.cursor()

    '''Insert Data In Table'''
    cmd = """UPDATE revise
                SET password = %s
                WHERE tg_id = %s"""
    cur.execute(cmd, (password, str(m.chat.id)))
    conn.commit()

    '''Close Cursor'''
    cur.close()
