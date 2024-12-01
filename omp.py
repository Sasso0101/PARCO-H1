from math import log, log2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sys
import numpy as np
from pyparsing import line
import scienceplots

plt.style.use(['science','ieee','no-latex'])
plt.rcParams.update({'font.size': 7})

# Inches don't make sense for me, so I use cm
cm = 1/2.54

def initialize_plot(xlabel, ylabel, logy=False):
  fig, ax = plt.subplots()
  ax.set_title("")
  fig.set_figheight(4*cm)
  fig.set_figwidth(4*cm)
  ax.set_xlabel(xlabel)
  ax.set_xscale("log", base=2)
  if logy:
    ax.set_yscale("log", base=2)
    ax.set_yticks([1, 2, 4, 8, 16, 32, 64])
  ax.set_ylabel(ylabel)
  ax.set_xticks([1, 2, 4, 8, 16, 32, 64])
  ax.grid(True, which="both", ls="-")
  ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
  ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
  return (fig, ax)

def collect_speedup_and_plot(df, name, metric, base, marker, color, label, ax):
  df = df[(df['name'] == name)].groupby(['threads'])[metric].mean().reset_index()
  df['speedup'] = base/df[metric]
  ax.plot('threads', 'speedup', data=df, marker=marker, color=color, linestyle='-', label=label, markersize=3.5, linewidth=0.5)

def collect_avg_and_plot(df, name, metric, marker, color, label, ax, linestyle='none'):
  df = df[df['name'] == name].groupby(['threads'])[metric].mean().reset_index()
  ax.plot('threads', metric, data=df, marker=marker, color=color, linestyle=linestyle, label=label, markersize=2.5, linewidth=0.5)

path = sys.argv[1] + "/" if len(sys.argv) > 1 else "results/"

df = pd.read_csv(path + "times.csv")

# Plot strong scaling speedup
fig3, ax3 = initialize_plot("Threads", "Speedup", logy=True)
xs = np.linspace(1, 64, 64)
ys = xs
ax3.plot(xs, ys, linestyle='--', color='red', label='Ideal speedup', linewidth=0.5)
# base = df.loc[(df['name'] == 'peak') & (df['threads'] == 1)].groupby(['size'])['transp_time'].mean().reset_index()['transp_time'].iloc[0]
# collect_speedup_and_plot(df, 'peak', 'transp_time', base, 'x', 'green', 'Peak speedup', ax3)
base = df.loc[(df['name'] == 'strong_scaling') & (df['threads'] == 1)].groupby(['size'])['transp_time'].mean().reset_index()['transp_time'].iloc[0]
collect_speedup_and_plot(df, 'strong_scaling', 'transp_time', base, 'x', 'blue', 'Real speedup', ax3)

ax3.legend(loc='upper left', frameon=True, framealpha=0.8)
fig3.savefig(path + "plots/strong_scaling.pdf")

# Plot weak scaling efficiency
fig3, ax3 = initialize_plot("Threads", "Efficiency")
xs = np.linspace(1, 64, 64)
ys = np.ones(64)
ax3.plot(xs, ys, linestyle='--', color='red', label='Ideal efficiency', linewidth=0.5)
# base = df.loc[(df['name'] == 'peak_weak') & (df['threads'] == 1)].groupby(['size'])['transp_time'].mean().reset_index()['transp_time'].iloc[0]
# collect_speedup_and_plot(df, 'peak_weak', 'transp_time', base, 'x', 'green', 'Peak efficiency', ax3)
base = df.loc[(df['name'] == 'weak_scaling') & (df['threads'] == 1)].groupby(['size'])['transp_time'].mean().reset_index()['transp_time'].iloc[0]
collect_speedup_and_plot(df, 'weak_scaling', 'transp_time', base, 'x', 'blue', 'Real efficiency', ax3)

ax3.legend(loc='upper right', frameon=True, framealpha=0.8)
fig3.savefig(path + "plots/weak_scaling.pdf")

# Plot bandwidth
df['transp_bandwidth'] = (df['size']**2)*4/1e9/df['transp_time']
fig1, ax1 = initialize_plot("Threads", "Bandwidth [GB/s]")
fig1.set_figwidth(6*cm)
collect_avg_and_plot(df, 'peak', 'transp_bandwidth', 'x', 'green', 'Peak bandwidth', ax1, linestyle='-')
collect_avg_and_plot(df, 'strong_scaling', 'transp_bandwidth', 'x', 'blue', 'Real bandwidth', ax1, linestyle='-')
ax1.legend(loc='upper left', frameon=True, framealpha=0.8)
fig1.savefig(path + "plots/omp_bandwidth.pdf")