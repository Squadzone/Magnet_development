"""
@author: yosi setiawan
Modified by yanuar harry
signed-off yosi setiawan
signed-off yanuar harry

License GPL-v2
"""

import re
import os
import errno


def make_sure_path_exist(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


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
import string
import re

yyyy = []
mo = []
dd = []
hh = []
mm = []
ss = []
Bh = []
Bd = []
Bz = []
Bf = []

date1 = datetime.utcnow() - timedelta(days=1)
tahun1 = int(date1.year)
bulan1 = int(date1.month)
tanggal1 = int(date1.day)

tahun = np.tile(tahun1, 86400)
bulan = np.tile(bulan1, 86400)
tanggal = np.tile(tanggal1, 86400)
jam = np.sort(np.tile(range(0, 24), 3600))
menit = np.tile(np.sort(np.tile(range(0, 60), 60)), 24)
detik = np.tile(range(0, 60), 1440)
Bh = list(np.tile(np.nan, 86400))
Bd = list(np.tile(np.nan, 86400))
Bz = list(np.tile(np.nan, 86400))
Bf = list(np.tile(np.nan, 86400))
h_mean = np.zeros(1440)
d_mean = np.zeros(1440)
z_mean = np.zeros(1440)
f_mean = np.zeros(1440)

filename = '%4.0f %02.0f %02.0f 00 00 00.txt' % (tahun1, bulan1, tanggal1)
namefolderlemi = '/home/tuntsi/Magnet_dev/LEMIDATA/' + \
    str(tahun1) + '/' + str(bulan1).zfill(2)
with open(namefolderlemi + '/' + filename) as f_lemi:
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
        Bx = float(data[6]) + 41300
        By = float(data[7])
        Bh[index] = np.sqrt(Bx ** 2 + By ** 2)
        Bd[index] = 60 * np.degrees(np.arcsin(By / Bh[index]))
        Bz[index] = float(data[8]) - 7100
        Bf[index] = np.sqrt((Bx ** 2) + (By ** 2) + (Bz[index] ** 2))

date1 = datetime(year=int(tahun1), month=int(bulan1),
                 day=int(tanggal1), hour=0, minute=0, second=0)

for k in range(0, 1440):
    if np.count_nonzero(np.isnan(Bh[(0 + (60 * k)):((60 + (60 * k)))])) <= 6:
        h_mean1 = np.array(Bh[(0 + (60 * k)):((60 + (60 * k)))])
        h_mean[k] = h_mean1[~np.isnan(h_mean1)].mean()
    else:
        h_mean[k] = 999999.9
    if np.count_nonzero(np.isnan(Bd[(0 + (60 * k)):((60 + (60 * k)))])) <= 6:
        d_mean1 = np.array(Bd[(0 + (60 * k)):((60 + (60 * k)))])
        d_mean[k] = d_mean1[~np.isnan(d_mean1)].mean()
    else:
        d_mean[k] = 99999.99
    if np.count_nonzero(np.isnan(Bz[(0 + (60 * k)):((60 + (60 * k)))])) <= 6:
        z_mean1 = np.array(Bz[(0 + (60 * k)):((60 + (60 * k)))])
        z_mean[k] = z_mean1[~np.isnan(z_mean1)].mean()
    else:
        z_mean[k] = 999999.89
    if np.count_nonzero(np.isnan(Bf[(0 + (60 * k)):((60 + (60 * k)))])) <= 6:
        f_mean1 = np.array(Bf[(0 + (60 * k)):((60 + (60 * k)))])
        f_mean[k] = f_mean1[~np.isnan(f_mean1)].mean()
    else:
        f_mean[k] = 99999.9

fileout = string.lower(date1.strftime("%b%d%y")) + '.tun'
namefolder = '/home/tuntsi/Magnet_dev/IMFV/' + \
    str(tahun1) + '/' + str(bulan1).zfill(2)
make_sure_path_exist(namefolder)
f_imfv = open(namefolder + '/' + fileout, 'w')

namefolderall = '/home/tuntsi/Magnet_dev/IMFVALL'
make_sure_path_exist(namefolderall)
f_imfv_all = open(namefolderall + '/' + fileout, 'w')

jam_a = 0
for b in range(0, 1440, 60):
    f_imfv.write('TUN ' + string.upper(date1.strftime("%b%d%y %j")) + ' ' +
                 str(jam_a).zfill(2) + ' HDZF R GIN 09000000 000000 RRRRRRRRRRRRRRRR\n')
    f_imfv_all.write('TUN ' + string.upper(date1.strftime("%b%d%y %j")) + ' ' +
                     str(jam_a).zfill(2) + ' HDZF R GIN 09000000 000000 RRRRRRRRRRRRRRRR\n')
    jam_a = jam_a + 1
    for q in range(0, 60, 2):
        Hodd = h_mean[(1 * q) + b] * 10
        Dodd = d_mean[(1 * q) + b] * 100
        Zodd = z_mean[
            (1 * q) + b] * 10
        Fodd = f_mean[(1 * q) + b] * 10
        Heven = h_mean[(1 * q) + b + 1] * 10
        Deven = d_mean[(1 * q) + b + 1] * 100
        Zeven = z_mean[
            (1 * q) + b + 1] * 10
        Feven = f_mean[(1 * q) + b + 1] * 10
        f_imfv.write('%07.0f %07.0f %07.0f %06.0f %s %07.0f %07.0f %07.0f %06.0f\n' %
                     (Hodd, Dodd, Zodd, Fodd, '', Heven, Deven, Zeven, Feven))
        f_imfv_all.write('%07.0f %07.0f %07.0f %06.0f %s %07.0f %07.0f %07.0f %06.0f\n' %
                         (Hodd, Dodd, Zodd, Fodd, '', Heven, Deven, Zeven, Feven))
f_imfv.write(' ')
f_imfv.close()
f_imfv_all.write(' ')
f_imfv_all.close()

print '%s converted to %s' % (filename, fileout)
