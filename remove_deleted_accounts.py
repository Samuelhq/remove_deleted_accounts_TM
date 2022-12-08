import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackQueryHandler, CallbackContext
from telegram.ext.dispatcher import run_async
from telegram.ext.jobqueue import Days

# Your Telegram Bot's API key
API_KEY = "5933995213:AAHExE0_P7C5aYZHLdJbDmhl0jq5sSOXpDc"

# The Telegram group where you want the bot to remove deleted accounts from
GROUP_ID =  -1001575583634

# Create a new Telegram bot
bot = telegram.Bot(token=API_KEY)

# Start the bot and connect to the Telegram API
updater = Updater(bot=bot)
dispatcher = updater.dispatcher

# Define a command handler for the /start command, which prints a greeting
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am RDA_bot, a bot that removes deleted accounts from a Telegram group.")

# Add the command handlers to the dispatcher
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
remove_handler = CommandHandler("remove", remove)
dispatcher.add_handler(remove_handler)
    
    
    # Define a command handler for the /remove command, which removes deleted accounts from the group
def remove(update, context):
    # Get a list of all members of the group
    members = context.bot.get_chat_members_count(chat_id=GROUP_ID)

  # Count how many members have deleted their account
  deleted_accounts = 0
  for member in members:
    if member.user.is_deleted:
      deleted_accounts += 1

  # Send a message to the user with the number of deleted accounts
  context.bot.send_message(chat_id=update.effective_chat.id, text=f"Removed {deleted_accounts} deleted accounts from the group.")

# Define a command handler for the /remove command, which removes deleted accounts from the group
def remove(update, context):
  # Get a list of all members of the group
  members = context.bot.get_chat_members_count(chat_id=GROUP_ID)

  # Loop through each member of the group
  for member in members:
    # If the member's account has been deleted, kick them from the group
    if member.user.is_deleted:
      context.bot.kick_chat_member(chat_id=GROUP_ID, user_id=member.user.id, until_date=0)

# Report how many deleted accounts were removed
report(update, context)

# Create a job that runs every 24 hours to remove deleted accounts from the group
job_queue = updater.job_queue
job = job_queue.run_repeating(remove, interval=Days(1), first=0)

# Start the bot
updater.start_polling()
