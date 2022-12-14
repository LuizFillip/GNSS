import sys
from gnss_utils import date_from_doy, gpsweek_from_date
import os
os.path.dirname(sys.executable)
from pathlib import Path



class paths(object):
    """Construct file paths from input date (year and doy)"""

    def __init__(self, 
                 year: int = 2014, 
                 doy: int = 1, 
                 root = str(Path.cwd())):
        
        
        
        self.date = date_from_doy(year, doy)
        self.week, self.number = gpsweek_from_date(self.date)
        self.root = root
        self.current_path = os.path.join(self.root, "database")
        
        self.year = str(year)
        self.doy = self.date.strftime("%j")
        self.ext_rinex = self.year[-2:] + "o"
        
    
    def orbit(self, const = "igr"):
        return os.path.join(self.current_path, "orbit", 
                            self.year, const)
    @property
    def geo(self):
        return os.path.join(self.current_path, "geo", 
                            f"{self.year}.txt")
    @property
    def rinex(self):
        return os.path.join(self.current_path, "rinex", 
                            self.year, self.doy)
    @property
    def process(self):
        return os.path.join(self.current_path, "process", 
                            self.year, self.doy)
    @property
    def all_process(self):
        return os.path.join(self.current_path, "all_process", 
                            self.year, self.doy)
    @property
    def roti(self):
        return os.path.join(self.current_path, "roti", 
                            self.year)
    @property
    def dcb(self):
        return os.path.join(self.current_path, "dcb", 
                            self.year)
    @property
    def json(self):
        return os.path.join(self.current_path, "json", 
                            self.year)
    @property
    def prns(self):
        fname = f"{self.doy}.txt"
        return os.path.join(self.current_path, "prns", 
                            self.year, fname)
    @property
    def fn_json(self):
        fname = f"{self.doy}.json"
        return os.path.join(self.json, fname)

    @property
    def fn_roti(self):
        fname = f"{self.doy}.txt"
        return os.path.join(self.roti, fname)
    
    def fn_orbit(self, const = "igr"):
        fname = f"{const}{self.week}{self.number}.sp3"
        return os.path.join(self.orbit(const), fname)
    
    def fn_process(self, station = "alar"):
        fname =  f"{station}.txt"
        return  os.path.join(self.process, fname)

    def fn_all_process(self, station = "alar"):
        fname =  f"{station}.txt"
        return  os.path.join(self.all_process, fname)
    
    def fn_rinex(self, station = "alar"):
        fname = f"{station}{self.doy}1.{self.ext_rinex}"
        return os.path.join(self.rinex, fname)
    
    def fn_dcb(self, mgx = True):
        if mgx:
            fname = f"CAS0MGXRAP_{self.year}{self.doy}0000_01D_01D_DCB.BSX" 
            return os.path.join(self.dcb, fname)
    
    

class prns:
    """Creating a prn list for each constellation"""
    
    def __init__(self):
        pass
    @staticmethod
    def format_prn(constelation, num):
        if num < 10:
            prn = f"{constelation}0{num}"
        else:
            prn = f"{constelation}{num}"
        return prn
    
    @staticmethod
    def prn_list(constelation = "G", number = 32):
        call = prns()
        return [call.format_prn(constelation, num) 
                for num in range(1, number + 1)]
    
    @property
    def gps_and_glonass(self):
        call = prns()
        return call.prn_list("G", 32) + call.prn_list("R", 24)
    
    

def folder(path_to_create: str):
    """Create a new directory by path must be there year and doy"""
    try:
        os.mkdir(path_to_create)
        print(f"Creation of the directory {path_to_create} successfully")
    except OSError:
        print(f"Creation of the directory {path_to_create} failed")
    
    return path_to_create

def tex_path(folder:str) -> str:
    """

    Parameters
    ----------
    folder : str
        Folder name in latex repository.

    Returns
    -------
    path: str
        DESCRIPTION.

    """
    
    latex = "G:\\My Drive\\Doutorado\\Modelos_Latex_INPE\\docs\\Proposal\\Figures\\"
    return os.path.join(latex, folder)

def database_folders(year = 2014):
    """Created all folders needed for save data"""
    folders = ["orbit", "json", "prns", 
               "process", "rinex", "roti"]
    
    base = paths(year = 2014).current_path
    
    for dir_ in folders:
        try:
            folder_created = folder(os.path.join(base, dir_))
            folder(os.path.join(folder_created, str(year)))
        except OSError:
              print("already exists")
      