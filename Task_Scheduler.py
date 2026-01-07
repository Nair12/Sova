

from Notify import ask_mood_notification



def add_mood_notification_sub(scheduler,bot,chat_id):
    scheduler.add_job(
        ask_mood_notification,
        trigger="cron",
        hour=14,
        minute=0,
        args=(bot, chat_id),
        id=f"daily_{chat_id}",
        replace_existing=True
    )




def remove_mood_notification_sub(scheduler,bot,chat_id):
    scheduler



