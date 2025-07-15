load "linespointsstyle.gnuplot"
set out "std_dev_timings.png"
set term pngcairo
set xlabel "sample"
set ylabel "standard deviation (ns)"

plot "std_scale_results.txt" u 1:2 w lines ti 'raw std dev' ls 1