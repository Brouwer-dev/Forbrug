#!/usr/bin/python
# -*- coding: utf-8 -*-


# Read data file containing meter read offs in the format:
# Dato[DD-MM-YYYY] El[kWh] Vand[m³] Varme[MWh] Fjernvarmevand[m³] Tilløbstemp[C] Fraløbstemp[C]
# Print average consumption normalised to 30 days to STDOUT in the format:
# Dato[DD-MM-YYYY] El[kWH/md] Vand[m³/md] Varme[MWh/md] Fjernvarmevand[m³/md] Tilløbstemp[C] Fraløbstemp[C] Middelafkøling[C]
# The average consumption is computed as the difference to the last meter read off divided by number of days passed, times 30.
# Average water cooling is computed as follows:
# Cooling of 1 litre water 1 degree yields 1000 cal = 4.18 kJ = 4.18/3600 kWh (as 1 Wh = 3600 J, 1 W = 1 J/s)
# Cooling of 1 m³ water 1 degree yields 4.18/3600 MWh.
# That is, 4.18/3600 MWh/m³/degree and the formula for average cooling is
# (E * 36000)/(V * 4.18) = E * 860 / V
# E = energy consumption i MWh, V = water volume in m³

import sys
import re
import datetime
from cryptography.fernet import Fernet

if (len(sys.argv) < 2):
    print('Usage:', sys.argv[0], '<datafile>')
    sys.exit()

datafile = open(sys.argv[1], 'r')
lines = datafile.readlines()
datafile.close()

print("# Denne fil er autogenereret og bruges som input til Gnuplot.")
print("# Den indeholder dato for aflæsning, normaliseret forbrug siden sidste aflæsning, samt temperatur aflæsning.")
print("# Dato[DD-MM-YYYY] El[kWH/md] Vand[m³/md] Varme[MWh/md] Fjernvarmevand[m³/md] Tilløbstemp[C] Fraløbstemp[C] Middelafkøling[C]\n")

prev = []
for i in range(len(lines)):
    if (re.match("^\d\d-\d\d-\d{4}", lines[i])):
        cur = lines[i].split()
        if (7 <= len(prev)):
            timenow  = cur[0]
            daynow   = int(timenow[0:2])
            monthnow = int(timenow[3:5])
            yearnow  = int(timenow[6:10])
            datenow  = datetime.date(yearnow, monthnow, daynow)
            timeprev = prev[0]
            dayprev  = int(timeprev[0:2])
            monthprev= int(timeprev[3:5])
            yearprev = int(timeprev[6:10])
            dateprev = datetime.date(yearprev, monthprev, dayprev)
            datediff = datenow - dateprev
            days     = datediff.days
            power    = int(cur[1]) - int(prev[1])
            water    = float(cur[2]) - float(prev[2])
            energy   = float(cur[3]) - float(prev[3])
            hotwater = float(cur[4]) - float(prev[4])
            # Hack for new "fjernvarme" meter
            energy   = energy if (0 < energy) else 0
            hotwater = hotwater if (0 < hotwater) else 0.01  # to avoid zero division
            # Hack for new water gauge 02 SEP 2015, initialised to 0
            if (datenow == datetime.date(2015,10,1)):
                water = float(cur[2]) - float(0)
            # Hack for new power meter 25 JUN 2019, initialised to 0
            if (datenow == datetime.date(2019,7,1)):
                power = float(cur[1]) - float(0)
            # Hack for new water meter 16 AUG 2024, initialised to 0
            if (datenow == datetime.date(2024,8,16)):
                water = float(cur[2]) - float(0)
            print(timenow, 30*power/days, 30*water/days, 30*energy/days, 30*hotwater/days, cur[5], cur[6], energy*860/hotwater)
        prev = cur

with open("fernet.key", "rb") as file:
    cryptoengine = Fernet(file.read())

ctextfile = sys.argv[1] + ".ctext"

with open(sys.argv[1], "rb") as file:
    ptext = file.read()
    ctext = cryptoengine.encrypt(ptext)
    #print(base64.urlsafe_b64decode(ctext))

with open(ctextfile, "wb") as file:
    file.write(ctext)

# Check decryption
with open(ctextfile, "rb") as file:
    ptextNew = cryptoengine.decrypt(file.read())

if ptext == ptextNew:
    print("Decryption verified succesfully", file=sys.stderr)
else:
    print("Error: decryption failed!!!", file=sys.stderr)
