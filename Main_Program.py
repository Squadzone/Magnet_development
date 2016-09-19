"""
@author: yosi setiawan
Modified by yanuar harry
signed-off yosi setiawan
signed-off yanuar harry

License GPL-v2
"""

import os
import time

while True:
    os.system('python /home/magnettsi/Magnet/save_iaga.py')
    time.sleep(6400)
    os.system('python /home/magnettsi/Magnet/save_iaga_last.py')
    time.sleep(6400)
    os.system('python /home/magnettsi/Magnet/save_imfv.py')
    time.sleep(6400)
    os.system('python /home/magnettsi/Magnet/save_imfv_last.py')
    time.sleep(6400)
    os.system('python /home/magnettsi/Magnet/Analisa_Lemi_stasiun.py')
    time.sleep(6400)
    os.system('python /home/magnettsi/Magnet/save_k.py')
    time.sleep(6400)
    os.system('python /home/magnettsi/Magnet/save_excel.py')
    time.sleep(6400)
    os.system('python /home/magnettsi/Magnet/save_normal.py')
    time.sleep(6400)
