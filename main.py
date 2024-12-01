import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import scienceplots

plt.style.use(['science','ieee','no-latex'])
plt.rcParams.update({'font.size': 6})

# Inches don't make sense for me, so I use cm
cm = 1/2.54

def initialize_plot(title, xlabel, ylabel):
  fig, ax = plt.subplots()
  ax.set_title("")
  # ax.set_title(title)
  fig.set_figheight(3.5*cm)
  ax.set_xlabel(xlabel)
  # ax.set_ylim(0, 16)
  ax.set_xscale("log", base=2)
  ax.set_ylabel(ylabel)
  ax.grid(True, which="both", ls="-")
  ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
  ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
  return (fig, ax)

def collect_max_avg_and_plot(df, names, metric, marker, color, label, ax, linestyle='none'):
  df = df[df['name'].isin(names)].groupby(['size', 'name']).mean().groupby('size')[metric].max().reset_index()
  plot(df, metric, marker, color, label, ax, linestyle)

def collect_avg_and_plot(df, name, metric, marker, color, label, ax, linestyle='none'):
  df = df[df['name'] == name].groupby(['size'])[metric].mean().reset_index()
  plot(df, metric, marker, color, label, ax, linestyle)

def collect_thread_avg_and_plot(df, name, metric, threads, marker, color, label, ax, linestyle='none'):
  df = df.loc[(df['name'] == name) & (df['threads'] == threads)].groupby(['size'])[metric].mean().reset_index()
  plot(df, metric, marker, color, label, ax, linestyle)

def plot(df, metric, marker, color, label, ax, linestyle='none'):
  ax.plot('size', metric, data=df, marker=marker, color=color, linestyle=linestyle, label=label, markersize=3.5)


path = sys.argv[1] + "/" if len(sys.argv) > 1 else "results/"

df = pd.read_csv(path + "times.csv")
df['sym_bandwidth'] = (df['size']**2)*4/1e9/df['sym_time']
df['transp_bandwidth'] = (df['size']**2)*2*4/1e9/df['transp_time']

# Draw data for simple transpose
fig1, ax1 = initialize_plot("Simple matrix transpose", "Matrix size", "Bandwidth [GB/s]")
collect_avg_and_plot(df, 'sequential', 'transp_bandwidth', 'x', 'red', '-O1', ax1)
collect_avg_and_plot(df, 'unrolled', 'transp_bandwidth', 'o', 'green', 'unrolled', ax1)
collect_avg_and_plot(df, "vectorized", 'transp_bandwidth', '*', 'blue', 'vectorized', ax1)
collect_avg_and_plot(df, "O3", 'transp_bandwidth', '^', 'purple', '-O3', ax1)
ax1.legend(loc='lower left', frameon=True, framealpha=0.8)
fig1.savefig(path + "plots/transpose_simple.pdf")

# Draw data for symmetry check
fig4, ax4 = initialize_plot("Matrix symmetry check", "Matrix size", "Bandwidth [GB/s]")
collect_avg_and_plot(df, 'sequential', 'sym_bandwidth', 'x', 'red', '-O1', ax4)
collect_avg_and_plot(df, 'unrolled', 'sym_bandwidth', 'o', 'green', 'unrolled', ax4)
collect_avg_and_plot(df, "vectorized", 'sym_bandwidth', '*', 'blue', 'vectorized', ax4)
collect_avg_and_plot(df, 'O3', 'sym_bandwidth', '^', 'purple', '-O3', ax4)
ax4.legend(loc='lower left', frameon=True, framealpha=0.8)
fig4.savefig(path + "plots/sym_check.pdf")

# Draw data for cache optimized transpose
fig2, ax2 = initialize_plot("Cache optimized matrix transpose", "Matrix size", "Bandwidth [GB/s]")
collect_max_avg_and_plot(df, ["sequential", "unrolled", "vectorized", "O3"], 'transp_bandwidth', 'x', 'red', 'best non.cache optimized', ax2)
collect_avg_and_plot(df, 'cache_unroll', 'transp_bandwidth', 'o', 'green', 'cache opt. unrolled', ax2)
collect_avg_and_plot(df, 'cache_vect', 'transp_bandwidth', '*', 'blue', 'cache opt. vectorized', ax2)
collect_avg_and_plot(df, 'cache_O3', 'transp_bandwidth', '^', 'purple', 'cache opt. -O3', ax2)
ax2.legend(loc='best', frameon=True, framealpha=0.8)
fig2.savefig(path + "plots/transpose_cache.pdf")

# Draw data for OpenMP transpose
fig3, ax3 = initialize_plot("OpenMP matrix transpose", "Matrix size", "Bandwidth [GB/s]")
collect_thread_avg_and_plot(df, 'omp_O3', 'transp_bandwidth', 4, 'x', 'red', '4 threads', ax3)
collect_thread_avg_and_plot(df, 'omp_O3', 'transp_bandwidth', 8, 'o', 'green', '8 threads', ax3, linestyle='solid')
collect_thread_avg_and_plot(df, 'omp_O3', 'transp_bandwidth', 16, '*', 'blue', '16 threads', ax3, linestyle='solid')
collect_thread_avg_and_plot(df, 'omp_O3', 'transp_bandwidth', 32, '^', 'purple', '32 threads', ax3, linestyle='solid')
collect_thread_avg_and_plot(df, 'omp_O3', 'transp_bandwidth', 64, 's', 'orange', '64 threads', ax3, linestyle='solid')
collect_thread_avg_and_plot(df, 'omp_O3', 'transp_bandwidth', 96, 'd', 'black', '96 threads', ax3, linestyle='solid')
ax3.legend(loc='best', frameon=True, framealpha=0.8)
fig3.savefig(path + "plots/transpose_omp.pdf")