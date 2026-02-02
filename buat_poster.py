#!/usr/bin/env python3
"""
Generator Poster Akademik DONGOL
Poster A0/A1 untuk pameran
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Create figure (A1 size ratio: 594 x 841 mm)
fig = plt.figure(figsize=(23.4, 33.1), dpi=150)
fig.patch.set_facecolor('white')

# Main title area
ax_title = fig.add_axes([0.05, 0.92, 0.9, 0.07])
ax_title.set_xlim(0, 1)
ax_title.set_ylim(0, 1)
ax_title.axis('off')

# Title box
title_box = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", 
                           facecolor='#1e3a5f', edgecolor='black', linewidth=3)
ax_title.add_patch(title_box)

ax_title.text(0.5, 0.65, 'DONGOL', fontsize=72, ha='center', va='center', 
              color='white', fontweight='bold', family='sans-serif')
ax_title.text(0.5, 0.30, 'Distributed Orchestration for Navigating Goals and Operational Logic', 
              fontsize=24, ha='center', va='center', color='#cccccc', style='italic')

# Author info
ax_author = fig.add_axes([0.05, 0.88, 0.9, 0.035])
ax_author.set_xlim(0, 1)
ax_author.set_ylim(0, 1)
ax_author.axis('off')

ax_author.text(0.5, 0.5, 
    'Ardellio Satria Anindito  |  SMA Kartika XIX-1 Bandung  |  Kelas 1 SMA  |  Surabaya, 2008',
    fontsize=18, ha='center', va='center', color='#333333', fontweight='bold')

# Left column - Abstract & Introduction
ax_abstract = fig.add_axes([0.05, 0.72, 0.42, 0.14])
ax_abstract.set_xlim(0, 1)
ax_abstract.set_ylim(0, 1)
ax_abstract.axis('off')

# Section header
header_box = FancyBboxPatch((0, 0.85), 1, 0.15, boxstyle="round,pad=0.01",
                            facecolor='#2980b9', edgecolor='black', linewidth=2)
ax_abstract.add_patch(header_box)
ax_abstract.text(0.5, 0.92, 'ABSTRAK', fontsize=20, ha='center', va='center', 
                 color='white', fontweight='bold')

abstract_text = """DONGOL merupakan sistem manajemen tugas paralel yang 
mengimplementasikan arsitektur terdistribusi modern dengan 
teknik chunking cerdas dan dependency tracking.

