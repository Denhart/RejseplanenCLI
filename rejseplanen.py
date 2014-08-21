#!/bin/python2.7
from requests import session
import re
import time
import argparse
from prettytable import *
def getStation(inputStation):
    url = 'http://mobil.rejseplanen.dk/mobil-bin/ajax-getstop.exe/mn?encoding=utf-8&start=1&getstop=1&suggestMethod=none&S=%s&REQ0JourneyStopsS0A=255&REQ0JourneyStopsB=5' % (inputStation)
    with session() as stn: 
        request = stn.get(url)
        regex = re.compile("""\"value":"(.*?)","id":"(.*?)\"""") 
        station = regex.findall(request.text)
        return station[0]
 
def getTimes(data):
    regex = re.compile("""headers="OUTWARDConTimeDep">(.*?)</td>.*?"OUTWARDConTimeDest">(.*?)</td>.*?OUTWARDConDuration">(.*?)</td>.*?OUTWARDConChanges">(.*?)</td>""", re.DOTALL)
    times = regex.findall(data)
    return times
 
def getStepsTesting(data):
    regex = re.compile("""<div class="productHolder">(.*)</div>""")
    temp = regex.findall(data)
    steps = ['','','','','','','','','','','','','','','']
    i = 0
    for item in temp:
        snug = ''
        regex = re.compile("""alt="(.*?)\"""")
        result = regex.findall(item)
        result.append("")
        for x in range(len(result)-1):
            res = result[x].replace("   "," ")
            res = res.replace("til","Til")
            if  result[x+1]:
                res = res+" =>"
            snug += " %s" % res
        steps[i] = snug
        i+=1
    return steps
 
 
def printDeparture(times,steps):
    out = PrettyTable(["Afgang", "Ankomst", "Tid", "Skift","Steps"])
    out.padding_width = 1 
    out.align["Steps"] = "l" 
    for i in range(len(times)):
        out.add_row([times[i][0],times[i][1],times[i][2].strip(),times[i][3].strip(),steps[i]])
    print out
def printDepartureTesting(times):
    print "Afgang Ankomst   Tid   Skift"
    for item in times:
        print "%s   %s    %s    %s" % (item[0],item[1],item[2].strip(),item[3].strip())
 
def getDeparture(fromStation,toStation,date,time,timeSel):
    fromStation = getStation(fromStation)
    toStation = getStation(toStation)
    url = "http://www.rejseplanen.dk/bin/query.exe/mn?REQ0JourneyStopsS0ID=%s&REQ0JourneyStopsZ0ID=%s&date=%s&time=%s&timesel=%s&application=PRINTVIEW&start=1" % (fromStation[1],toStation[1],date,time,timeSel)
    print "Fra: %s\nTil: %s" % (fromStation[0],toStation[0])
    with session() as rp:
        request = rp.get(url)
        timeData = getTimes(request.text)
        stepData = getStepsTesting(request.text)
#        printDepartureTesting(timeData)
        printDeparture(timeData,stepData)
 
parser = argparse.ArgumentParser(description='Rejseplanen CLI.')
parser.add_argument('From', help='The station to travel from')
parser.add_argument('Destination', help='The destination.')
parser.add_argument('-t','--time', dest='tTime', default=time.strftime("%H:%M"),help='Time of journey in the format H:M')
parser.add_argument('-d','--date', dest='tDate', default=time.strftime("%d.%m.%Y"),help='Date of journey in the format H:M')
parser.add_argument('-s','--sort', dest='timeSel', default="depart",choices=["depart","arrive"],help='Selects time after arrive')
args = parser.parse_args()
 
getDeparture(args.From,args.Destination,args.tDate,args.tTime,args.timeSel)