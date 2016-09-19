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

make_sure_path_exist("temp")

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
status = [0] * 7
k_i = [-1] * 56
a_i = [0] * 56
k_to = [-1] * 56
a_to = [-1] * 7
A_i = [-1] * 7


date1 = datetime.utcnow()
tahun1 = int(date1.year)
bulan1 = int(date1.month)
tanggal1 = int(date1.day)

namafile4 = '/home/tuntsi/Magnet_dev/data.sh'
f_k = open(namafile4, 'w')
f_k.write('kasm TUN:%s:7 300 xy /home/tuntsi/Magnet_dev/data /home/tuntsi/Magnet_dev/IMFVALL/' %
          (string.upper(((date1 - timedelta(days=6)).strftime("%d%b%Y")))))
f_k.close()

os.system('sh /home/tuntsi/Magnet_dev/data.sh')

f_kall = open('/home/tuntsi/Magnet_dev/kall.dat', 'w')
f_kmin = open('/home/magnettsi/Magnet/temp/kmin.dat', 'w')
f_k03 = open('/home/magnettsi/Magnet/temp/k03.dat', 'w')
f_k4 = open('/home/magnettsi/Magnet/temp/k4.dat', 'w')
f_k56 = open('/home/magnettsi/Magnet/temp/k56.dat', 'w')
f_k79 = open('/home/magnettsi/Magnet/temp/k79.dat', 'w')
f_Aall = open('/home/tuntsi/Magnet_dev/Aall.dat', 'w')
f_a0 = open('/home/magnettsi/Magnet/temp/a0.dat', 'w')
f_a30 = open('/home/magnettsi/Magnet/temp/a30.dat', 'w')
f_a50 = open('/home/magnettsi/Magnet/temp/a50.dat', 'w')
f_a100 = open('/home/magnettsi/Magnet/temp/a100.dat', 'w')
f_status = open('/home/magnettsi/Magnet/status.dat', 'w')
with open('/home/tuntsi/Magnet_dev/data.dka') as f:
    content = f.readlines()
    for j in range(6, len(content)):
        data_k = content[j].split(' ')
        for i in range(0, len(data_k) - 12):
            data_k.remove('')
        k_t = datetime.strptime(data_k[0], '%d-%b-%y')
        k_ti = datetime.strptime(data_k[0], '%d-%b-%y') - timedelta(days=6)
        indeks_k_t = ((date1 - k_t).days - 6) * -1
        k_i[0 + (indeks_k_t * 8)] = data_k[2]
        k_i[1 + (indeks_k_t * 8)] = data_k[3]
        k_i[2 + (indeks_k_t * 8)] = data_k[4]
        k_i[3 + (indeks_k_t * 8)] = data_k[5]
        k_i[4 + (indeks_k_t * 8)] = data_k[6]
        k_i[5 + (indeks_k_t * 8)] = data_k[7]
        k_i[6 + (indeks_k_t * 8)] = data_k[8]
        k_i[7 + (indeks_k_t * 8)] = data_k[9]

for p in range(0, 56):
    k_to[p] = (k_ti + timedelta(hours=3 * p + 2)
               - datetime(1970, 1, 1)).total_seconds()
    if (int(k_i[p]) >= 0 and int(k_i[p]) <= 3):
        f_k03.write('%s %s\n' % (k_to[p], k_i[p]))
    else:
        f_k03.write('%s %s\n' % (k_to[p], '0'))
    if (int(k_i[p]) == 4):
        f_k4.write('%s %s\n' % (k_to[p], k_i[p]))
    else:
        f_k4.write('%s %s\n' % (k_to[p], '0'))
    if (int(k_i[p]) == 5 or int(k_i[p]) == 6):
        f_k56.write('%s %s\n' % (k_to[p], k_i[p]))
    else:
        f_k56.write('%s %s\n' % (k_to[p], '0'))
    if (int(k_i[p]) >= 7):
        f_k79.write('%s %s\n' % (k_to[p], k_i[p]))
    else:
        f_k79.write('%s %s\n' % (k_to[p], '0'))
    if (int(k_i[p]) < 0):
        f_kmin.write('%s %s\n' % (k_to[p], k_i[p]))
    else:
        f_kmin.write('%s %s\n' % (k_to[p], '0'))
    f_kall.write('%s %s\n' % (k_to[p], k_i[p]))
f_kall.close()

for m in range(0, 56):
    if (k_i[m] == '0'):
        a_i[m] = 0
    elif (k_i[m] == '1'):
        a_i[m] = 3
    elif (k_i[m] == '2'):
        a_i[m] = 6
    elif (k_i[m] == '3'):
        a_i[m] = 12
    elif (k_i[m] == '4'):
        a_i[m] = 24
    elif (k_i[m] == '5'):
        a_i[m] = 40
    elif (k_i[m] == '6'):
        a_i[m] = 70
    elif (k_i[m] == '7'):
        a_i[m] = 120
    elif (k_i[m] == '8'):
        a_i[m] = 200
    elif (k_i[m] == '9'):
        a_i[m] = 300
    elif (k_i[m] == '-1'):
        a_i[m] = 0

for n in range(0, 7):
    A_i[n] = sum(a_i[0 + (n * 8):8 + (n * 8)]) / 8
    a_to[n] = (k_ti + timedelta(days=n, hours=12)
               - datetime(1970, 1, 1)).total_seconds()
    if (A_i[n] <= 30):
        status[n] = 'Relatively-Quiet'
        f_a0.write('%s %s\n' % (a_to[n], A_i[n]))
    else:
        f_a0.write('%s %s\n' % (a_to[n], '-50'))
    if (A_i[n] > 30 and A_i[n] <= 50):
        status[n] = 'Small-Storm'
        f_a30.write('%s %s\n' % (a_to[n], A_i[n]))
    else:
        f_a30.write('%s %s\n' % (a_to[n], '-50'))
    if (A_i[n] > 50 and A_i[n] <= 100):
        status[n] = 'Mid-Storm'
        f_a50.write('%s %s\n' % (a_to[n], A_i[n]))
    else:
        f_a50.write('%s %s\n' % (a_to[n], '-50'))
    if (A_i[n] > 100):
        status[n] = 'Great-Storm'
        f_a100.write('%s %s\n' % (a_to[n], A_i[n]))
    else:
        f_a100.write('%s %s\n' % (a_to[n], '-50'))
    f_Aall.write('%s %s\n' % (a_to[n], A_i[n]))
    f_status.write('%s\n' % status[n])
f_Aall.close()


print 'K index and A index calculated for %s' % (date1)
