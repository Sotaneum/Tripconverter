def ReadFile(path, callback):
    f = open(path, 'r', encoding='UTF8')
    data = {}
    while True:
        line = f.readline()
        if not line: break
        callback(line, data)
    f.close()
    return data

def ReadTRIP(line:str, data:dict):
    cut = line.replace("\n","").split("|")
    key = cut[3]
    sub = cut[14:18]
    data.update({key:sub})

def ReadRISK(line:str, data:dict):
    cut = line.replace("\n","").split("|")
    key = cut[3]
    sub = cut[5:7]
    try:
        data[key].append(sub)
    except:
        data.update({key:[sub]})

def JOIN(TRIP:dict, RISK:dict):
    for key in TRIP.keys():
        trip = TRIP[key]
        if key in RISK.keys():
            Ratio(trip, RISK[key])
    return RISK

def Ratio(TRIP:list, RISK:list):
    tLat = float(TRIP[0])
    tLon = float(TRIP[1])
    rLat = float(RISK[0][0])
    rLon = float(RISK[0][1])
    at_ratio = tLat/rLat
    on_ratio = tLon/rLon
    for risk in RISK:
        risk[0]=str(float(risk[0]) * at_ratio)
        risk[1]=str(float(risk[1]) * on_ratio)
