from datetime import datetime
import random
import string

def random_name(length=6): #Name randomizer for simulations
    
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
    
    
def dateInput(commstring, preset = None): #date input function which enables proper checks
    
    while True:
        if preset == None:
            date = input(f'{commstring}')
        else:
            date = preset
            
        chars = list(date)
        
        try:
            year = int(date[0:4])
        except:
            pass
            
        try:
            month = int(date[5:7])
        except:
            pass
        try:
            day = int(date[8:])
        except:
            pass
        
        if len(date) != 10:
            
            print ('Invalid date! Please try again')
            preset = None
            continue
            
        elif (chars[4] != '-') or (chars[7] != '-'):
            
            print ('Invalid date! Please try again')
            preset = None
            continue
            
        elif year not in range(1954, datetime.now().year+1):
            
            print ('Invalid year! Please try again!')
            preset = None
            continue
            
        elif month not in range (1, 13):
            
            print ('Invalid month! Please try again!')
            preset = None
            continue
        
        elif day not in range (1, 32):
            
            print ('Invalid day! Please try again!')
            preset = None
            continue
            
        elif (day in range (30, 32)) and month == 2:
            
            print ('Invalid date! Please try again!')
            preset = None
            continue
        
        else:
            
            break
            
    return date
