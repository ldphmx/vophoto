#Encoding=UTF8

import re
import datetime
import calendar
from _ast import Num

############ abs
# 2014年_nt 的_u 照片_n
# 3月份_nt
# 2014年_nt 3月_nt 的_u 照片_n
# 15日_nt 的_u 照片_n
# 3月_nt 11日_nt 的_u 照片_n

############ relative
# 去年_nt 的_u 照片_n
# 春天_nt 的_u 照片_n
# 今年_nt 春天_nt 的_u 照片_n
# 上个月_nt 的_u 照片_n
# 最近_nt 的_u 照片_n
# 上周_nt 的_u 照片_n
# 今天_nt 的_u 照片_n
# 昨天_nt 的_u 照片_n
# 上周六_nt 的_u 照片_n
# 前年_nt 的_u 照片_n

def do_parse_raw_year(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    m = re.search(regex, date_str)
    if not m:
        return None
    
    year = int(m.group(1))
    return (year, year)

def do_parse_last_year(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    start = datetime.date.today()
    return (start.year - 1, start.year - 1)

def do_parse_this_year(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    start = datetime.date.today()
    return (start.year, start.year)

def do_parse_last2_year(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    start = datetime.date.today()
    return (start.year - 2, start.year - 2)

def do_parse_raw_month(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    m = re.search(regex, date_str)
    if not m:
        return None
    
    month = int(m.group(1))
    return (month, month)

def do_parse_last_month(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    start = datetime.date.today()
    day = start.day
    delta = datetime.timedelta(days=day + 1)
    start = start - delta
    (day1, ndays) = calendar.monthrange(start.year, start.month)
    return (start.year, start.month, 1, start.year, start.month, ndays)

def do_parse_spring(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    return (2, 5)

def do_parse_summer(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    return (5, 8)

def do_parse_autumn(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    return (8, 10)

def do_parse_winter(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    return (10, 12)

def do_parse_raw_day(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    m = re.search(regex, date_str)
    if not m:
        return None
    
    day = int(m.group(1))
    return (day, day)

def do_parse_recent(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    now = datetime.date.today()
    delta = datetime.timedelta(days=7)
    start = now - delta
    (day1, ndays) = calendar.monthrange(start.year, start.month)
    return (start.year, start.month, start.day, now.year, now.month, now.day)

def do_parse_n_recent(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    now = datetime.date.today()
    m = re.search(regex, date_str)
    if not m:
        return None
    
    day = m.group(2)
    if not day:
        day = 7
    else:
        day = int(day)
    delta = datetime.timedelta(days=day)
    start = now - delta
    return (start.year, start.month, start.day, now.year, now.month, now.day)

def do_parse_last_weekday(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    now = datetime.date.today()
    wd = calendar.weekday(now.year, now.month, now.day)
    m = re.search(regex, date_str)
    if not m:
        return None
    
    day = m.group(1)
    if not day:
        day = 7 + wd
        delta = datetime.timedelta(days=day)
        start = now - delta
        end = start + datetime.timedelta(days=7)
        return (start.year, start.month, start.day, end.year, end.month, end.day)
    else:
        day = 7 + wd + int(convert_chinese_num(day))
        delta = datetime.timedelta(days=day)
        start = now - delta
        return (start.year, start.month, start.day, start.year, start.month, start.day)
    

def do_parse_last_n_week(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    now = datetime.date.today()
    m = re.search(regex, date_str)
    if not m:
        return None
    
    day = m.group(1)
    if not day:
        day = 21
        delta = datetime.timedelta(days=day)
        start = now - delta
    else:
        day = 7 * int(convert_chinese_num(day))
        delta = datetime.timedelta(days=day)
        start = now - delta
        
    return (start.year, start.month, start.day, now.year, now.month, now.day)

def do_parse_today(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    start = datetime.date.today()
    return (start.year, start.month, start.day, start.year, start.month, start.day)

def do_parse_lastday(regex, date_str):
    print 'do parse: ' + regex + " - " + date_str
    now = datetime.date.today()
    delta = datetime.timedelta(days=1)
    start = now - delta
    return (start.year, start.month, start.day, start.year, start.month, start.day)

year_regex = [(ur'(\d+)年', do_parse_raw_year),
              (ur'去年', do_parse_last_year),
              (ur'今年', do_parse_this_year),
              (ur'前年', do_parse_last2_year),]

month_regex = [(ur'(\d+)月[份]{0,1}', do_parse_raw_month),
               (ur'春[天季]', do_parse_spring),
               (ur'夏[天季]', do_parse_summer),
               (ur'秋[天季]', do_parse_autumn),
               (ur'冬[天季]', do_parse_winter)]

day_regex = [(ur'(\d+)日', do_parse_raw_day)]

relative_regex = [(ur'[上|(最近)]([一二三四五六七八九两1-9]{0,1})[个]{0,1}月', do_parse_last_month),
                  (ur'今天', do_parse_today),
                  (ur'昨天', do_parse_lastday),
                  (ur'最近((\d+)天){0,1}', do_parse_n_recent),
                  (ur'上周([一二三四五六日1-6]{0,1})', do_parse_last_weekday),
                  (ur'[上|(最近)]([一二三四五六七八九两1-9])周', do_parse_last_n_week)]

def convert_chinese_num(num):
    if num == '1'  or num == u'一':
        return 1
    elif num == '2'  or num == u'二' or num == u'两':
        return 2
    elif num == '3'  or num == u'三':
        return 3
    elif num == '4'  or num == u'四':
        return 4
    elif num == '5'  or num == u'五':
        return 5
    elif num == '6'  or num == u'六':
        return 6
    elif num == '7'  or num == u'七':
        return 7
    elif num == '8'  or num == u'八':
        return 8
    elif num == '9'  or num == u'九':
        return 9

def parse_nl_date(date_str):   
    now = datetime.date.today()
    (start_year, start_month, start_day) = (now.year, now.month, now.day)
    (end_year, end_month, end_day) = (now.year, now.month, now.day)
    
    year_set = False
    month_set = False
    day_set = False
            
    for st in date_str:
        res = parse_relative(st)
        if res:
            (start_year, start_month, start_day, end_year, end_month, end_day) = res
        else:
            res = parse_year(st)
            if res:
                (start_year, end_year) = res
                year_set = True
            res = parse_month(st)
            if res:
                (start_month, end_month) = res
                month_set = True
            res = parse_day(st)
            if res:
                (start_day, end_day) = res
                day_set = True
                    
            if not year_set and not month_set and not day_set:
                break
            
            if not year_set:
                (start_year, end_year) = (now.year, now.year)
                
            if not month_set:
                if year_set:
                    (start_month, end_month) = (1,12)
                elif day_set:
                    (start_month, end_month) = (now.month, now.month)
                    
            if not day_set:
                (start_day, end_day) = (1,31)
            
    return datetime.date(start_year, start_month, start_day), datetime.date(end_year, end_month, end_day)

def parse_date_item(date_str, regex):
    parse_func = None
    parse_reg = None
    for reg, func in regex:
        m = re.search(reg, date_str)
        if m:
            parse_func = func
            parse_reg = reg
            break
    
    if parse_func:
        return parse_func(parse_reg, date_str)
    
    return None

def parse_year(date_str):
    return parse_date_item(date_str, year_regex)

def parse_month(date_str):
    return parse_date_item(date_str, month_regex)

def parse_day(date_str):
    return parse_date_item(date_str, day_regex)

def parse_relative(date_str):
    return parse_date_item(date_str, relative_regex)

if __name__ == "__main__":
    # relative time
#     print parse_nl_date([u'上个月'])
#     print parse_nl_date([u'最近'])
#     print parse_nl_date([u'最近3天'])
#     print parse_nl_date([u'最近3个月'])
#     print parse_nl_date([u'上周'])
#     print parse_nl_date([u'上周五'])
#     print parse_nl_date([u'上两周'])
#     
#     #absolute time
#     print parse_nl_date([u'2014年'])
#     print parse_nl_date([u'今年'])
#     print parse_nl_date([u'去年'])
#     print parse_nl_date([u'前年'])
#     print parse_nl_date([u'3月份'])
#     print parse_nl_date([u'春天'])
#     print parse_nl_date([u'春季'])
#     print parse_nl_date([u'夏天'])
#     print parse_nl_date([u'秋天'])
#     print parse_nl_date([u'冬天'])
    
    print parse_nl_date([u'2104年',u'3月'])
    print parse_nl_date([u'2104年',u'夏天'])
    print parse_nl_date([u'去年',u'冬天'])
    
    
#     print parse_nl_date([u'3月'])
#     print parse_nl_date([u'15日'])
#     print parse_nl_date([u'2014年',u'3月份', u'15日'])
#     print parse_nl_date([u'2014年',u'3月份'])
    
    
    