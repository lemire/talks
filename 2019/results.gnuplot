set term pngcairo fontscale 2
set out "results.png"
set ylabel "Performance (GB/s)"
set xlabel "timestamp"
set ytics format "%.2f"
set xtics format ""
set key center
plot "twitterjson.txt" using 2:3 w lines lw 5 notitle
