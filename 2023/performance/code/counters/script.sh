make
sudo ./bench > results.txt
echo "$(tail -n +2 results.txt)" > trimmed_results.txt

gnuplot plot.gnuplot
