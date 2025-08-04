import re
import os
import datetime
import json

from dotenv import load_dotenv

load_dotenv()

from util import generatedExcelFile, emailReport, getDayAndWeek

now = datetime.datetime.now()
sessionDate = now.strftime("%Y-%m-%d")

[day, week] = getDayAndWeek(now)
# [day, week] = getDayAndWeek(now + datetime.timedelta(days=7))

#Check if current day is not saturday or sunday, Sun = 1, Sat = 7
if(day != 1 and day != 7):
    print("Exited!. Current day is not saturday nor sunday")
    exit()

groupKey = "w" + str(week) + "_d" + str(day) 

# print(groupKey)
# exit()

print("Started...")
# TODO - Log code execution

# These will be used to check against the files uploaded
# w_#_# - w_(week#)_(day#)
sitesGroups = {
    "w1_d7" : ["PTAIBC01DS1","NLSNBC01DS1","FSJNBC01DS2","VANCBC03DS1","HANYBC01DS1","LNGLBC01DS1"],
    "w1_d1" : ["BNVTPQXQDS1","MTMGPQXQDS1","STHLPQXQDS1","MATNPQXQDS1","BRKSAB01CG1","EDSOAB01CG0","CLGRAB04CG0"],
    "w2_d7" : ["PTCMBC02DS2","WVCRBC01DS1","NVCRBC01DS1","NNIMBC03DS1","LEDCAB01CG1","SYPLAB02CG1"],
    "w2_d1" : ["SDNYBC01DS1","IVMRBC01DS1","KLWNBC02DS2","KMLPBC02DS1","VCTABC06DS1","WLLKBC01DS1","TRRCBC02DS1"],
    "w3_d7" : ["BNBYBC01DS1","VERNBC01DS1","NNIMBC01DS1","WLOCAB01CG1","CLWKBC01DS1","CRBKBC01DS1"],
    "w3_d1" : ["GBSNBC01DS1","VCTABC05DS1","DWCKBC01DS1","TRALBC01DS1","CRTYBC01DS1","CBRVBC01DS1"],
    "w4_d7" : ["PWRVBC01DS1","ARGVBC01DS1","CQTLBC01DS1","ABFDBC01DS2","PNTNBC02DS1","SRRYBC01DS2"],
    "w4_d1" : ["DELTBC01DS1","RCMDBC02DS2","WHRKBC01DS2","VCTABC03DS2","SLAMBC01DS1","KMLPBC01DS2"],
}



rawFilesDir = "raw_files"
tcuList = []
fileList = os.listdir(rawFilesDir)

_sitesFileStatus = []

# sites = sitesGroups["w3_d1"] 
sites = sitesGroups[groupKey] 

def logSiteStatus(sList:list, f:str, dr:bool, dc:bool, fs, r=""):
    sList.append({
        "name": f,
        "dataReceived": str(dr),
        "dataCalculated": str(dc),
        "fileSize": fs,
        "remarks": r
    })

def processLine(fileName:str, line:str, searchStr:str, addPos:int, tcuList:list):
    search = re.search(searchStr, line)
    if search :
        position = search.start()
        stringTcu = line[position : position + addPos]
        darkCount = "WC"
        if "TDS0299" in line: darkCount = "DD"
        tcuList.append(fileName + "_" + stringTcu + "_" + darkCount)

def main():

    for fileName in fileList:
        try:
            if fileName in sites: 
                file = open(rawFilesDir + "/" + fileName, "r")

                isFileComplete = False
                
                # check first if the file is complete by looking for "RANGE PROCESSING COMPLETE"
                for line in file: 
                      if "RANGE PROCESSING COMPLETE" in line:
                        isFileComplete = True;
                        break
                      
                filePath = os.stat(rawFilesDir + "/" + fileName)
                fileSize = str(round(filePath.st_size / (1024 * 1024), 2)) + "MB"

                if isFileComplete:
                    sites.remove(fileName) #Removes filename from the list
                    for line in file: 
                        if " DN " in line and " TDS" in line:
                            if "TCU" in line:
                                processLine(fileName, line, "TCU\d\d\d\.\d\d\d\d", 11, tcuList)
                            elif "RSU" in line:
                                processLine(fileName, line, "RSU\d\d\d\.\d\d\d\d", 11, tcuList)
                            elif "RLU" in line:
                                processLine(fileName, line, "RLU\d\d\d\.\d\d\d\d", 6, tcuList)
                            elif "MXU" in line:
                                processLine(fileName, line, "MXU\d\d\d\.\d\d\d\d", 6, tcuList)
                            else :
                                None
                    logSiteStatus(_sitesFileStatus, fileName, True, True, fileSize, "OK")
                
                else :
                    logSiteStatus(_sitesFileStatus, fileName, True, True, fileSize, "Incomplete File, no `RANGE PROCESSING COMPLETE` found")


                
        except Exception:
            f = open('error.log', 'w')
            f.write('An exceptional thing happed during opening '+ fileName +' - %s' % e)
            f.close()
            logSiteStatus(_sitesFileStatus, fileName, True, False, "", "Error when opening the file")
            continue

    if len(sites) > 0:
        for site in sites:
            logSiteStatus(_sitesFileStatus, site, False, False, "", "No raw file found")

    sitesFileStatus = { "sites" : _sitesFileStatus }

    tcuList.sort()

    # count TCU
    result = dict(zip(list(tcuList),[list(tcuList).count(i) for i in list(tcuList)]))

    # y = json.dumps(sitesFileStatus, indent=2)
    # print(y)

    # sitesFileStatus TODO - Log this

    generatedExcelFile(result, sessionDate)
    # emailReport(sitesFileStatus, sessionDate)

main()

print("Done!")

# TODO - Copy generated csv/xlsx to /devops/projects/Customer_Count/Voice/GTD5 dir?
# TODO - Compress raw files and store the somewhere(maybe GDrive?), delete raw files after processing?
# TODO - Create endpoint that will be triggered by Resolve?
# TODO - Cron triggered?






