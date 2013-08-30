#!/usr/bin/env python
import sys
import matplotlib
if len(sys.argv) > 1 and sys.argv[1].endswith('.svg'):
    matplotlib.use('SVG')
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np
import math
from mpltools import style
from mpltools import layout
style.use('ggplot')


font = FontProperties()
font.set_size('medium')
font.set_weight('semibold')

distributions = {'ALL': []}
with open('data/citation_distribution') as input_file:
    for line in input_file:
        line = line.lstrip()

        # skip blank lines or lines with no dataset id
        if not line: continue
        if not line.split('\t')[1].strip(): continue

        chunks = line.split('\t')[0].split()
        n, repo = chunks[0], ' '.join(chunks[1:])
        if not repo in distributions:
            distributions[repo] = []
        distributions[repo].append(int(n))
        distributions['ALL'].append(int(n))

num_datasets = {}
with open('data/dataset_counts') as input_file:
    for line in input_file:
        line = line.strip()

        if not line: continue

        chunks = line.split('\t')[0].split()
        n, repo = chunks[0], ' '.join(chunks[1:])

        num_datasets[repo] = int(n)

num_datasets['ALL'] = sum(num_datasets.values())
            
fig = plt.figure(figsize=(12,8))
subs = []

column_order=['Journal Archives', 'ALL']
for n, key in enumerate(sorted(distributions, 
                        key=lambda x:(column_order.index(x) if x in column_order else -1, 
                                      x.upper()))):
    # plot a histogram for each repository
    sub = plt.subplot(3,4,n+1)
    subs.append(sub)
    
    distributions[key].sort(reverse=True)
    data = []
    data = []
    for value in distributions[key]:
        data.append(value)

    zeroes = num_datasets[key] - len(data)
    data += [0] * zeroes
    weights = [100./num_datasets[key] for x in data]
    
    bins = [0] + list(np.logspace(0, 6, num=7, base=2))
    plt.ylim(0,100)
    plt.text(0.5, 0.9, key, fontproperties=font,
             horizontalalignment='center',
             verticalalignment='center',
             transform=sub.transAxes)
    plt.text(0.5, 0.8, 'median=%s' % int(np.median(data)),
             horizontalalignment='center',
             verticalalignment='center',
             transform=sub.transAxes)
    plt.text(0.5, 0.7, 'mean=%s' % round(np.mean(data), 1),
             horizontalalignment='center',
             verticalalignment='center',
             transform=sub.transAxes)

    plt.hist(data, bins=bins, weights=weights)
    plt.xscale('symlog', basex=2)
    sub.set_xticks([x*2 if x > 0 else 1 for x in bins])
    sub.set_xticklabels([int(x) for x in bins],rotation=45, rotation_mode="anchor", ha="right")


fig.text(0.5, 0.04, 'citations', ha='center', va='center')
fig.text(0.06, 0.5, '% of datasets', ha='center', va='center', rotation='vertical')

for sub in subs:
    sub.minorticks_off()
    layout.cross_spines(ax=sub)

try:
    figname = sys.argv[1]
    plt.savefig(figname, dpi=200)
except IndexError:
    plt.show()