# TelegramAssistantBot
A telegram bot that can be used as a personal assistant, for keeping tasks and sending reminders.

My Bot is called Zenigata.

Commands:
- \add <Task> adds a new task to the list.
- \done <number> marks a task corresponding to number as Done.
- \list shows the current tasks (both to do and done)
- \delete <number> deletes the tasks from the list.

# Notes

If you want to fork this repo and make changes, I suggest to launch this line after cloning:

'''
git rm --cached tasks.json
'''

In this way you will have a tasks.json file correctly initialized but remote repository won't see the changes in all the tasks.


