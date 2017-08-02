import numpy
import random as r
import csv

numpy.random.seed(2)

with open('questions_12.csv') as f:
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
print("\\title{cf_predict rect messy urns 12}")
print("\\usepackage{tikz}")
print("\\usepackage[margin=0.5in]{geometry}")
print("\\usetikzlibrary{external}")
print("\\tikzexternalize[prefix=rect_messy_12/]")
print("\\begin{document}")
print('')
color_list = ['blue', 'green', 'black', 'red', 'yellow']
for item in questions:
    box1 = []
    box2 = []
    for color in color_list:
        box1 += [color] * item[color + '1']
        box2 += [color] * item[color + '2']
    box1 = numpy.random.permutation(box1)
    box2 = numpy.random.permutation(box2)
    print("\\tikzsetnextfilename{"+"urn{}".format(item['id'])+"}")
    print('\\begin{tikzpicture}[scale=1.5]')
    print('\\begin{scope}[shift={(-3cm,0)}]')
    print('\\draw[black,line width=1mm, fill=black!20!] (0cm,0cm) rectangle (4cm,4cm);')
    for i in range(0, item['size1']):
        print('\\draw[black!20!{}, fill={}]  ({}mm,{}mm) circle (4mm);'.format(box1[i], box1[i], i // 4 % 2 * 40 + (-1) ** (i // 4) * (5 + i % 4 * 10), 5 + i // 4 * 10))
    print('\\node at (2cm,4.5cm) {\LARGE Box A (Chance: 50\%)};')
    print('\\node[align=center, below] at (2cm,-0.5cm) {')
    for color in color_list:
        if item[color] == 1:
            print('\\Large {} balls: {}\\\\'.format(color, item[color + '1']))
    print('};')
    print('\\end{scope}')

    print('\\begin{scope}[shift={(3cm,0)}]')
    print('\\draw[black,line width=1mm, fill=black!20!] (0cm,0cm) rectangle (4cm,4cm);')
    for i in range(0, item['size2']):
        print('\\draw[black!20!{}, fill={}]  ({}mm,{}mm) circle (4mm);'.format(box2[i], box2[i], i // 4 % 2 * 40 + (-1) ** (i // 4) * (5 + i % 4 * 10), 5 + i // 4 * 10))
    print('\\node at (2cm,4.5cm) {\LARGE Box B (Chance: 50\%)};')
    print('\\node[align=center, below] at (2cm,-0.5cm) {')
    for color in color_list:
        if item[color] == 1:
            print('\\Large {} balls: {}\\\\'.format(color, item[color + '2']))
    print('};')
    print('\\end{scope}')
    print('\\end{tikzpicture}')
    print('')
print("\\end{document}")
