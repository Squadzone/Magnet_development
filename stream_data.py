#!/usr/bin/env python

"""
@author: yosi setiawan
Modified by yanuar harry
signed-off yosi setiawan
signed-off yanuar harry

License GPL-v2
"""
import sys
import socket
import traceback
import time
import os
import os.path
import errno
import serial
import string
from datetime import datetime
from datetime import timedelta
from pylab import *
import time
import subprocess
import select
import datetime
from datetime import datetime

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
)


def make_sure_path_exist(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

make_sure_path_exist("/home/tuntsi/Magnet_dev/LEMI")
make_sure_path_exist("/home/tuntsi/Magnet_dev/LEMIRAW")
make_sure_path_exist("/home/tuntsi/Magnet_dev/LEMIRAWFILTER")
make_sure_path_exist("/home/tuntsi/Magnet_dev/LEMIDATA")
make_sure_path_exist("/home/tuntsi/Magnet_dev/LEMICLIENT")
make_sure_path_exist("/home/tuntsi/Magnet_dev/IAGA")
make_sure_path_exist("/home/tuntsi/Magnet_dev/IMFV")
make_sure_path_exist("/home/tuntsi/Magnet_dev/Excel")

if os.path.isfile('tmp') == True:
    os.remove('tmp')
else:
    pass

if os.path.isfile('tmp2') == True:
    os.remove('tmp2')
else:
    pass


def do_work(forever=True):
    last_t = datetime(
        year=2016, month=01, day=01, hour=00, minute=00, second=59)
    sekarang = datetime.utcnow()
    namafile = str(sekarang.year) + ' ' + str(sekarang.month).zfill(2) + \
        ' ' + str(sekarang.day).zfill(
            2) + ' ' + '00' + ' ' + '00' + ' ' + '00' + '.txt'
    namafileclient = 'tuntungan_lemi_raw_' + \
        str(sekarang.year) + str(sekarang.month).zfill(2) + \
        str(sekarang.day).zfill(2) + '.txt'

    if os.path.isfile('/home/tuntsi/Magnet_dev/LEMIRAW/' + namafile):
        f_lemi_raw = open('/home/tuntsi/Magnet_dev/LEMIRAW/' + namafile, 'a')
    else:
        f_lemi_raw = open('/home/tuntsi/Magnet_dev/LEMIRAW/' + namafile, 'w+')

    namefolder = '/home/tuntsi/Magnet_dev/LEMI/' + \
        str(sekarang.year) + '/' + str(sekarang.month).zfill(2)
    make_sure_path_exist(namefolder)
    if os.path.isfile(namefolder + '/' + namafile):
        f_lemi = open(namefolder + '/' + namafile, 'a')
    else:
        f_lemi = open(namefolder + '/' + namafile, 'w+')

    namefolderdata = '/home/tuntsi/Magnet_dev/LEMIDATA/' + \
        str(sekarang.year) + '/' + str(sekarang.month).zfill(2)
    make_sure_path_exist(namefolderdata)
    if os.path.isfile(namefolderdata + '/' + namafile):
        f_lemi_data = open(namefolderdata + '/' + namafile, 'a')
    else:
        f_lemi_data = open(namefolderdata + '/' + namafile, 'w+')

    namefolderrawfilter = '/home/tuntsi/Magnet_dev/LEMIRAWFILTER/' + \
        str(sekarang.year) + '/' + str(sekarang.month).zfill(2)
    make_sure_path_exist(namefolderrawfilter)
    if os.path.isfile(namefolderrawfilter + '/' + namafile):
        f_lemi_raw_filter = open(namefolderrawfilter + '/' + namafile, 'a')
    else:
        f_lemi_raw_filter = open(namefolderrawfilter + '/' + namafile, 'w+')

    namefolderclient = '/home/tuntsi/Magnet_dev/LEMICLIENT/' + \
        str(sekarang.year) + '/' + str(sekarang.month).zfill(2)
    make_sure_path_exist(namefolderclient)
    if os.path.isfile(namefolderclient + '/' + namafileclient):
        f_lemi_client = open(namefolderclient + '/' + namafileclient, 'a')
    else:
        f_lemi_client = open(namefolderclient + '/' + namafileclient, 'w+')

    time.sleep(1)

    while ser.isOpen():
        try:
            datamag = ser.readline()
            data = datamag.split(' ')
            if int(data[0]) == sekarang.year:
                tahun = int(data[0])
            else:
                tahun = lasttahun
            bulan = int(data[1])
            tanggal = int(data[2])
            jam = int(data[3])
            menit = int(data[4])
            detik = int(data[5])
            if float(data[7]) > 40000.0 and float(data[7]) < 45000.0:
                X = float(data[7])
            else:
                X = lastX
            if float(data[12]) > -100.0 and float(data[12]) < 100.0:
                Y = float(data[12])
            else:
                Y = lastY
            if float(data[14]) > -8000.0 and float(data[14]) < -6000.0:
                Z = float(data[14])
            else:
                Z = lastZ
            if float(data[16]) > 10.0 and float(data[16]) < 40.0:
                Te = float(data[16])
            else:
                Te = lastTe
            if float(data[18]) > 10.0 and float(data[18]) < 40.0:
                Tf = float(data[18])
            else:
                Tf = lastTf
            if float(data[23]) > 1.0 and float(data[23]) < 100.0:
                Bt = float(data[23])
            else:
                Bt = lastBt

        except ValueError:
            continue
        except IndexError:
            continue

        # change baseline here
        X = X - 41300
        # Y = Y + 278
        Z = Z + 7100
        # change baseline end

        lasttahun = tahun
        lastbulan = bulan
        lasttanggal = tanggal
        lastjam = jam
        lastmenit = menit
        lastdetik = detik
        lastX = X
        lastY = Y
        lastZ = Z
        lastTe = Te
        lastTf = Tf
        lastBt = Bt

        format_lemi = '%4.0f %02.0f %02.0f %02.0f %02.0f %02.0f %5.2f %5.2f %5.2f %5.2f %5.2f A N FL %2.0f\r\n' % (
            tahun, bulan, tanggal, jam, menit, detik, X, Y, Z, Te, Tf, Bt)
        format_lemi_data = '%4.0f %02.0f %02.0f %02.0f %02.0f %02.0f %5.2f %5.2f %5.2f %5.2f %5.2f %2.0f\r\n' % (
            tahun, bulan, tanggal, jam, menit, detik, X, Y, Z, Te, Tf, Bt)
        format_lemi_raw = '%4.0f %02.0f %02.0f %02.0f %02.0f %02.0f %5.2f %5.2f %5.2f %5.2f %5.2f %2.0f\r\n' % (
            tahun, bulan, tanggal, jam, menit, detik, (X + 41300), Y, (Z - 7100), Te, Tf, Bt)
        t = datetime(year=tahun, month=bulan, day=tanggal,
                     hour=jam, minute=menit, second=detik)
        dt = (t - datetime(1970, 1, 1)).total_seconds()

        if ((t - last_t).total_seconds() == 1.0) or ((t - last_t).total_seconds() > 100):
            format_lemi2 = '%8.0f %8.2f %7.2f %7.2f %5.2f %5.2f\n' % (
                dt, X, Y, Z, Te, Tf)

            if (jam + menit + detik == 0):
                namafile = str(tahun) + ' ' + str(bulan).zfill(2) + ' ' + str(
                    tanggal).zfill(2) + ' ' + '00' + ' ' + '00' + ' ' + '00' + '.txt'
                namafileclient = 'tuntungan_lemi_raw_' + \
                    str(tahun) + str(bulan).zfill(
                        2) + str(tanggal).zfill(2) + '.txt'
                f_lemi_raw.close()
                f_lemi_raw = open(
                    '/home/tuntsi/Magnet_dev/LEMIRAW/' + namafile, 'w+')
                namefolder = '/home/tuntsi/Magnet_dev/LEMI/' + \
                    str(tahun) + '/' + str(bulan).zfill(2)
                make_sure_path_exist(namefolder)
                f_lemi.close()
                f_lemi = open(namefolder + '/' + namafile, 'w+')
                namefolderdata = '/home/tuntsi/Magnet_dev/LEMIDATA/' + \
                    str(tahun) + '/' + str(bulan).zfill(2)
                make_sure_path_exist(namefolderdata)
                f_lemi_data.close()
                f_lemi_data = open(namefolderdata + '/' + namafile, 'w+')
                namefolderrawfilter = '/home/tuntsi/Magnet_dev/LEMIRAWFILTER/' + \
                    str(tahun) + '/' + str(bulan).zfill(2)
                make_sure_path_exist(namefolderrawfilter)
                f_lemi_raw_filter.close()
                f_lemi_raw_filter = open(
                    namefolderrawfilter + '/' + namafile, 'w+')
                namefolderclient = '/home/tuntsi/Magnet_dev/LEMICLIENT/' + \
                    str(tahun) + '/' + str(bulan).zfill(2)
                make_sure_path_exist(namefolderclient)
                f_lemi_client.close()
                f_lemi_client = open(
                    namefolderclient + '/' + namafileclient, 'w+')

            f_lemi_raw.write(datamag)
            f_lemi_raw.flush()
            f_lemi.write(format_lemi)
            f_lemi.flush()
            f_lemi_data.write(format_lemi_data)
            f_lemi_data.flush()
            f_lemi_raw_filter.write(format_lemi_raw)
            f_lemi_raw_filter.flush()
            f_lemi_client.write(datamag)
            f_lemi_client.flush()

            f_lemi_tmp = open('/home/tuntsi/Magnet_dev/tmp', 'a')
            f_lemi_tmp.write(format_lemi2)
            f_lemi_tmp.flush()
            f_lemi_tmp2 = open('/home/tuntsi/Magnet_dev/tmp2', 'a')
            f_lemi_tmp2.write(format_lemi2)
            f_lemi_tmp2.flush()
            last_t = t
            print '%4.0f %02.0f %02.0f %02.0f %02.0f %02.0f %5.2f %5.2f %5.2f %5.2f %5.2f A N FL %2.0f' % (tahun, bulan, tanggal, jam, menit, detik, X, Y, Z, Te, Tf, Bt)
        else:
            log = open('/home/tuntsi/Magnet_dev/log', 'a')
            tt = datetime.strftime(last_t, "%Y-%m-%d %H:%M:%S") + \
                '         ' + \
                datetime.strftime(
                    t, "%Y-%m-%d %H:%M:%S\n")
            log.write(tt)
            continue

if __name__ == '__main__':

    do_work(True)
    ser.close()
