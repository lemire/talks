load "linespointsstyle.gnuplot"
stats "results.txt"   using 1:0 nooutput
set out "timings.png"
set term pngcairo
set xlabel "sample"
set ylabel "time (ns)"
#set yrange [0:]
#set label 1 sprintf("average = %3.1f",STATS_mean_x) at 50,(STATS_mean_x+400) font "arialbd,18"
#set label 2 sprintf("minimum = %3.1f",STATS_min_x) at 50,(STATS_min_x+400) font "arialbd,18"

plot "results.txt" u 0:1 w lines ti 'raw timings' ls 1, "" u 0:(STATS_mean_x) w lines ti 'average'  ls 2, "" u 0:(STATS_min_x) w lines ti 'minimum'  ls 3

set out "instructions.png"
set ylabel "instructions"
stats "results.txt"  using 3:0  nooutput
plot "results.txt" u 0:3 w lines ti 'raw timings' ls 1, "" u 0:(STATS_mean_x) w lines ti 'average'  ls 2, "" u 0:(STATS_min_x) w lines ti 'minimum'  ls 3


set out "cycles.png"
set ylabel "cycles"
stats "results.txt"  using 2:0  nooutput
plot "results.txt" u 0:2 w lines ti 'raw timings' ls 1, "" u 0:(STATS_mean_x) w lines ti 'average'  ls 2, "" u 0:(STATS_min_x) w lines ti 'minimum'  ls 3



stats "trimmed_results.txt"   using 1:0 nooutput
set out "trimmed_timings.png"
set ylabel "time (ns)"

plot "trimmed_results.txt" u 0:1 w lines ti 'raw timings' ls 1, "" u 0:(STATS_mean_x) w lines ti 'average'  ls 2, "" u 0:(STATS_min_x) w lines ti 'minimum'  ls 3

set out "trimmed_instructions.png"
set ylabel "instructions"
stats "trimmed_results.txt"  using 3:0  nooutput
plot "trimmed_results.txt" u 0:3 w lines ti 'raw timings' ls 1, "" u 0:(STATS_mean_x) w lines ti 'average'  ls 2, "" u 0:(STATS_min_x) w lines ti 'minimum'  ls 3


set out "trimmed_cycles.png"
set ylabel "cycles"
stats "trimmed_results.txt"  using 2:0  nooutput
plot "trimmed_results.txt" u 0:2 w lines ti 'raw timings' ls 1, "" u 0:(STATS_mean_x) w lines ti 'average'  ls 2, "" u 0:(STATS_min_x) w lines ti 'minimum'  ls 3
