"""
@author: yosi setiawan
Modified by yanuar harry
signed-off yosi setiawan
signed-off yanuar harry

License GPL-v2
"""


def clear_all():
    """Clears all the variables from the workspace of the spyder application."""
    gl = globals().copy()
    for var in gl:
        if var[0] == '_':
            continue
        if 'func' in str(globals()[var]):
            continue
        if 'module' in str(globals()[var]):
            continue

        del globals()[var]
if __name__ == "__main__":
    clear_all()

clear_all()

from datetime import datetime
from datetime import timedelta
import numpy as np
import re
import time
import string
import sys
import string
import os
import errno


def make_sure_path_exist(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

yyyy = []
mo = []
dd = []
hh = []
mm = []
ss = []
Bx = []
By = []
Bz = []
Bf = []
Bh = []
Bd = []
sk1 = []
sk2 = []


Bx = list(np.tile(np.nan, 86400))
By = list(np.tile(np.nan, 86400))
Bz = list(np.tile(np.nan, 86400))
Bf = list(np.tile(np.nan, 86400))
Bh = list(np.tile(np.nan, 86400))
Bd = list(np.tile(np.nan, 86400))
date1 = datetime.utcnow() - timedelta(days=1)
tahun1 = int(date1.year)
bulan1 = int(date1.month)
tanggal1 = int(date1.day)
k_t = datetime.utcnow()

namafile4 = '/home/tuntsi/Magnet_dev/k_harian.sh'

f_k = open(namafile4, 'w')
f_k.write('kasm TUN:%s:1 300 xy /home/tuntsi/Magnet_dev/k_harian /home/tuntsi/Magnet_dev/IMFV/%s/%s/' %
          (string.upper((date1.strftime("%d%b%Y"))), str(tahun1), str(bulan1).zfill(2)))
f_k.close()

os.system('sh /home/tuntsi/Magnet_dev/k_harian.sh')

f_kall = open('/home/tuntsi/Magnet_dev/k_harian_all.dat', 'w')

with open('/home/tuntsi/Magnet_dev/k_harian.dka') as f:
    content = f.readlines()
    for j in range(6, len(content)):
        data_k = content[j].split(' ')
        for i in range(0, len(data_k) - 12):
            data_k.remove('')
        k_t1 = datetime.strptime(data_k[0], '%d-%b-%y')
        sk1 = int(data_k[10])

f_kall = open('/home/tuntsi/Magnet_dev/k_harian_all.dat', 'w')

with open('/home/tuntsi/Magnet_dev/k_normal.txt') as f:
    content = f.readlines()
    for j in range(6, len(content)):
        data_k = content[j].split(' ')
        k_t2 = datetime.strptime(data_k[0], '%d-%b-%y')
        sk2 = int(data_k[1])

if sk1 > 0:
    if sk1 < sk2:
        k_t = k_t1
        file_k = open('/home/tuntsi/Magnet_dev/k_normal.txt', 'w')
        data_k = '%s %s' % (k_t.strftime('%d-%b-%y'), sk1)
        file_k.write(data_k)
        file_k.close()
else:
    k_t = k_t2

namafile = str(k_t.year) + ' ' + str(k_t.month).zfill(
    2) + ' ' + str(k_t.day).zfill(2) + ' 00 00 00.txt'
namefolderlemi = '/home/tuntsi/Magnet_dev/LEMIDATA/' + \
    str(k_t.year) + '/' + str(k_t.month).zfill(2)
with open(namefolderlemi + '/' + namafile) as f_lemi:
    content = f_lemi.readlines()
    for i in range(0, len(content)):
        data = re.split('\s+', content[i])
        yyyy = float(data[0])
        mo = float(data[1])
        dd = float(data[2])
        hh = float(data[3])
        mm = float(data[4])
        ss = float(data[5])
        index = int((hh * 3600) + (mm * 60) + ss)
        Bx[index] = float(data[6]) + 41300
        By[index] = float(data[7])
        Bh[index] = np.sqrt(Bx[index] ** 2 + By[index] ** 2)
        Bd[index] = 60 * np.degrees(np.arcsin(By[index] / Bh[index]))
        Bz[index] = float(data[8]) - 7100
        Bf[index] = np.sqrt(
            (Bx[index] ** 2) + (By[index] ** 2) + (Bz[index] ** 2))


fileout = open('/home/tuntsi/Magnet_dev/normal.txt', 'w')
for j in range(0, 86400):
    data_normal = '%9.3f %6.3f %9.3f %9.3f %9.3f %7.3f \n' % (
        Bh[j], Bd[j], Bz[j], Bf[j], Bx[j], By[j])
    fileout.write(data_normal)
fileout.close()


print 'normal data calculated for %s' % (k_t)
