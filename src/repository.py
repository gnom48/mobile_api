from .database.orm import new_session
from .database.models import *
from .api.models import *
from sqlalchemy import select, update, delete, and_


class Repository:
    """Класс репозиторий для работы с базой данных как с объектом"""

    # -------------------------- users --------------------------


    @classmethod
    async def registrate_user(cls, data: User) -> bool:
        async with new_session() as session:
            try:
                new_user = UserOrm(**data.model_dump())
                new_user.type = UserTypesOrm[data.type.name]
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
                #new_note.date_time = int(datetime.now() - datetime(1970, 1, 1).total_seconds())
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
            

    # -------------------------- tasks --------------------------
    

    @classmethod
    async def update_statistics(cls, user_id: int, statistic: str, addvalue: int) -> bool:
        async with new_session() as session:
            try:
                statistic_to_edit: DayStatisticsOrm = await session.get(DayStatisticsOrm, user_id)
                print(user_id, statistic, addvalue)
                print(statistic_to_edit.meets)
                match statistic:
                    case WorkTasksTypesOrm.FLYERS.value:
                        statistic_to_edit.flyers += addvalue
                    case WorkTasksTypesOrm.CALLS.value:
                        statistic_to_edit.calls += addvalue
                    case WorkTasksTypesOrm.SHOW.value:
                        statistic_to_edit.shows += addvalue
                    case WorkTasksTypesOrm.MEET.value:
                        print(1000)
                        statistic_to_edit.meets += addvalue
                    case WorkTasksTypesOrm.DEAL.value:
                        statistic_to_edit.deals += addvalue
                    case WorkTasksTypesOrm.DEPOSIT.value:
                        statistic_to_edit.deposits += addvalue
                    case WorkTasksTypesOrm.SEARCH.value:
                        statistic_to_edit.searches += addvalue
                    case WorkTasksTypesOrm.ANALYTICS.value:
                        statistic_to_edit.analytics += addvalue
                    case _:
                        print(-1000)
                        statistic_to_edit.others += addvalue
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
