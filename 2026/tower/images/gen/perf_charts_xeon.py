#!/usr/bin/env python3
"""twitter.json parsing / serialization on the Intel Xeon Gold 6548N (big4), same style as the
Apple Silicon charts from simdjson_talks/cppcon2025 (generate_perf_charts.py).
Numbers: median of 3 runs of simdjson's benchmark/static_reflect/twitter_benchmark, GCC 16
(gcc:16 container, -O3, C++26 static reflection), pinned to one core. Raw log:
../../bench/simdjson_reflection_big4.log"""
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})

MACHINE = 'Intel Xeon Gold 6548N (Emerald Rapids)'

def chart(libs, speeds, colors, langs, title, ylim, out):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(libs, speeds, color=colors, edgecolor='black')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    for i, bar in enumerate(bars):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + ylim * 0.0125, f'{yval} MB/s', ha='center', va='bottom', fontsize=12)
        plt.text(bar.get_x() + bar.get_width() / 2, yval + ylim * 0.045, langs[i], ha='center', va='bottom',
                 fontsize=12, color='black', fontweight='bold', style='italic')
    bars[-1].set_linewidth(3)
    bars[-1].set_edgecolor('#FF0000')
    plt.ylabel('Throughput (MB/s)', fontsize=14)
    plt.ylim(0, ylim)
    plt.title(title, fontsize=16)
    plt.text(0.01, 0.99, MACHINE, transform=ax.transAxes, fontsize=14, ha='left', va='top', style='italic')
    plt.text(0.01, 0.89, 'twitter.json', transform=ax.transAxes, fontsize=14, ha='left', va='top', style='italic')
    plt.tight_layout()
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()

# parsing: bench_nlohmann_parsing, bench_rapidjson_parsing, bench_rust_parsing, bench_yyjson_parsing, bench_simdjson_from_parsing
chart(["nlohmann::json", "RapidJSON", "Serde (Rust)", "yyjson", "simdjson"],
      [153, 843, 1903, 1181, 4800],
      ['#8B8680', '#6495ED', '#FF6F61', '#2ECC71', '#FFD700'],
      ["C++", "C++", "Rust", "C", "C++"],
      'JSON Parsing Performance', 5500, '../perf_with_simdjson_parsing_xeon.png')

# serialization: bench_nlohmann, bench_reflect_cpp, bench_rust, bench_yyjson, bench_simdjson_to (simdjson::to_json)
chart(["nlohmann::json", "reflect-cpp", "Serde (Rust)", "yyjson", "simdjson"],
      [176, 1213, 1361, 1537, 6574],
      ['#8B8680', '#6495ED', '#FF6F61', '#2ECC71', '#FFD700'],
      ["C++", "C++", "Rust", "C", "C++"],
      'JSON Serialization Performance', 7500, '../perf_with_simdjson_xeon.png')
print("ok")
