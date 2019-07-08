import os
import datetime

def __set_path(path):
    path = path.replace("\\", "/")
    if path[0] != '/' and path[1] != ':':
        path = os.getcwd().replace("\\", "/") + "/" + path
    return path

def __create_folder(path):
    path = __set_path(path)
    if path[-1] == '/':
        path = path[0:len(path)-1]
    try:
        if os.path.isdir(path) is False:
            os.mkdir(path)
    except Exception as e:
        print("create Folder : ", e)
        repath = str(path).split("/")[-1]
        repath = str(path).split("/"+repath)[0]
        __create_folder(repath)
        __create_folder(path)
    if path[-1] is not '/':
        path = path+"/"
    return path

def toCSVfromFolder(fromFolder, toFile, func, encoding='UTF8'):
    print("work : toCSV")
    toCSV(datafromFolder(fromFolder, func, encoding),toFile)

def datafromFolder(fromFolder, func, encoding='UTF8'):
    fromFolder = __create_folder(fromFolder)
    file_list = os.listdir(fromFolder)
    file_list.sort()
    data = []
    for item in file_list:
        print("work : ", item)
        ReadFile(fromFolder+item,func, data, encoding)
    return data

def toCSV(data:list, toPath:str):
    path = toPath.split(toPath.split("/")[-1])[0]
    path = __create_folder(path)
    f = open(toPath, 'w')
    f.write("id,vendor_id,pickup_datetime,dropoff_datetime,passenger_count,pickup_longitude,pickup_latitude,dropoff_longitude,dropoff_latitude,store_and_fwd_flag,trip_duration\n")
    for d in data:
        f.write(d+"\n")
    f.close()

def ToDate(date:str):
    _year = date[0:4]
    _month = date[4:6]
    _day = date[6:8]
    _h = date[8:10]
    _m = date[10:12]
    _s = date[12:14]
    return "{}-{}-{} {}:{}:{}".format(
        _year,
        _month,
        _day,
        _h,
        _m,
        _s
    )

def ReadFile(path, callback, data=[], encoding='UTF8'):
    f = open(path, 'r', encoding=encoding)
    while True:
        line = f.readline()
        if not line: break
        callback(line, data)
    f.close()
    return data

def isKorea(lon, lat):
    lon = float(lon)
    lat = float(lat)
    if lon <131.896599 and lon > 124.762885 and lat <38.637389 and lat>32.720577:
        return True
    return False

def __dateToArray(date:str):
    fors = date.split(" ")
    _date = fors[0].split("-")
    _time = fors[1].split(":")
    _date += _time
    _date = [int(i) for i in _date ]
    return _date

def __getSec(date1, date2, real=True):
    date1 = __dateToArray(date1)
    date2 = __dateToArray(date2)
    start_time = datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    end_time = datetime.datetime(date2[0],date2[1],date2[2],date2[3],date2[4],date2[5])
    result = start_time - end_time
    sec_ = result.total_seconds()
    if sec_ < 0 and real is True:
        sec_*=-1
    return sec_

def ReadTRIP(line:str, data:list):
    cut = line.replace("\n","").split("|")
    _id = cut[3]
    _vandor_id = cut[6]
    _on_datetime = ToDate(cut[12])
    _off_datetime = ToDate(cut[13])
    _trip_path = cut[18]
    _on_lon = cut[14]
    _on_lat = cut[15]
    _off_lon = cut[16]
    _off_lat = cut[17]
    _flag = 'N'
    _trip_duration = __getSec(_on_datetime,_off_datetime)#cut[22]
    if isKorea(_on_lon, _on_lat) and isKorea(_off_lon,_off_lat):
        data.append("{},{},{},{},{},{},{},{},{},{},{}".format(
            _id,
            _vandor_id,
            _on_datetime,
            _off_datetime,
            _trip_path,
            _on_lon,
            _on_lat,
            _off_lon,
            _off_lat,
            _flag,
            _trip_duration
        ))

