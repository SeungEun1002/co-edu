from datetime import date, datetime, timedelta


def get_timetable_time_list():
    time_list = []
    for i in range(8, 24):
        data = {}
        if i == 11:
            data = {
                'str': f'{i}:00am~{i+1}:00pm',
                'hour': i,
            }
        elif i ==12:
            data = {
                'str': f'{i}:00pm~{(i+1) % 12}:00pm',
                'hour': i,
            }
        elif i == 23:
            data = {
                'str': f'{i}:00pm~{(i + 1) % 12}:00am',
                'hour': i,
            }
        elif i//12 ==0:
            data = {
                'str': f'{i}:00am~{i+1}:00am',
                'hour': i,
            }
        else:
            data = {
                'str': f'{i % 12}:00pm~{(i+1) % 12}:00pm',
                'hour': i,
            }
        time_list.append(data)
    return time_list

def get_cur_week_datetime():
    today = datetime.now()  # or .today()
    start = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
    end = (start + timedelta(days=6)).replace(hour=23, minute=59, second=0, microsecond=0)

    return (start, end, today)
