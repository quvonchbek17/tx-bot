import asyncio
from calendar import weekday
import logging
from time import timezone
from datetime import datetime, timedelta, timezone
from pprint import pprint as print

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler_di import ContextSchedulerDecorator
# from apscheduler.jobstores.redis import RedisJobStore

from data.config import ADMINS
from loader import dp, db, bot
from middlewares.scheduler import SchedulerMiddleware

from googletrans import Translator
trans = Translator()


logger = logging.getLogger(__name__)

# weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
weekdays = ['dushanba','seshanba','chorshanba','payshanba','juma','shanba','yakshanba']

# qanaqadir ikir-chikir sozlamalar
def register_all_middlewares(scheduler):
    dp.setup_middleware(SchedulerMiddleware(scheduler))


# jadvalni ishga tushuruvchi asosiy funktsiya
async def set_scheduler():
    now = datetime.now(timezone(timedelta(hours=5)))
    scheduler = AsyncIOScheduler(timezone='Asia/Tashkent')
    scheduler.add_job(plan_schedules, 'cron', day_of_week="mon-sun", hour=now.hour, minute=now.minute+1, args=(scheduler,))
    register_all_middlewares(scheduler)
    scheduler.start()
    
    
# foydalanuvchilarga jadvallarini jo'natish
async def send_message_to_users(lessons):
    today = weekdays[datetime.now(timezone(timedelta(hours=5))).weekday()]
    for lesson in lessons:
        user_ids = [user[5] for user in (await db.select_user(group_id=lesson[8]))]
        science = await db.select_science(lesson[0])
        teacher = await db.select_teacher(lesson[0])
        room = await db.select_room(lesson[0])
        start_time = await db.select_start_time(lesson[0])
        # await bot.send_message(chat_id=ADMINS[0],text=str(user_ids))
        for user_id in user_ids:
            language = (await db.select_user(chat_id=user_id))[0][5]
            lesson_text = f"""
{trans.translate('Bugun:',dest=language).text} <b>{trans.translate(today, dest=language).text.capitalize()}</b>

{trans.translate('Science:',dest=language).text} <i>{science}</i>
{trans.translate("O'qituvchi",dest=language).text}:  {teacher}
{trans.translate("Xona",dest=language).text}:  {room}
{trans.translate("Boshlanish vaqti",dest=language).text}:  {start_time}
    """
            # photo_id = 'AgACAgIAAxkBAAIN_2MeLzhSWOBYd8u-rWjlhXkpetd4AAJVvzEbCK3xSJMoeMCw_GY9AQADAgADeQADKQQ'
            # await bot.send_photo(chat_id=user_id, photo=photo_id, caption=lesson_text)
            try:
                await bot.send_message(chat_id=user_id, text=lesson_text)
            except:
                pass
            await asyncio.sleep(0.1)


# adminlarga xabar jo'natish
async def send_message_to_admins():
    for admin_id in ADMINS:
        await bot.send_message(text="Vaqtli xabar", chat_id=admin_id)
    
    
# rejalashtirilgan vaqtga sayqal berish
async def get_run_date(lesson_start_time) -> datetime:
    time = lesson_start_time
    hour, minute = int(time[:time.index(':')]), int(time[time.index(':')+1:])
    now = datetime.now(timezone(timedelta(hours=5)))
    run_time = now.replace(hour=hour, minute=minute) - timedelta(minutes=15)
    return run_time


# kunlik jadvallarni jo'natish uchun rejalashtirish
async def plan_schedules(scheduler):
    today = weekdays[datetime.now(timezone(timedelta(hours=5))).weekday()]
    schedules = await db.select_schedules(day=today)
    start_times = await db.select_time(today)
    for start_time in start_times:
        schedules = await db.select_schedules(day=today,time_id=start_time[0])
        run_date = await get_run_date(start_time[1])
        scheduler.add_job(send_message_to_users, 'date', run_date=run_date,
                        #   end_date=(datetime.now()+timedelta(hours=23)),
                          args=(schedules,))
        await asyncio.sleep(0.1)

    # for schedule in schedules:
    #     lesson_id = schedule[0]
    #     # user_ids = [user[1] for user in (await db.select_user(user_group_id=schedule[6]))]
    #     run_date = await get_run_date(schedule[5])
    #     scheduler.add_job(send_message_to_users, 'date', run_date=run_date,
    #                     #   end_date=(datetime.now()+timedelta(hours=23)),
    #                       args=(lesson_id,))
    #     asyncio.sleep(0.1)


# async def set_scheduled_jobs(scheduler, *args, **kwargs):
#     # Bajarish uchun vazifalar qo'shish
#     scheduler.add_job(send_message_to_admins, "cron", day='this day', hour=14, minute=45)
#     # scheduler.add_job(some_other_regular_task, "interval", seconds=100)




if __name__ == '__main__':
    time = asyncio.run(send_message_to_users())
    print(time)
