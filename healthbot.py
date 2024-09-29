import telebot
import sqlite3
import os
import csv

connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()
TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)
def find_abbr(message):
    try:
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM abr WHERE name = ?",(message.text.lower(),)).fetchall()
        return rows[0][1]
    except:
        bot.send_message(message.from_user.id,'Данная аббревиатура не зарегистрирована')    

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    decod_abr = find_abbr(message)
    bot.send_message(message.from_user.id, decod_abr)    

table_name = 'abr'
file_path = '/data/input.csv'
file_name = 'data/input.csv'
if not(os.path.isfile(file_path)):
    os.write(2,'Файл не найден'.encode('utf-8'))
    quit()

cursor.execute('''CREATE TABLE IF NOT EXISTS abr(
        name TEXT NOT NULL,
        decode TEXT NOT NULL)
        ''')
import fileinput

for line in fileinput.input(file_name, inplace=1):
    print(line.lower(), end='') 
cursor.execute('DELETE FROM abr WHERE name = name ')
file = open(file_name,encoding='utf-8')
contents = csv.reader(file)
insert_records = "INSERT INTO abr(name,decode) VALUES(?, ?)"
cursor.executemany(insert_records,contents)  
connection.commit()        
cursor.execute('DELETE FROM abr WHERE name = name')
bot.polling(none_stop=True, interval=5)
connection.close()