Hasil: Speedup 4.5x, 48.713 tasks/detik, 
 throughput 1.644 MB/detik"""

ax_abstract.text(0.5, 0.40, abstract_text, fontsize=14, ha='center', va='center',
                 color='#333333', linespacing=1.8, family='sans-serif')

# Left column - Architecture
ax_arch = fig.add_axes([0.05, 0.45, 0.42, 0.25])
ax_arch.set_xlim(0, 1)
ax_arch.set_ylim(0, 1)
ax_arch.axis('off')

header_box2 = FancyBboxPatch((0, 0.92), 1, 0.08, boxstyle="round,pad=0.01",
                             facecolor='#27ae60', edgecolor='black', linewidth=2)
ax_arch.add_patch(header_box2)
ax_arch.text(0.5, 0.96, 'ARSITEKTUR SISTEM', fontsize=18, ha='center', va='center',
             color='white', fontweight='bold')

# Architecture boxes
layers = [
    (0.1, 0.75, 0.8, 0.12, 'Presentation Layer\nCLI | REST API | WebSocket | SDK', '#e74c3c'),
    (0.1, 0.55, 0.8, 0.15, 'Unified Core Engine\nAsync Event Loop | Task Scheduler\nState Machine | Memory Manager', '#3498db'),
    (0.1, 0.30, 0.25, 0.20, 'Parallel\nThinker\nMatrix', '#9b59b6'),
    (0.375, 0.30, 0.25, 0.20, 'Intelligent\nChunking\nEngine', '#f39c12'),
    (0.65, 0.30, 0.25, 0.20, 'Context\nMemory\nSystem', '#1abc9c'),
    (0.1, 0.05, 0.8, 0.10, 'Persistence Layer | SQLite | Sled | File System | Cloud', '#34495e'),
]

for x, y, w, h, text, color in layers:
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                         facecolor=color, edgecolor='black', linewidth=2, alpha=0.9)
    ax_arch.add_patch(box)
    ax_arch.text(x + w/2, y + h/2, text, ha='center', va='center',
                 fontsize=11, color='white', fontweight='bold',
                 linespacing=1.3)

# Arrows
for y in [0.73, 0.53, 0.28]:
    ax_arch.annotate('', xy=(0.5, y), xytext=(0.5, y+0.05),
                     arrowprops=dict(arrowstyle='->', lw=3, color='black'))

# Right column - Benchmark Results
ax_bench = fig.add_axes([0.52, 0.72, 0.43, 0.26])
ax_bench.set_xlim(0, 1)
ax_bench.set_ylim(0, 1)
ax_bench.axis('off')

header_box3 = FancyBboxPatch((0, 0.92), 1, 0.08, boxstyle="round,pad=0.01",
                             facecolor='#e67e22', edgecolor='black', linewidth=2)
ax_bench.add_patch(header_box3)
ax_bench.text(0.5, 0.96, 'HASIL BENCHMARK', fontsize=18, ha='center', va='center',
              color='white', fontweight='bold')

# Benchmark chart
categories = ['Task\nCreation', 'Throughput', 'Parallel\nSpeedup', 'Memory\nUsage']
target = [1, 10000, 2, 50]
achieved = [0.021, 48713, 4.5, 35]

x = np.arange(len(categories))
width = 0.35

# Normalize for visualization
target_norm = [1, 10000/5000, 2/2, 50/50]  # Scale to 1
achieved_norm = [0.021/1, 48713/5000, 4.5/2, 35/50]

ax_chart = fig.add_axes([0.55, 0.78, 0.38, 0.15])
ax_chart.bar(x - width/2, target_norm, width, label='Target', color='#95a5a6', edgecolor='black')
ax_chart.bar(x + width/2, achieved_norm, width, label='Achieved', color='#2ecc71', edgecolor='black')
ax_chart.set_ylabel('Relative Performance', fontsize=12)
ax_chart.set_xticks(x)
ax_chart.set_xticklabels(categories, fontsize=10)
ax_chart.legend(fontsize=10)
ax_chart.set_title('Performance vs Target', fontsize=14, fontweight='bold')

# Speedup highlight
ax_bench.text(0.5, 0.35, '4.5x SPEEDUP!', fontsize=36, ha='center', va='center',
              color='#e74c3c', fontweight='bold',
              bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

ax_bench.text(0.5, 0.15, 'Sequential: 11.47s\nDONGOL: 2.55s\n(501 files, 4.19 GB)',
              fontsize=14, ha='center', va='center', linespacing=1.5)

# Right column - Real Data Analysis
ax_data = fig.add_axes([0.52, 0.42, 0.43, 0.28])
ax_data.set_xlim(0, 1)
ax_data.set_ylim(0, 1)
ax_data.axis('off')

header_box4 = FancyBboxPatch((0, 0.92), 1, 0.08, boxstyle="round,pad=0.01",
                             facecolor='#8e44ad', edgecolor='black', linewidth=2)
ax_data.add_patch(header_box4)
ax_data.text(0.5, 0.96, 'ANALISIS DATA NYATA', fontsize=18, ha='center', va='center',
             color='white', fontweight='bold')

# Stats boxes
stats = [
    ('2,979', 'Files'),
    ('23.12', 'GB'),
    ('95', 'Types'),
    ('48s', 'Analysis'),
]

for i, (value, label) in enumerate(stats):
    x = 0.12 + (i % 2) * 0.45
    y = 0.60 if i < 2 else 0.25
    
    box = FancyBboxPatch((x, y), 0.38, 0.25, boxstyle="round,pad=0.02",
                         facecolor='#3498db', edgecolor='black', linewidth=2)
    ax_data.add_patch(box)
    ax_data.text(x + 0.19, y + 0.15, value, fontsize=28, ha='center', va='center',
                 color='white', fontweight='bold')
    ax_data.text(x + 0.19, y + 0.06, label, fontsize=16, ha='center', va='center',
                 color='#ecf0f1')

# Right column - Conclusion
ax_conc = fig.add_axes([0.52, 0.15, 0.43, 0.25])
ax_conc.set_xlim(0, 1)
ax_conc.set_ylim(0, 1)
ax_conc.axis('off')

header_box5 = FancyBboxPatch((0, 0.92), 1, 0.08, boxstyle="round,pad=0.01",
                             facecolor='#c0392b', edgecolor='black', linewidth=2)
ax_conc.add_patch(header_box5)
ax_conc.text(0.5, 0.96, 'KESIMPULAN', fontsize=18, ha='center', va='center',
             color='white', fontweight='bold')

conclusions = [
    '✓ Speedup 4.5x tercapai',
    '✓ 48.713 tasks/detik',
    '✓ Validasi pada 23.12 GB data nyata',
    '✓ Sistem siap produksi'
]

for i, conc in enumerate(conclusions):
    ax_conc.text(0.5, 0.70 - i*0.18, conc, fontsize=16, ha='center', va='center',
                 color='#2c3e50', fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#ecf0f1', alpha=0.9))

# Bottom logos/QR area
ax_bottom = fig.add_axes([0.05, 0.02, 0.9, 0.10])
ax_bottom.set_xlim(0, 1)
ax_bottom.set_ylim(0, 1)
ax_bottom.axis('off')

bottom_box = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.01",
                            facecolor='#ecf0f1', edgecolor='black', linewidth=2)
ax_bottom.add_patch(bottom_box)

ax_bottom.text(0.5, 0.5, 
    'SMA Kartika XIX-1 Bandung  |  Kelas 1 SMA  |  Surabaya 2008  |  16 Tahun',
    fontsize=16, ha='center', va='center', color='#2c3e50', fontweight='bold')

plt.savefig('Poster_DONGOL_Ardellio.png', dpi=150, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
print("✓ Poster akademik berhasil dibuat!")
print("  File: Poster_DONGOL_Ardellio.png")
print("  Ukuran: A1 (23.4 x 33.1 inch)")
print("  Resolusi: 150 DPI")

# Also save PDF version
plt.savefig('Poster_DONGOL_Ardellio.pdf', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print("  File PDF juga tersedia: Poster_DONGOL_Ardellio.pdf")
