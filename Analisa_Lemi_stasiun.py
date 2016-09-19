"""
@author: yosi setiawan
Modified by yanuar harry
signed-off yosi setiawan
signed-off yanuar harry

License GPLv3
"""

from scipy import signal
import numpy as np
from datetime import datetime
from datetime import timedelta
import re
import os
import errno
import sys
import matplotlib.pyplot as plt
import scipy
import matplotlib
import matplotlib.mlab
import numpy
import warnings


def bandpass(X, st, hp, lp):
    Xh = []
    Y = []
    SampleSec = st
    LowPeriod = lp
    HighPeriod = hp
    w1 = (float(SampleSec) * 2) / float(LowPeriod)
    w2 = (float(SampleSec) * 2) / float(HighPeriod)

    b, a = signal.butter(2, [w1, w2], btype='bandpass')
    for i in range(0, 1):
        Xh[i:] = [x - X[i] for x in X]
        Y[i:] = signal.filtfilt(
            b, a, Xh[i:], padtype='odd', padlen=3 * max(len(b) - 1, len(a) - 1))
    return Y


def normal_corr(data, comp):
    dataedit = list(np.tile(np.nan, len(data)))
    global Normal_H, Normal_D, Normal_Z
    if comp == 'H':
        datanormal = Normal_H
    elif comp == 'D':
        datanormal = Normal_D
    elif comp == 'Z':
        datanormal = Normal_Z

    for i in range(0, len(data)):
        if comp == 'H':
            if data[i] <= 44000 and data[i] >= 36000:
                dataedit[i] = data[i]
            else:
                dataedit[i] = datanormal[i]
        elif comp == 'D':
            if data[i] <= 100 and data[i] >= -200:
                dataedit[i] = data[i]
            else:
                dataedit[i] = datanormal[i]
        elif comp == 'Z':
            if data[i] <= -8000 and data[i] >= -24000:
                dataedit[i] = data[i]
            else:
                dataedit[i] = datanormal[i]
    return dataedit


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def cart2pol(x, y):
    radius = np.hypot(x, y)
    theta = np.arctan2(y, x)
    return theta, radius


def compass(u, v, w, x, y):
    arrowprops = dict(color='darkorange', linewidth=2)
    angles = u
    radii = v
    fig, ax = plt.subplots(subplot_kw=dict(polar=True))

    kw = dict(arrowstyle="->", color='k')
    if arrowprops:
        kw.update(arrowprops)
    [ax.annotate("", xy=(angle, radius), xytext = (0, 0), arrowprops = kw)
     for angle, radius in zip([angles], [radii])]

    ax.set_ylim(0, np.max(radii))
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_title('Analisa Azimuth-%s\nAz = %3.3f Degree NE\nAmp = %3.3f' %
                 (w.strftime('%Y-%m-%d'), np.rad2deg(x), y))
    plt.tight_layout()
    plt.savefig('/home/tuntsi/Magnet_dev/azimuth_file/%s/%s/%s.png' %
                (str(w.year), str(w.month).zfill(2), w.strftime('%Y-%m-%d')), dpi=150)


