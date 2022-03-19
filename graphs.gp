# Gnuplot script file for plotting utility consumption
# How to make the size of the plot depend on the number of data points:
# http://stackoverflow.com/questions/13869439/gnuplot-how-to-increase-the-width-of-my-graph

# don't make any output just yet
#set terminal unknown

# plot the data file to get information on ranges
set xdata time
set timefmt "%d-%m-%Y"
plot "diff.txt" using 1:2 title "El"

# span of data in x and y
xspan = GPVAL_DATA_X_MAX - GPVAL_DATA_X_MIN
yspan = GPVAL_DATA_Y_MAX - GPVAL_DATA_Y_MIN

# print xspan gives 94608000.0 for three years, scale 1500 pixels accordingly
xdim = 1500*xspan/95000000
ydim = 680
print "Plot width is ", xdim, " pixels"

set term jpeg size xdim,ydim

set title "El forbrug per 30 dage"
set xdata time
set timefmt "%d-%m-%Y"
set xlabel "Dato"
set ylabel "El [kWh/30dage]"
set format x "%d/%m/%y"
set output "power.jpg"
plot "diff.txt" using 1:2 title "El" with linespoints

set title "Vand forbrug per 30 dage"
set xdata time
set timefmt "%d-%m-%Y"
set xlabel "Dato"
set ylabel "Vand [m³/30dage]"
set format x "%d/%m/%y"
set output "water.jpg"
plot "diff.txt" using 1:3 title "Vand" with linespoints

set title "Varmeenergi forbrug per 30 dage"
set xdata time
set timefmt "%d-%m-%Y"
set xlabel "Dato"
set ylabel "Varme [MWh/30dage]"
set format x "%d/%m/%y"
set output "energy.jpg"
plot "diff.txt" using 1:4 title "Varme" with linespoints

set title "Fjernvarmevand forbrug per 30 dage"
set xdata time
set timefmt "%d-%m-%Y"
set xlabel "Dato"
set ylabel "Fjernvarmevand [m³/30dage]"
set format x "%d/%m/%y"
set output "hotwater.jpg"
plot "diff.txt" using 1:5 title "Fjernvarmevand" with linespoints


set title "Tilløbs- og fraløbstemperatur samt gennemsnitlig afkøling"
set xdata time
set timefmt "%d-%m-%Y"
set xlabel "Dato"
set ylabel "Temperatur [grader C]"
set format x "%d/%m/%y"
set output "temperature.jpg"
plot "diff.txt" using 1:6 title "Tilløb" with linespoints,\
     "diff.txt" using 1:7 title "Fraløb" with linespoints,\
     "diff.txt" using 1:8 title "Middelafkøling" with linespoints

