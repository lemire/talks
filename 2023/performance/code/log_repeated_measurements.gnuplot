! python3 log-repeated_measurements.py > log-repeated_measurements.txt
load "linespointsstyle.gnuplot"
set out "log-repeated_measurements.png"
set term pngcairo
set xlabel "sample"
set ylabel "standard deviation (ns)"

plot "log-repeated_measurements.txt" u 1:2 w lines ti 'simulated std dev' ls 1