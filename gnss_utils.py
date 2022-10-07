import gnsscal
import datetime
import numpy as np
import os


def gpsweek_from_date(date: datetime.datetime) -> tuple:
    """Return GPS week and number from date"""
    return gnsscal.date2gpswd(date)

def gpsweek_from_doy_and_year(year: int, doy:int) -> tuple:
    """Return GPS week and number from date"""
    return gnsscal.date2gpswd(date_from_doy(year, doy))

def doy_from_gpsweek(week: int, number: int) -> tuple:
    """Return year and doy from gps week"""
    return gnsscal.gpswd2yrdoy(week, number)

def date_from_gpsweek(week, number):
    """Return date from gps week"""
    year, doy = doy_from_gpsweek(week, number)
    return date_from_doy(year, doy)

def date_from_doy(year: int, doy:int) -> datetime.datetime:
    """Return date from year and doy"""
    return datetime.date(year, 1, 1) + datetime.timedelta(doy - 1)

def day_and_month(year: int, doy:int) -> tuple:
    """Get month and day from year and doy"""
    date = date_from_doy(year, doy)
    return date.month, date.day
        

def delete_files(infile, extension = ".22d"):
    """Deleting files in directory by extension"""
    _, _, files = next(os.walk(infile))
    
    for filename in files:
        if filename.endswith(extension):
            try:
                os.remove(os.path.join(infile, filename))
            except Exception:
                print(f"Could not delete {filename}")



def tec_fname(filename):
    """Convert TEC filename (EMBRACE format) to datetime"""
    args = filename.split('_')
    date = args[1][:4] + '-' + args[1][4:6]+ '-' +args[1][-2:] 
    time = args[-1].replace('.txt', '')
    time = time[:2] + ':' + time[2:]
    
    return datetime.datetime.strptime(date + ' ' + time, "%Y-%m-%d %H:%M")


class fname_attrs(object):
    
    """Attributes of filenames (rinex, orbit and bias)"""
    
    def __init__(self, fname):
        
        extension = fname.split(".")
        if extension[1][-1] == "o":
        
            self.station = extension[0][:4]
            year = extension[1][:2]
            doy = extension[0][4:7]

            if int(year) < 99:
                year = "20" + year
            else:
                year = "19" + year

            self.year = int(year)
            self.doy = int(doy)
            
        elif extension[1] == "sp3":
            
            self.const = extension[0][:3]
            week = int(extension[0][3:7])
            number = int(extension[0][7:])
            
            self.year, self.doy = doy_from_gpsweek(week, number)
            
        else:
            args = extension[0].split("_")

            if "MGX" in args[0]:
                self.year = int(args[1][:4])
                self.doy = int(args[1][4:7])
                
                
        self.date = date_from_doy(self.year, self.doy)
         
    
  