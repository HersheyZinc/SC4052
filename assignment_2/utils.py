from datetime import datetime

def get_month_year(date_string):
    # Extracts month, year from date string
    dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return f"{dt.strftime('%B')} {dt.year}"