def ReadDTG(line:str, data:list):
    cut = line.replace("\n","").split(",")
    _id = cut[5]
    _vandor_id = cut[4]
    _on_datetime = ToDate(cut[14])
    _off_datetime = ""
    _trip_path = cut[12]
    _on_lon = cut[18]
    _on_lat = cut[19]
    _off_lon = ""
    _off_lat = ""
    _flag = 'N'
    _trip_duration = _on_datetime
    if isKorea(_on_lon, _on_lat):
        data.append("{},{},{},{},{},{},{},{},{},{},{}".format(
            _id, # 0
            _vandor_id,  # 1
            _on_datetime,  # 2
            _off_datetime,  # 3
            _trip_path,  # 4
            _on_lon,  # 5
            _on_lat,  # 6
            _off_lon,  # 7
            _off_lat,  # 8
            _flag,  # 9
            _trip_duration  # 10
        ))
def ReadDTG2(line:str, data:list):
    cut = line.replace("\n","").split("|")
    _id = cut[0]
    _vandor_id = cut[3]
    _on_datetime = ToDate("20"+cut[-1])
    _off_datetime = ""
    _trip_path = cut[7]
    _on_lon = cut[12][0:3]+"."+cut[12][3:]
    _on_lat = cut[13][0:2]+"."+cut[13][2:]
    _off_lon = ""
    _off_lat = ""
    _flag = 'N'
    _trip_duration = _on_datetime
    if isKorea(_on_lon, _on_lat):
        data.append("{},{},{},{},{},{},{},{},{},{},{}".format(
            _id, # 0
            _vandor_id,  # 1
            _on_datetime,  # 2
            _off_datetime,  # 3
            _trip_path,  # 4
            _on_lon,  # 5
            _on_lat,  # 6
            _off_lon,  # 7
            _off_lat,  # 8
            _flag,  # 9
            _trip_duration  # 10
        ))

def isSameIDFromDTG(dtg1:list, dtg2:list):
    if dtg1[0] == dtg2[0]:
        return True
    return False

def MergeDTG(dtg1, dtg2):
    sec = __getSec(dtg1[2],dtg2[2], False)
    
    _id = dtg1[0]
    _vandor_id = dtg1[1]
    _on_datetime = dtg1[2]
    _off_datetime =dtg1[3]
    _trip_path = dtg1[4]
    _on_lon = dtg1[5]
    _on_lat =dtg1[6]
    _off_lon =dtg1[7]
    _off_lat = dtg1[8]
    _flag = dtg1[9]
    _trip_duration = dtg1[10]
    
    if sec > 0:
        _on_datetime = dtg2[2]
        _on_lon = dtg2[5]
        _on_lat =dtg2[6]
        if _off_datetime == "":
            _off_datetime =dtg1[2]
            _off_lon =dtg1[5]
            _off_lat = dtg1[6]
    else:
        if _off_datetime != "":
            sec = __getSec(dtg1[3],dtg2[2], False)
        else:
            sec = -1
        if sec < 0 :
            _off_datetime = dtg2[2]
            _off_lon = dtg2[5]
            _off_lat =dtg2[6]
    _trip_duration = int(__getSec(_on_datetime,_off_datetime))
    return "{},{},{},{},{},{},{},{},{},{},{}".format(
            _id, # 0
            _vandor_id,  # 1
            _on_datetime,  # 2
            _off_datetime,  # 3
            _trip_path,  # 4
            _on_lon,  # 5
            _on_lat,  # 6
            _off_lon,  # 7
            _off_lat,  # 8
            _flag,  # 9
            _trip_duration  # 10
        )

def findData(data:list, d:str):
    for c in data:
        if d==c:
            continue
        a = d.split(",")
        b = c.split(",")
        del c
        if isSameIDFromDTG(a,b):
            d = MergeDTG(a,b)
    return d

def DTGToTRIP(data:list, func = None, toFile=None):
    result = []
    for a in data:
        max = len(data)
        now = data.index(a)+1
        g = a
        while(True):
            if now == max:
                break
            b = data[now]
            c = g.split(",")
            d = b.split(",")
            if isSameIDFromDTG(c,d):
                del data[now]
                max-=1
                now-=1
                g = MergeDTG(c,d)
            now+=1
        k = g.split(",")
        if k[3] != "":
            if func is not None:
                func(g, toFile)
            else:
                result.append(g)
    if func is not None:
        return result
    else:
        return None

def _toCSV(data:str, toPath:str):
    path = toPath.split(toPath.split("/")[-1])[0]
    path = __create_folder(path)
    f = open(toPath, 'a')
    f.write(data+"\n")
    f.close()
