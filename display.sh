#!/bin/bash

python3 consumption.py meter-readings.txt > diff.txt

gnuplot graphs.gp

sleep 2

eog power.jpg&
eog water.jpg&
eog energy.jpg&
eog hotwater.jpg&
eog temperature.jpg&