def make_sure_path_exist(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


make_sure_path_exist("/home/tuntsi/Magnet_dev/correction_file")
make_sure_path_exist("/home/tuntsi/Magnet_dev/azimuth_file")
yyyy = []
mo = []
dd = []
hh = []
mm = []
ss = []
Bh = list(np.tile(np.nan, 86400))
Bd = list(np.tile(np.nan, 86400))
Bz = list(np.tile(np.nan, 86400))
Bf = list(np.tile(np.nan, 86400))
Bx = list(np.tile(np.nan, 86400))
Bi = list(np.tile(np.nan, 86400))
By = list(np.tile(np.nan, 86400))
Normal_H = list(np.tile(np.nan, 86400))
Normal_D = list(np.tile(np.nan, 86400))
Normal_Z = list(np.tile(np.nan, 86400))
date1 = datetime.utcnow() - timedelta(days=1)

dt = (date1 - datetime(1970, 1, 1)).total_seconds()
tahun1 = int(date1.year)
bulan1 = int(date1.month)
tanggal1 = int(date1.day)

filename = '/home/tuntsi/Magnet_dev/normal.txt'
with open(filename) as f_normal:
    content = f_normal.readlines()
    for i in range(0, len(content)):
        data = re.split('\s+', content[i])
        Normal_H[i] = float(data[0])
        Normal_D[i] = float(data[1])
        Normal_Z[i] = float(data[2])

namafolder = '/home/tuntsi/Magnet_dev/LEMIDATA/' + \
    str(tahun1) + '/' + str(bulan1).zfill(2)
filename = namafolder + '/' + \
    '%4.0f %02.0f %02.0f 00 00 00.txt' % (tahun1, bulan1, tanggal1)
with open(filename) as f_lemi:
    content = f_lemi.readlines()
    for i in range(0, len(content)):
        if len(content) < 77760:
            print 'Too many lost data'
            sys.exit(0)
        data = re.split('\s+', content[i])
        yyyy = float(data[0])
        mo = float(data[1])
        dd = float(data[2])
        hh = float(data[3])
        mm = float(data[4])
        ss = float(data[5])
        index = int((hh * 3600) + (mm * 60) + ss)
        Bx[index] = float(data[6])
        By[index] = float(data[7])
        Bz[index] = float(data[8])
        Bf[index] = np.sqrt(
            (Bx[index] ** 2) + (By[index] ** 2) + (Bz[index] ** 2))
        Bh[index] = float('%9.3f' % np.sqrt(Bx[index] ** 2 + By[index] ** 2))
        Bd[index] = 60 * np.degrees(np.arctan(By[index] / Bx[index]))
        Bi[index] = np.rad2deg(np.arctan(Bz[index] / Bh[index]))

dataedit_H = np.array(normal_corr(Bh, 'H'))
dataedit_D = np.array(normal_corr(Bd, 'D'))
dataedit_Z = np.array(normal_corr(Bz, 'Z'))
dataedit_F = np.sqrt((dataedit_H ** 2) + (dataedit_Z ** 2))
dataedit_X = dataedit_H * np.cos(np.deg2rad(dataedit_D / 60))
dataedit_Y = dataedit_H * np.sin(np.deg2rad(dataedit_D / 60))

fileout = str(tahun1) + str(bulan1).zfill(2) + str(tanggal1).zfill(2) + '.corr'
f_corr = open('/home/tuntsi/Magnet_dev/correction_file/' + fileout, 'w')
for j in range(0, len(dataedit_H)):
    corr = '%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f\n' % (
        dataedit_H[j], dataedit_D[j], dataedit_Z[j], dataedit_F[j], dataedit_X[j], dataedit_Y[j])
    f_corr.write(corr)
f_corr.write(' ')
f_corr.close()

Hbp = np.array(bandpass(dataedit_H, 1, 3, 600))
Zbp = np.array(bandpass(dataedit_Z, 1, 3, 600))

H15 = Hbp[50399:53999]
H16 = Hbp[53999:57599]
H17 = Hbp[57599:61199]
H18 = Hbp[61199:64799]
H19 = Hbp[64799:68399]
H20 = Hbp[68399:71999]

Z15 = Zbp[50399:53999]
Z16 = Zbp[53999:57599]
Z17 = Zbp[57599:61199]
Z18 = Zbp[61199:64799]
Z19 = Zbp[64799:68399]
Z20 = Zbp[68399:71999]

[Hs15, Fh15] = matplotlib.mlab.complex_spectrum(
    H15, Fs=1, window=numpy.hamming(3600))
[Hs16, Fh16] = matplotlib.mlab.complex_spectrum(
    H16, Fs=1, window=numpy.hamming(3600))
[Hs17, Fh17] = matplotlib.mlab.complex_spectrum(
    H17, Fs=1, window=numpy.hamming(3600))
[Hs18, Fh18] = matplotlib.mlab.complex_spectrum(
    H18, Fs=1, window=numpy.hamming(3600))
[Hs19, Fh19] = matplotlib.mlab.complex_spectrum(
    H19, Fs=1, window=numpy.hamming(3600))
[Hs20, Fh20] = matplotlib.mlab.complex_spectrum(
    H20, Fs=1, window=numpy.hamming(3600))

[Zs15, Fz15] = matplotlib.mlab.complex_spectrum(
    Z15, Fs=1, window=numpy.hamming(3600))
[Zs16, Fz16] = matplotlib.mlab.complex_spectrum(
    Z16, Fs=1, window=numpy.hamming(3600))
[Zs17, Fz17] = matplotlib.mlab.complex_spectrum(
    Z17, Fs=1, window=numpy.hamming(3600))
[Zs18, Fz18] = matplotlib.mlab.complex_spectrum(
    Z18, Fs=1, window=numpy.hamming(3600))
[Zs19, Fz19] = matplotlib.mlab.complex_spectrum(
    Z19, Fs=1, window=numpy.hamming(3600))
[Zs20, Fz20] = matplotlib.mlab.complex_spectrum(
    Z20, Fs=1, window=numpy.hamming(3600))

Hrs15 = 10 * np.log10(abs(Hs15))
Hrs16 = 10 * np.log10(abs(Hs16))
Hrs17 = 10 * np.log10(abs(Hs17))
Hrs18 = 10 * np.log10(abs(Hs18))
Hrs19 = 10 * np.log10(abs(Hs19))
Hrs20 = 10 * np.log10(abs(Hs20))

Zrs15 = 10 * np.log10(abs(Zs15))
Zrs16 = 10 * np.log10(abs(Zs16))
Zrs17 = 10 * np.log10(abs(Zs17))
Zrs18 = 10 * np.log10(abs(Zs18))
Zrs19 = 10 * np.log10(abs(Zs19))
Zrs20 = 10 * np.log10(abs(Zs20))

Mat_Temp15 = []
Temp15 = [Fh15, Hrs15, Zrs15, Hrs15, Zrs15]
Mat_Temp16 = []
Temp16 = [Fh16, Hrs16, Zrs16, Hrs16, Zrs16]
Mat_Temp17 = []
Temp17 = [Fh17, Hrs17, Zrs17, Hrs17, Zrs17]
Mat_Temp18 = []
Temp18 = [Fh18, Hrs18, Zrs18, Hrs18, Zrs18]
Mat_Temp19 = []
Temp19 = [Fh19, Hrs19, Zrs19, Hrs19, Zrs19]
Mat_Temp20 = []
Temp20 = [Fh20, Hrs20, Zrs20, Hrs20, Zrs20]

i_P2015 = np.where(abs(Temp15[0] - 0.022) == min(abs(Temp15[0] - 0.022)))
i_P1015 = np.where(abs(Temp15[0] - 0.012) == min(abs(Temp15[0] - 0.012)))
i_P2016 = np.where(abs(Temp16[0] - 0.022) == min(abs(Temp16[0] - 0.022)))
i_P1016 = np.where(abs(Temp16[0] - 0.012) == min(abs(Temp16[0] - 0.012)))
i_P2017 = np.where(abs(Temp17[0] - 0.022) == min(abs(Temp17[0] - 0.022)))
i_P1017 = np.where(abs(Temp17[0] - 0.012) == min(abs(Temp17[0] - 0.012)))
i_P2018 = np.where(abs(Temp18[0] - 0.022) == min(abs(Temp18[0] - 0.022)))
i_P1018 = np.where(abs(Temp18[0] - 0.012) == min(abs(Temp18[0] - 0.012)))
i_P2019 = np.where(abs(Temp19[0] - 0.022) == min(abs(Temp19[0] - 0.022)))
i_P1019 = np.where(abs(Temp19[0] - 0.012) == min(abs(Temp19[0] - 0.012)))
i_P2020 = np.where(abs(Temp20[0] - 0.022) == min(abs(Temp20[0] - 0.022)))
i_P1020 = np.where(abs(Temp20[0] - 0.012) == min(abs(Temp20[0] - 0.012)))

Mat_Temp15 = [Temp15[0][i_P2015][0], Temp15[1][i_P2015][0],
              Temp15[2][i_P2015][0], Temp15[3][i_P1015][0], Temp15[4][i_P1015][0]]
Mat_Temp16 = [Temp16[0][i_P2016][0], Temp16[1][i_P2016][0],
              Temp16[2][i_P2016][0], Temp16[3][i_P1016][0], Temp16[4][i_P1016][0]]
Mat_Temp17 = [Temp17[0][i_P2017][0], Temp17[1][i_P2017][0],
              Temp17[2][i_P2017][0], Temp17[3][i_P1017][0], Temp17[4][i_P1017][0]]
Mat_Temp18 = [Temp18[0][i_P2018][0], Temp18[1][i_P2018][0],
              Temp18[2][i_P2018][0], Temp18[3][i_P1018][0], Temp18[4][i_P1018][0]]
Mat_Temp19 = [Temp19[0][i_P2019][0], Temp19[1][i_P2019][0],
              Temp19[2][i_P2019][0], Temp19[3][i_P1019][0], Temp19[4][i_P1019][0]]
Mat_Temp20 = [Temp20[0][i_P2020][0], Temp20[1][i_P2020][0],
              Temp20[2][i_P2020][0], Temp20[3][i_P1020][0], Temp20[4][i_P1020][0]]

Hasil15 = [
    tahun1, bulan1, tanggal1, 15, Mat_Temp15[1], Mat_Temp15[2], Mat_Temp15[3],
    Mat_Temp15[4], Mat_Temp15[2] / Mat_Temp15[1], Mat_Temp15[4] / Mat_Temp15[3]]
Hasil16 = [
    tahun1, bulan1, tanggal1, 16, Mat_Temp16[1], Mat_Temp16[2], Mat_Temp16[3],
    Mat_Temp16[4], Mat_Temp16[2] / Mat_Temp16[1], Mat_Temp16[4] / Mat_Temp16[3]]
Hasil17 = [
    tahun1, bulan1, tanggal1, 17, Mat_Temp17[1], Mat_Temp17[2], Mat_Temp17[3],
    Mat_Temp17[4], Mat_Temp17[2] / Mat_Temp17[1], Mat_Temp17[4] / Mat_Temp17[3]]
Hasil18 = [
    tahun1, bulan1, tanggal1, 18, Mat_Temp18[1], Mat_Temp18[2], Mat_Temp18[3],
    Mat_Temp18[4], Mat_Temp18[2] / Mat_Temp18[1], Mat_Temp18[4] / Mat_Temp18[3]]
Hasil19 = [
    tahun1, bulan1, tanggal1, 19, Mat_Temp19[1], Mat_Temp19[2], Mat_Temp19[3],
    Mat_Temp19[4], Mat_Temp19[2] / Mat_Temp19[1], Mat_Temp19[4] / Mat_Temp19[3]]
Hasil20 = [
    tahun1, bulan1, tanggal1, 20, Mat_Temp20[1], Mat_Temp20[2], Mat_Temp20[3],
    Mat_Temp20[4], Mat_Temp20[2] / Mat_Temp20[1], Mat_Temp20[4] / Mat_Temp20[3]]
Hasil = [Hasil15, Hasil16, Hasil17, Hasil18, Hasil19, Hasil20]

fileout = '/home/tuntsi/Magnet_dev/spectrum_magdas_Nighttime.txt'
if os.path.isfile(fileout) == False:
    f_spectrum = open(fileout, 'a')
    f_spectrum.write(
        'Year\tMonth\tDay\tHour\t   H 0.22\t  Z 0.22\t  H 0.12\t  Z 0.12\t Z/H 0.22\t Z/H 0.12\n')
else:
    f_spectrum = open(fileout, 'a')
    pass
for k in range(0, 6):
    f_spectrum.write('%4.0f\t%02.0f\t%02.0f\t%2.0f\t%8.3f\t%8.3f\t%8.3f\t%8.3f\t%8.3f\t%8.3f\n' %
                     (Hasil[k][0], Hasil[k][1], Hasil[k][2], Hasil[k][3], Hasil[k][4], Hasil[k][5], Hasil[k][6], Hasil[k][7], Hasil[k][8], Hasil[k][9]))
f_spectrum.close()

total_data = len(dataedit_X)
iterasi = int(np.floor(total_data / 3600))

Xs = np.zeros(24, dtype=complex)
Ys = np.zeros(24, dtype=complex)
Zs = np.zeros(24, dtype=complex)

for i in range(1, iterasi + 1):
    star = ((i - 1) * 3600)
    en = i * 3600
    X_hour = dataedit_X[star:en]
    Y_hour = dataedit_Y[star:en]
    Z_hour = dataedit_Z[star:en]

    [Xs1h, Fx] = matplotlib.mlab.complex_spectrum(
        X_hour, Fs=1, window=numpy.hamming(3600))
    [Ys1h, Fy] = matplotlib.mlab.complex_spectrum(
        Y_hour, Fs=1, window=numpy.hamming(3600))
    [Zs1h, Fz] = matplotlib.mlab.complex_spectrum(
        Z_hour, Fs=1, window=numpy.hamming(3600))

    Xs[i - 1] = Xs1h[180]
    Ys[i - 1] = Ys1h[180]
    Zs[i - 1] = Zs1h[180]

G = np.matrix([Ys.tolist(), Xs.tolist()])

m = (Zs.tolist() * np.conj(G).T) * ((G * np.conj(G).T).I)

A = m.tolist()[0][1]
B = m.tolist()[0][0]

Amp = np.sqrt(A * np.conj(A) + B * np.conj(B))
Dir = np.arctan(np.real(B) / np.real(A))

[x, y] = pol2cart(Dir, Amp)

if Dir > 6.2832 or Dir < - 6.2832:
    Dir1 = Dir / 6.2832
    Dir2 = Dir1 - float(Dir1) * 6.2832
else:
    Dir2 = Dir
if Dir2 < 0:
    Dir3 = 6.2832 + Dir2
else:
    Dir3 = Dir2

compass(Dir, np.real(Amp), date1, Dir3, np.real(Amp))
fileout = '/home/tuntsi/Magnet_dev/azimuth.txt'
f_azm = open(fileout, 'a')
f_azm.write('%8.0f %8.2f %8.2f\n' %
            ((datetime(year=tahun1, month=bulan1, day=tanggal1, hour=12, minute=0, second=0) - datetime(1970, 1, 1)).total_seconds(), np.rad2deg(Dir3), np.real(Amp)))
f_azm.close()

Dst_indeks = list(np.tile(np.nan, 24))
fileout = '/home/tuntsi/Magnet_dev/dst_index.txt'
f_dst = open(fileout, 'a')
for j in range(0, 24):
    if j == 0:
        Dst_indeks[j] = float('%9.3f' % dataedit_H[j]) - Normal_H[j]
    else:
        Dst_indeks[j] = float(
            '%9.3f' % dataedit_H[j * 3600 - 1]) - Normal_H[j * 3600 - 1]
    f_dst.write('%8.0f %8.2f\n' %
                ((datetime(year=tahun1, month=bulan1, day=tanggal1, hour=j, minute=0, second=0) - datetime(1970, 1, 1)).total_seconds(), Dst_indeks[j]))
f_dst.close()

filename = '/home/tuntsi/Magnet_dev/spectrum_magdas_Nighttime.txt'
fileout = '/home/tuntsi/Magnet_dev/plot_spektrum.txt'
with open(filename) as f_spectrum:
    content = f_spectrum.readlines()
    zh12 = list(np.tile(np.nan, len(content) - 1))
    for i in range(1, len(content)):
        data = re.split('\s+', content[i])
        zh12[i - 1] = float(data[9])
std_zh = np.std(zh12)
movar = list(np.tile(np.nan, len(content) - 1))
stdp = list(np.tile(np.nan, len(content) - 1))
stdn = list(np.tile(np.nan, len(content) - 1))
for i in range(0, len(content) - 1):
    movar[i] = np.mean(zh12[0 + i:18 + i])
    stdp[i] = movar[i] + std_zh
    stdn[i] = movar[i] - std_zh

f_plot = open(fileout, 'w+')
f_plot.write(
    'Second\t       Year\tMonth\tDay\tHour\t   Z/H 0.12\t    STD+\t    STD-\t\n')
for k in range(0, len(content) - 1):
    data = re.split('\s+', content[k + 1])
    f_plot.write('%8.0f\t%4.0f\t%2.0f\t%2.0f\t%2.0f\t%8.3f\t%8.3f\t%8.3f\n' %
                 ((datetime(year=int(data[0]), month=int(data[1]), day=int(data[2]), hour=(int(data[3]) * 4) - 60, minute=0, second=0) - datetime(1970, 1, 1)).total_seconds(), float(data[0]), float(data[1]), float(data[2]), float(data[3]), zh12[k - 1], stdp[k - 1], stdn[k - 1]))
f_plot.close()
