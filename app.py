import logging
from random import randint
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

scoredict = {}

def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Hi, {update.effective_user.first_name}!')
    

def rockpaperscissors(update, context):
    query = update.callback_query
    #replies the query
    query.answer()
    #create a list of play options
    t = ["Rock", "Paper", "Scissors"]
    #assign a random play to the computer
    computer = t[randint(0,2)]
    #receives the player choice
    player = query.data
    #edits the inline keyboard to the player choice
    query.edit_message_text(text="You choose: {}".format(query.data))
    #displays the computer choice
    query.message.reply_text(f"{computer}!")
    #defines the winner and prints result
    if  player == computer:
        query.message.reply_text("Tie!")
    elif player == "Rock":
        if computer == "Paper":
            query.message.reply_text(f"You lose! {computer} covers {player}")
            scorefun(f"{query.message.chat_id}", False, update, context)
        else:
            query.message.reply_text(f"You win! {player} smashes {computer}")
            scorefun(f"{query.message.chat_id}", True, update, context)
    elif player == "Paper":
        if computer == "Scissors":
            query.message.reply_text(f"You lose! {computer} cut {player}")
            scorefun(f"{query.message.chat_id}", False, update, context)
        else:
            query.message.reply_text(f"You win! {player} covers {computer}")
            scorefun(f"{query.message.chat_id}", True, update, context)
    elif player == "Scissors":
        if computer == "Rock":
            query.message.reply_text(f"You lose... {computer} smashes {player}")
            scorefun(f"{query.message.chat_id}", False, update, context)
        else:
            query.message.reply_text(f"You win! {player} cut {computer}")
            scorefun(f"{query.message.chat_id}", True, update, context)
      
def game(update, context):
    keyboard = [[InlineKeyboardButton("Rock", callback_data='Rock'),
                 InlineKeyboardButton("Paper", callback_data='Paper')],

                [InlineKeyboardButton("Scissors", callback_data='Scissors')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def stats(update, context):
    global scoredict
    if not update.message.chat_id == 23742393:
        update.message.reply_text("Restricted")
        return
    update.message.reply_text(scoredict)

    
def scorefun(chat_id, win, update, context):
    global scoredict
    if not f"{chat_id}" in scoredict:
       scoredict [f"{chat_id}"] = 0
    elif win == True:
        scoredict [f"{chat_id}"] +=1
        if scoredict[f"{chat_id}"] == 3:
            context.bot.send_sticker(chat_id=update.effective_chat.id, sticker="CAACAgEAAxkBAAJcOF6ZCXw7kKreAcrND7_phWGowkRcAAIKAQACU0ekCfR8ymMnU9oqGAQ")
            scoredict [f"{chat_id}"] = 0
        return
    scoredict [f"{chat_id}"] -=1
    if scoredict [f"{chat_id}"] == -3:
        context.bot.send_sticker(chat_id=update.effective_chat.id, sticker="CAACAgMAAxkBAAJcNV6Y9KiGDz-KhyFImkbTwMNDgC9xAALXAANTR6QJyiuP9myQG3EYBA")
        scoredict [f"{chat_id}"] = 0    


def main():
    """Start the bot."""
    updater = Updater("", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("game", game))
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CallbackQueryHandler(rockpaperscissors))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()