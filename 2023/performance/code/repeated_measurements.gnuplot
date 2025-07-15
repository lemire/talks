! python3 repeated_measurements.py > repeated_measurements.txt
load "linespointsstyle.gnuplot"
set out "repeated_measurements.png"
set term pngcairo
set xlabel "sample"
set ylabel "standard deviation (ns)"

plot "repeated_measurements.txt" u 1:2 w lines ti 'simulated std dev' ls 1