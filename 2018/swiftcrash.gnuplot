set term pngcairo font "Arial,22"
set style line 80 lt rgb "#000000"
set border 3 back linestyle 80
set xtics nomirror
set ytics nomirror
set out "swiftcrash.png"
set xlabel "hash table size"
set ylabel "time (s)"
plot "swiftcrash.txt" using 1:2 notitle with linespoints lw 4
