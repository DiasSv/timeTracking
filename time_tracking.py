import pymysql
from config import host, user, password, db_name, employee_id, date
from datetime import datetime, timedelta

def get_times_on_day(employee_id: int, date: str, cursor: object) -> list[dict]:
    """
    Gets and processes all events from the database for the day.
    :param employee_id: ``int``
    :param date: Date in string format '%Y-%m-%d', ``str``
    :param cursor: provides an interface for working with the results of a database query,  ``object``
    """
    start_day = datetime.strptime(date, '%Y-%m-%d').replace(hour=9, minute=0, second=0)
    end_day = datetime.strptime(date, '%Y-%m-%d').replace(hour=18, minute=0, second=0)
    query = f'SELECT time, type FROM events WHERE employee_id = {employee_id}'\
            f' AND time >= "{start_day}" AND time <= "{end_day}" ORDER BY time;'
    cursor.execute(query)
    events = cursor.fetchall()
    if len(events) == 0:
        return [{'time': datetime.strptime(date,'%Y-%m-%d'), 'type': 'entrance'}, {'time': datetime.strptime(date,'%Y-%m-%d'), 'type': 'exit'}]
    if events[0].get('type') != 'entrance':
        events.insert(0, {'time': start_day, 'type': 'entrance'})
    if events[-1].get('type') != 'exit':
        events.append({'time': end_day, 'type': 'exit'})
    return events

def get_times_on_week(employee_id: int, date: str, cursor: object) -> list[dict]:
    """
    Gets and processes all events from the database for the workweek.
    :param employee_id: ``int``
    :param date: Date in string format '%Y-%m-%d', ``str``
    :param cursor: provides an interface for working with the results of a database query,  ``object``
    """
    datetime_obj = datetime.strptime(date, "%Y-%m-%d")
    list_hours_on_week = []
    for i in range(4):
        current_day = (datetime_obj - timedelta(datetime_obj.weekday())) + timedelta(i)
        hours_day_in_week = get_times_on_day(employee_id, current_day.strftime('%Y-%m-%d'), cursor)
        list_hours_on_week.append(hours_day_in_week)
    return list_hours_on_week

def get_work_hours_day(events: list[dict]) -> float:
    """
    Processes events, returns working hours per day.
    :param events: A list containing events that are enclosed in dictionaries, ``list[dict]``
    """
    total_work_seconds = 0
    for i in range(0, len(events), 2):
        event_in = events[i]
        event_out = events[i+1]
        work_seconds = (event_out['time'] - event_in['time']).total_seconds()
        total_work_seconds += work_seconds
    return round(total_work_seconds / 3600, 2)

def get_work_hours_week(events_week: list[dict]) -> float:
    """
    Processes events, returns working hours per week.
    :param events: A list containing events that are enclosed in dictionaries, ``list[dict]``
    """
    total_work_hours = 0
    for events in events_week:
        total_work_hours += get_work_hours_day(events)
    return round(total_work_hours, 2)

def get_info_employee(employee_id: int, cursor: object) -> list[dict]:
    """
    Gets information about an employee. Full name and position.
    :param employee_id: ``int``
    :param cursor: provides an interface for working with the results of a database query,  ``object``
    """
    query = f"SELECT full_name, position FROM employees WHERE id = {employee_id};"
    cursor.execute(query)
    return cursor.fetchone()

def time_conversion(time: float) -> dict:
    """
    Converts time from decimal to a dictionary of hours and minutes.
    :param time: time to convert, ``float``
    """
    hours = int(time)
    minutes = int((time - hours) * 60)
    return {'hours': hours, 'minutes': minutes}


def main():
    """
    There is a connection to the database, then functions 
    are called to calculate the employee's working time.
    """
    try:
        connection = pymysql.Connection(
        host = host,
        port = 3306,
        user = user,
        password =password,
        database = db_name,
        cursorclass = pymysql.cursors.DictCursor)
        print('Successfully connected to database')

        try:
            
            with connection.cursor() as cursor:
                working_hours_per_day = time_conversion(get_work_hours_day(get_times_on_day(employee_id, date, cursor)))
                working_hours_per_week = time_conversion(get_work_hours_week(get_times_on_week(employee_id, date, cursor)))
                name_employee = get_info_employee(employee_id, cursor)
                print(f"The employee - {name_employee['full_name']}, position - {name_employee['position']}"
                      f" worked for the specified day - {working_hours_per_day['hours']}h {working_hours_per_day['minutes']}m ,"
                      f" for the week - {working_hours_per_week['hours']}h {working_hours_per_week['minutes']}m")
        except Exception as err:
            print(err)
        finally:
            cursor.close()
            connection.close()

    except Exception as err:
        print('Error connecting to database')


if __name__ == '__main__':
    main()