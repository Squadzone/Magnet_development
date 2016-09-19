"""
@author: yosi setiawan
Modified by yanuar harry
signed-off yosi setiawan
signed-off yanuar harry

License GPLv3
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
import re

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

date1 = datetime.utcnow() - timedelta(days = 1)
tahun1 = int(date1.year)
bulan1 = int(date1.month)
tanggal1 = int(date1.day)

tahun = np.tile(tahun1, 86400)
bulan = np.tile(bulan1, 86400)
tanggal = np.tile(tanggal1, 86400)
jam = np.sort(np.tile(range(0, 24), 3600))
menit = np.tile(np.sort(np.tile(range(0, 60), 60)), 24)
detik = np.tile(range(0, 60), 1440)
Bx = list(np.tile(np.nan, 86400))
By = list(np.tile(np.nan, 86400))
Bz = list(np.tile(np.nan, 86400))
Bf = list(np.tile(np.nan, 86400))
x_mean = np.zeros(1440)
y_mean = np.zeros(1440)
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
        Bx[index] = float(data[6]) + 41300
        By[index] = float(data[7])
        Bz[index] = float(data[8]) - 7100
        Bf[index] = np.sqrt(
            (Bx[index] ** 2) + (By[index] ** 2) + (Bz[index] ** 2))

date1 = datetime(year=int(tahun1), month=int(bulan1),
                 day=int(tanggal1), hour=0, minute=0, second=0)

for k in range(0, 1440):
    if np.count_nonzero(np.isnan(Bx[(0 + (60 * k)):((60 + (60 * k)))])) <= 6:
        x_mean[k] = np.nanmean(Bx[(0 + (60 * k)):((60 + (60 * k)))])
    else:
        x_mean[k] = 99999.00
    if np.count_nonzero(np.isnan(By[(0 + (60 * k)):((60 + (60 * k)))])) <= 6:
        y_mean[k] = np.nanmean(By[(0 + (60 * k)):((60 + (60 * k)))])
    else:
        y_mean[k] = 99999.00
    if np.count_nonzero(np.isnan(Bz[(0 + (60 * k)):((60 + (60 * k)))])) <= 6:
        z_mean[k] = np.nanmean(Bz[(0 + (60 * k)):((60 + (60 * k)))])
    else:
        z_mean[k] = 99999.00
    if np.count_nonzero(np.isnan(Bf[(0 + (60 * k)):((60 + (60 * k)))])) <= 6:
        f_mean[k] = np.nanmean(Bf[(0 + (60 * k)):((60 + (60 * k)))])
    else:
        f_mean[k] = 99999.00

fileout = 'TUN' + str(tahun1) + str(bulan1).zfill(
    2) + str(tanggal1).zfill(2) + 'vmin' + '.min'
namefolder = '/home/tuntsi/Magnet_dev/IAGA/' + \
    str(tahun1) + '/' + str(bulan1).zfill(2)
make_sure_path_exist(namefolder)
f_iaga = open(namefolder + '/' + fileout, 'w')

f_iaga.write(
    ' Format                 IAGA-2002                                    |\n')
f_iaga.write(
    ' Source of Data         BMKG                                         |\n')
f_iaga.write(
    ' Station Name           Tuntungan                                    |\n')
f_iaga.write(
    ' IAGA Code              TUN                                          |\n')
f_iaga.write(
    ' Geodetic Latitude      3.517                                        |\n')
f_iaga.write(
    ' Geodetic Longitude     98.567                                       |\n')
f_iaga.write(
    ' Elevation              86                                           |\n')
f_iaga.write(
    ' Reported               XYZF                                         |\n')
f_iaga.write(
    ' Sensor Orientation     XYZ                                          |\n')
f_iaga.write(
    ' Digital Sampling       1 second                                     |\n')
f_iaga.write(
    ' Data Interval Type     Filtered 1-minute (00:15-01:45)              |\n')
f_iaga.write(
    ' Data Type              variation                                    |\n')
f_iaga.write(
    'DATE       TIME         DOY     TUNX      TUNY      TUNZ      TUNF   |\n')

for j in range(0, 1440):
    body_iaga = '%s     %8.2f  %8.2f  %8.2f  %8.2f\n' % (
        (date1 + timedelta(minutes=j)).strftime("%Y-%m-%d %H:%M:%S.000 %j"), x_mean[j], y_mean[j], z_mean[j], f_mean[j])
    f_iaga.write(body_iaga)
f_iaga.write(' ')
f_iaga.close()

print '%s converted to %s' % (filename, fileout)
