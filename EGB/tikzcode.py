import numpy
import random as r
import csv

with open('questions_trial.csv') as f:
    questions = list(csv.DictReader(f))
for item in questions:
    for key in item:
        try:
            try:
                item[key] = int(item[key])
            except ValueError:
                item[key] = float(item[key])
        except ValueError:
            pass

print("\\documentclass{article}")
print("\\title{cf_update urns 12}")
print("\\usepackage{tikz}")
print("\\usepackage[margin=0.5in]{geometry}")
print("\\usetikzlibrary{external}")
print("\\tikzexternalize[prefix=cf_update/]")
print("\\begin{document}")
print('')
for item in questions:
    box1 = ['blue'] * item['blue1'] + ['orange'] * item['orange1'] + ['green'] * item['green1'] + ['red'] * item['red1'] + ['yellow'] * item['yellow1']
    box2 = ['blue'] * item['blue2'] + ['orange'] * item['orange2'] + ['green'] * item['green2'] + ['red'] * item['red2'] + ['yellow'] * item['yellow2']
    print("\\tikzsetnextfilename{"+"urn{}".format(item['id'])+"}")
    print('\\begin{tikzpicture}')
    print('\\begin{scope}[shift={(-4cm,0)}]')
    print('\\draw[black,line width=5mm] (-3cm,-3cm) rectangle (3cm,3cm);')
    for i in range(0, item['size1']):
        print('\\draw[black!20!{}, fill={}]  ({}:2cm) circle (2mm);'.format(box1[i], box1[i], (item['start1'] + i * 360 / item['size1']) % 360))
    print('\\node at (0cm,4cm) {\LARGE Box A (Chance: 50\%)};')
    print('\\node[align=center, below] at (0cm,-4cm) {')
    for color in ['blue', 'orange', 'green', 'red', 'yellow']:
        if item[color] == 1:
            print('\\Large {} balls: {}\\\\'.format(color, item[color + '1']))
    print('};')
    print('\\end{scope}')

    print('\\begin{scope}[shift={(4cm,0)}]')
    print('\\draw[black,line width=5mm] (-3cm,-3cm) rectangle (3cm,3cm);')
    for i in range(0, item['size2']):
        print('\\draw[black!20!{}, fill={}]  ({}:2cm) circle (2mm);'.format(box2[i], box2[i], (item['start2'] + i * 360 / item['size2']) % 360))
    print('\\node at (0cm,4cm) {\LARGE Box B (Chance: 50\%)};')
    print('\\node[align=center, below] at (0cm,-4cm) {')
    for color in ['blue', 'orange', 'green', 'red', 'yellow']:
        if item[color] == 1:
            print('\\Large {} balls: {}\\\\'.format(color, item[color + '2']))
    print('};')
    print('\\end{scope}')
    print('\\end{tikzpicture}')
    print('')
print("\\end{document}")
