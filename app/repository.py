from .database.orm import new_session
from sqlalchemy.sql import text
from .database.models import *
from .api.models import *
import time
from sqlalchemy import select, update, delete, and_


class Repository:
    """Класс репозиторий для работы с базой данных как с объектом"""

    # -------------------------- config --------------------------

    @classmethod
    async def get_config(cls) -> str:
        async with new_session() as session:
            try:
                req = text("SELECT version() AS db_version;")
                result = await session.execute(req)
                version = result.scalars().first()
                req = text("SELECT now() AS db_datetime;")
                result = await session.execute(req)
                ntime = result.scalars().first()
                return (version, ntime)
            except:
                return None

    # -------------------------- users --------------------------


    @classmethod
    async def registrate_user(cls, data: User) -> bool:
        async with new_session() as session:
            try:
                new_user = UserOrm(**data.model_dump())
                new_user.type = UserTypesOrm[data.type.name]
                new_user.reg_date = int(time.time())
                new_user.id = None
                session.add(new_user)
                await session.flush()
            except:
                return False
            
            day_stats = DayStatisticsOrm()
            day_stats.user_id = new_user.id
            week_stats = WeekStatisticsOrm()
            week_stats.user_id = new_user.id
            month_stats = MonthStatisticsOrm()
            month_stats.user_id = new_user.id
            session.add(day_stats)
            session.add(week_stats)
            session.add(month_stats)

            await session.commit()
            return True
        

    @classmethod
    async def edit_user(cls, data: User) -> bool:
        async with new_session() as session:
            try:
                old_user = await session.get(UserOrm, data.id)
                old_user.type = UserTypesOrm[data.type.name]
                old_user.birthday = data.birthday
                old_user.gender = data.gender
                old_user.login = data.login
                old_user.password = data.password
                old_user.name = data.name
                old_user.phone = data.phone
                old_user.photo = data.photo
                await session.flush()
            except:
                return False
            await session.commit()
            return True
        

    @classmethod
    async def get_user_by_id(cls, id: int) -> UserOrm:
        async with new_session() as session:
            try:
                res = await session.get(UserOrm, id)
                return res
            except:
                return None
                
                
    @classmethod
    async def get_user_statistics(cls, id: int) -> StatisticsOrm:
        async with new_session() as session:
            try:
                res = await session.get(StatisticsOrm, id)
                return res
            except:
                return None
                
                
    @classmethod
    async def get_user_by_login(cls, login: str, password: str) -> UserOrm:
        async with new_session() as session:
            try:
                query = select(UserOrm).where(UserOrm.login == login).where(UserOrm.password == password)
                r = await session.execute(query)
                return r.scalar()
            except:
                return None
                

    # -------------------------- notes --------------------------

                
    @classmethod
    async def get_all_notes_by_user_id(cls, user_id: int) -> list[NoteOrm]:
        async with new_session() as session:
            try:
                query = select(NoteOrm).where(NoteOrm.user_id == user_id)
                r = await session.execute(query)
                return r.scalars().all()
            except:
                return None


    @classmethod
    async def add_note(cls, data: Note) -> int:
        async with new_session() as session:
            try:
                new_note = NoteOrm(**data.model_dump())
                new_note.id = None
                session.add(new_note)
                await session.flush()
                note_id = new_note.id
                await session.commit()
                return note_id
            except:
                return None


    @classmethod
    async def del_note(cls, id: int) -> bool:
        async with new_session() as session:
            try:
                note_to_del = await session.get(NoteOrm, id)
                await session.delete(note_to_del)
                await session.commit()
                return True
            except:
                return False
                
    
    @classmethod
    async def edit_note(cls, data: Note) -> bool:
        async with new_session() as session:
            try:
                note_to_edit = await session.get(NoteOrm, data.id)
                note_to_edit.title = data.title
                note_to_edit.desc = data.desc
                note_to_edit.date_time = data.date_time
                await session.commit()
                return True
            except:
                return False


    # -------------------------- tasks --------------------------

                
    @classmethod
    async def get_all_tasks_by_user_id(cls, user_id: int) -> list[TaskOrm]:
        async with new_session() as session:
            try:
                query = select(TaskOrm).where(TaskOrm.user_id == user_id)
                r = await session.execute(query)
                return r.scalars().all()
            except:
                return None


    @classmethod
    async def add_task(cls, data: Task) -> int:
        async with new_session() as session:
            try:
                new_task = TaskOrm(**data.model_dump())
                new_task.id = None
                new_task.work_type = data.work_type.name
                session.add(new_task)
                await session.flush()
                task_id = new_task.id
                await session.commit()
                return task_id
            except:
                return None


    @classmethod
    async def del_task(cls, id: int) -> bool:
        async with new_session() as session:
            try:
                task_to_del = await session.get(TaskOrm, id)
                await session.delete(task_to_del)
                await session.commit()
                return True
            except:
                return False
            

    # -------------------------- statistics --------------------------
    

    @classmethod
    async def update_statistics(cls, user_id: int, statistic: str, addvalue: int) -> bool:
        async with new_session() as session:
            try:
                day_statistic_to_edit: DayStatisticsOrm = await session.get(DayStatisticsOrm, user_id)
                week_statistic_to_edit: WeekStatisticsOrm = await session.get(WeekStatisticsOrm, user_id)
                month_statistic_to_edit: MonthStatisticsOrm = await session.get(MonthStatisticsOrm, user_id)
                print(user_id, statistic, addvalue)
                print(day_statistic_to_edit.meets)
                match statistic:
                    case WorkTasksTypesOrm.FLYERS.value:
                        day_statistic_to_edit.flyers += addvalue
                        week_statistic_to_edit.flyers += addvalue
                        month_statistic_to_edit.flyers += addvalue
                    case WorkTasksTypesOrm.CALLS.value:
                        day_statistic_to_edit.calls += addvalue
                        week_statistic_to_edit.calls += addvalue
                        month_statistic_to_edit.calls += addvalue
                    case WorkTasksTypesOrm.SHOW.value:
                        day_statistic_to_edit.shows += addvalue
                        week_statistic_to_edit.shows += addvalue
                        month_statistic_to_edit.shows += addvalue
                    case WorkTasksTypesOrm.MEET.value:
                        day_statistic_to_edit.meets += addvalue
                        week_statistic_to_edit.meets += addvalue
                        month_statistic_to_edit.meets += addvalue
                    case WorkTasksTypesOrm.DEAL.value:
                        day_statistic_to_edit.deals += addvalue
                        week_statistic_to_edit.deals += addvalue
                        month_statistic_to_edit.deals += addvalue
                    case WorkTasksTypesOrm.DEPOSIT.value:
                        day_statistic_to_edit.deposits += addvalue
                        week_statistic_to_edit.deposits += addvalue
                        month_statistic_to_edit.deposits += addvalue
                    case WorkTasksTypesOrm.SEARCH.value:
                        day_statistic_to_edit.searches += addvalue
                        week_statistic_to_edit.searches += addvalue
                        month_statistic_to_edit.searches += addvalue
                    case WorkTasksTypesOrm.ANALYTICS.value:
                        day_statistic_to_edit.analytics += addvalue
                        week_statistic_to_edit.analytics += addvalue
                        month_statistic_to_edit.analytics += addvalue
                    case _:
                        day_statistic_to_edit.others += addvalue
                        week_statistic_to_edit.others += addvalue
                        month_statistic_to_edit.others += addvalue
                await session.commit()
                return True
            except:
                return False
            
    
    @classmethod
    async def get_statistics_by_period(cls, user_id: int, period: str) -> Statistics:
        async with new_session() as session:
            try:
                match period:
                    case StatisticPeriods.DAY_STATISTICS_PERIOD:
                        return await session.get(DayStatisticsOrm, user_id)
                    case StatisticPeriods.WEEK_STATISTICS_PERIOD:
                        return await session.get(WeekStatisticsOrm, user_id)
                    case StatisticPeriods.MONTH_STATISTICS_PERIOD:
                        return await session.get(MonthStatisticsOrm, user_id)
                    case _:
                        return None
            except:
                return None
            

    @classmethod
    async def clear_day_statistics():
        async with new_session() as session:
            try:
                for item in session.query(DayStatisticsOrm).all():
                    item.flyers = 0
                    item.calls = 0
                    item.shows = 0
                    item.meets = 0
                    item.deals = 0
                    item.deposits = 0
                    item.searches = 0
                    item.analytics = 0
                    item.others = 0
                session.commit()
            except:
                return

            
    @classmethod
    async def clear_month_statistics():
        async with new_session() as session:
            try:
                for item in session.query(WeekStatisticsOrm).all():
                    item.flyers = 0
                    item.calls = 0
                    item.shows = 0
                    item.meets = 0
                    item.deals = 0
                    item.deposits = 0
                    item.searches = 0
                    item.analytics = 0
                    item.others = 0
                session.commit()
            except:
                return


    @classmethod
    async def clear_month_statistics(): 
        async with new_session() as session:
            try:
                for item in session.query(MonthStatisticsOrm).all():
                    item.flyers = 0
                    item.calls = 0
                    item.shows = 0
                    item.meets = 0
                    item.deals = 0
                    item.deposits = 0
                    item.searches = 0
                    item.analytics = 0
                    item.others = 0
                session.commit()
            except:
                return