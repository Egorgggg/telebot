import telebot
import sqlite3
import os
import csv
import chardet
import codecs
import fileinput

global password_real
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()
TOKEN = os.environ["TOKEN"]
password_real = os.environ['PASSWORD']
bot = telebot.TeleBot(TOKEN)
def decoding(file_path):
    with open(file_path, mode='rb') as file:
        f = file.read()
    encoding_result = chardet.detect(f)
    encoding = encoding_result['encoding']
    print(encoding)          
    if encoding != 'utf-8':
        BLOCKSIZE = 1048576
        with codecs.open(file_path, "r",encoding) as sourceFile:
            with codecs.open('data/input_new.csv', "wb", 'utf-8') as targetFile:
                while True:
                    contents = sourceFile.read(BLOCKSIZE)
                    if not contents:
                        break
                    targetFile.write(contents)
        lowing('data/input_new.csv')
        create_table('abr','data/input_new.csv')
        

def lowing(file_name):
    for line in fileinput.input(file_name, inplace=1):
        print(line.lower(), end='')

def find_abbr(message):
    try:
        connection = sqlite3.connect('my_database.db',timeout=10.0)
        cursor = connection.cursor()
        rows = cursor.execute("SELECT * FROM abr WHERE name = ?",(message.text.lower(),)).fetchall()
        return rows[0][1]
    except:
        bot.send_message(message.from_user.id,'Данная аббревиатура не зарегистрирована')    

def renaming(original_name,new_name):
    try:
        os.rename(original_name,new_name)
    except:
        my_file = open(original_name,'w+')
        my_file.write('xc')
        my2 = open(new_name,'w+')
        my2.write('xc')
        
def opening(file,type,message,downloaded_file):
    try:
        with open(file,type) as new_file:
            type(new_file)
            new_file.write(downloaded_file)
            return new_file
    except:
        bot.send_message(message.from_user.id,"Не подходящий файл(проверьте формат или содержимое)")


@bot.message_handler(content_types=['text'])
def get_text_messages(message): 
    decod_abr = find_abbr(message)
    bot.send_message(message.from_user.id, decod_abr)   

@bot.message_handler(content_types= ['document'])
def input_file(message):
    global password
    password = message.text
    if password == password_real:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'data/tele_input.csv'
        try:
            with open(src,'wb') as new_file:
                bot.reply_to(message, "Пожалуй, я сохраню это")
                new_file.write(downloaded_file)
        except:
            bot.send_message(message.from_user.id,"Не подходящий файл(проверьте формат или содержимое)")

        decoding(src)  
        try:
            os.remove('data/input_old.csv')
        except:
            my_file = open('data/input_old.csv','w+')
            my_file.write('xc,joke')    
        renaming('data/input.csv','data/input_old.csv')    
        renaming('data/input_new.csv','data/input.csv')
    else:
        bot.send_message(message.from_user.id,"Неверный пароль")

def create_table(table_name,file_path):
    connection = sqlite3.connect('my_database.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS abr(
        name TEXT NOT NULL,
        decode TEXT NOT NULL)
        ''')
    cursor.execute(f'DELETE FROM {table_name} WHERE name = name')
    file = open(file_path,encoding='utf-8')
    contents = csv.reader(file)
    insert_records = f"INSERT INTO {table_name}(name,decode) VALUES(?, ?)"
    cursor.executemany(insert_records,contents)  
    connection.commit()
    connection.close()

table_name = 'abr'
file_path = 'data/input.csv'
file_name = 'data/input.csv'
decoding(file_name)
cursor.execute('''CREATE TABLE IF NOT EXISTS abr(
        name TEXT NOT NULL,
        decode TEXT NOT NULL)
        ''')
cursor.execute('DELETE FROM abr WHERE name = name ')
file = open('data/input.csv',encoding='utf-8')  
contents = csv.reader(file)        
insert_records = "INSERT INTO abr(name,decode) VALUES(?, ?)"
cursor.executemany(insert_records,contents)  
connection.commit()        
cursor.execute('DELETE FROM abr WHERE name = name')
connection.close()
bot.polling(none_stop=True, interval=5)