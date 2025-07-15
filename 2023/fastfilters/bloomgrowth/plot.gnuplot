set term pngcairo fontscale 1.2
set xlabel "number of entries"

set out "fpp.png"
set ylabel "false positive rate"
plot "metric.txt" u 1:4 w lines notitle lw 3
set out "bloom_bits_per_entry.png"

set ylabel "bits per entries"
set logscale y 10
plot "metric.txt" u 1:2 w lines notitle lw 3