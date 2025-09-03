import logging
import json
import csv
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes      

# get this from BotFather on Telegram
from dotenv import load_dotenv
import os
load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

TASKS_FILE = "tasks.json"

# Logging configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# Helper functions to load and save tasks
def load_tasks():
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)
        
# Command handlers
# I use async and await to make the bot non-blocking
# which means that it can handle multiple requests at the same time,
# i.e. if two users send a command at the same time, it will handle both
# without waiting for one to finish before starting the other.
# In addition, if a user sends a command that takes a long time to process,
# the bot can still respond to other commands from the same user or other users.

# For every command, I define an async function that takes two arguments:
# - update: contains information about the incoming update (message, user, chat, etc.)
# - context: contains information about the context of the command (bot, job queue, etc.)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi! I’m Zenigata, your To-Do Bot.\n"
        "• /add <task> → add new task\n"
        "• /list → show tasks\n"
        "• /done <number> → mark task as done\n"
        "• /delete <number> → delete task\n"
        "• /clean → delete all completed tasks\n"
        "• /help → show this help message\n"
    )
    
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    task_text = " ".join(context.args)
    if not task_text:
        await update.message.reply_text("⚠️ Usage: /add <task>")
        return

    tasks = load_tasks()
    tasks.append({"task": task_text, "done": False, "created": str(datetime.now())})
    save_tasks(tasks)

    await update.message.reply_text(f"✅ Added: {task_text}")
    
async def list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    if not tasks:
        await update.message.reply_text("📭 No tasks found. Use /add to create a new task.")
        return

    message = "📝 Your Tasks:\n"
    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        message += f"{i}. {status} {task['task']}\n"

    await update.message.reply_text(message)
    
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    try:
        task_number = int(context.args[0]) - 1
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Usage: /done <integer>")
        return

    tasks = load_tasks()
    if task_number < 0 or task_number >= len(tasks):
        await update.message.reply_text("⚠️ Invalid task number.")
        return

    tasks[task_number]["done"] = True
    tasks[task_number]["completed"] = str(datetime.now())
    save_tasks(tasks)

    await update.message.reply_text(f"✅ Marked as done: {tasks[task_number]['task']}")
    
async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        task_number = int(context.args[0]) - 1
    except (IndexError, ValueError):
        await update.message.reply_text("⚠️ Usage: /delete <integer>")
        return

    tasks = load_tasks()
    if task_number < 0 or task_number >= len(tasks):
        await update.message.reply_text("⚠️ Invalid task number.")
        return

    removed_task = tasks.pop(task_number)
    save_tasks(tasks)

    await update.message.reply_text(f"🗑️ Deleted: {removed_task['task']}")
    
async def clean(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tasks = load_tasks()
    tasks = [task for task in tasks if not task["done"]]
    save_tasks(tasks)
    await update.message.reply_text("🧹 Cleaned up completed tasks.")
    
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n"
        "• /add <task> → add new task\n"
        "• /list → show tasks\n"
        "• /done <number> → mark task as done\n"
        "• /delete <number> → delete task\n"
        "• /clean → delete all completed tasks\n"
        "• /help → show this help message\n"
    )
    
    
# MAIN
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("list", list))
    application.add_handler(CommandHandler("done", done))
    application.add_handler(CommandHandler("delete", delete))
    application.add_handler(CommandHandler("clean", clean))
    application.add_handler(CommandHandler("help", help))
    
    application.run_polling()
    
if __name__ == "__main__":
    main()
