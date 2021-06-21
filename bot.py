# Telegram bot modules
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup, ForceReply

# System modules
import os
import sys
import time

# Our module
import main as m

### GLOBAL DATA ###

# Initialize the university data
data = m.init_data()    # The whole data frame of univsersities
probs = {}              # Current probabilites (diff for each usr)
usedQ = {}              # Which questions have already been answered
idx_q = {}              # The index of the current active question

# Possible answers and their associated key (to be used in the main module)
poss_ans = {
        '🟢   It is a must!' : 4,
        '🔵   Would be fine' : 3,
        '🟡   I don\'t care' : 2,
        '🟠   I\'d rather not' : 1,
        '🔴   Absolutely not!' : 0
        }

# Help message
help_mes = '''
List of possible commands:
/start: Start a new round.
/help: Get this help message.
/instr: Tell me how all of this works!
/repeat: Say the last question again (if unanswered)
'''

# Instructions message
instr_mes = '''
Hi! I am here to help you find a university for your future mobility stay.

I am going to ask a series of questions that will help me to make the best suggestions for you 😃.
For each question, you just need to choose the answer that best captures your feeling. For example, if I ask _Do you prefer staying in Europe?_ and you really want to stay in Europe, choose _It is a must!_. Easy! So let's go. Just type (or click!) the /start command again.
'''


### BOT FUNCTIONS ###

# Simple start function.
def start(update: Update, context: CallbackContext) -> None:
    message = 'Welcome! Let\'s find out your best choice for your stay abroad 😊\nYou can use the buttons below to interact.📲'
    ans_keyboard = [[KeyboardButton('Take quiz'), KeyboardButton('Instructions'), KeyboardButton('Help')]]
    reply_kb_markup = ReplyKeyboardMarkup(ans_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(message, reply_markup=reply_kb_markup)

    # Initialize the info for the user
    usr_id = update.message.from_user["id"]
    global probs
    global usedQ
    global idx_q
    probs[usr_id] = m.init_priors(data)
    usedQ[usr_id] = m.init_usedQ(data)
    idx_q[usr_id] = None


# Help function
def helpfun(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(help_mes)


# Instruction function
def instr(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(instr_mes, parse_mode="Markdown")


# Repeat function
def repeat(update: Update, context: CallbackContext) -> None:
    usr_id = update.message.from_user["id"]
    if not usr_id in idx_q or idx_q[usr_id] is None:
        update.message.reply_text('There was no active question')
        helpfun(update, context)
        return

    # If there was a previous question, repeat it
    send_question(update, context, m.get_question(data, idx_q[usr_id]))


# Sends the top results to the user in the appropriate format
def send_results(update, context, top_list):
    for i, uni in enumerate(top_list):
        message = f"Ranked number {i+1}:\n" + uni
        update.message.reply_text(message, parse_mode="Markdown")


# Sends the given question to the user with the answers keyboard
def send_question(update, context, question):
    names = list(poss_ans.keys())
    ans_keyboard = [[KeyboardButton(names[0]), KeyboardButton(names[4])],[KeyboardButton(names[1]), KeyboardButton(names[2]), KeyboardButton(names[3])]]
    reply_kb_markup = ReplyKeyboardMarkup(ans_keyboard, resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(question+'?', reply_markup=reply_kb_markup)


# Provisional question function, asks question and expects answer
def questions(update, context):
    usr_id = update.message.from_user["id"]
    global usedQ
    global idx_q

    # Check user data has been initialized
    if not usr_id in idx_q:
        update.message.reply_text('Remember to do /start before the start of a new round!')
        return


    if not m.finished(probs[usr_id], usedQ[usr_id]):

        # Choose next question and ask it
        idx_q[usr_id], usedQ[usr_id] = m.next_question(data, usedQ[usr_id], probs[usr_id])
        send_question(update, context, m.get_question(data, idx_q[usr_id]))
    else:
        update.message.reply_text('*Here are your results!*', parse_mode='Markdown')
        time.sleep(2)
        # Print the results
        top_list = m.best_options(data, probs[usr_id])
        send_results(update, context, top_list)

        # Print goodbye and reset
        del idx_q[usr_id] # Delete entry of user
        update.message.reply_text('Thank you 👌 You can use /start to take another quiz 🌍')


# Get all input from user and act accordingly
def answer(update: Update, context: CallbackContext) -> None:
    usr_id = update.message.from_user["id"]
    text = update.message.text

    # Check for basic commands at start
    if text == 'Take quiz':
        if usr_id in idx_q and idx_q[usr_id] is not None:
            # If someone types it in the middle of a question
            update.message.reply_text(help_mes)
            return
        questions(update, context)
        return
    if text == 'Instructions':
        instr(update,context)
        return
    if text == 'Help':
        helpfun(update,context)
        return
    # Else assume it is an answer

    # If the user had no active question, assume it is a mistake
    if not usr_id in idx_q or idx_q[usr_id] is None:
        update.message.reply_text(help_mes)
        return

    text = update.message.text
    if text not in poss_ans:
        update.message.reply_text('Not a valid answer. Type /repeat to repeat the previous question')
        return

    global probs
    # Else is a valid answer, update posteriors
    probs[usr_id] = m.update_posteriors(data, probs[usr_id], idx_q[usr_id], poss_ans[text])
    questions(update,context)



### BOT SETUP ###

# Read the bot token from the local file
with open(os.path.join(sys.path[0], 'token.txt'),'r') as t:
    token = t.read().strip()
updater = Updater(token)

# Define possible commands
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', helpfun))
updater.dispatcher.add_handler(CommandHandler('instr', instr))
updater.dispatcher.add_handler(CommandHandler('repeat', repeat))

# If gets a message that is not a command, assume it is an answer
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, answer))


# Start the bot
updater.start_polling()
updater.idle()

