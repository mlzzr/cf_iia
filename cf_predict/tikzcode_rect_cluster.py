import random as r
import csv

r.seed(2)

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
## Header
print("\\documentclass{article}")
print("\\title{cf_predict rect urns 12}")
print("\\usepackage{tikz}")
print("\\usepackage[margin=0.5in]{geometry}")
print("\\usetikzlibrary{external}")
print("\\tikzexternalize[prefix=rect_12/]")
print("\\begin{document}")
print('')
## This is for png
print('\\tikzset{')
print('    png export/.style={')
print(' external/system call=')
print(' {xelatex \\tikzexternalcheckshellescape -halt-on-error -interaction=batchmode -jobname "\\image" "\\texsource";')
print('  convert -density 300 white "\\image.pdf" "\\image.png"; rm -f "\\image.pdf"},')
print('}')
print('}')
print('\\tikzset{')
print('/pgf/images/external info,')
print('use png/.style={png export,png import},')
print('png import/.code={')
print(' \\tikzset{')
print('   /pgf/images/include external/.code={')
print('\\includegraphics')
print('                [width=15cm]')
print('         {{##1}.png}')
print('     }')
print(' }')
print('}')
print('}')

gridx = ['5', '15', '25', '35', '35', '35', '25', '25', '15', '15', '5', '5']
gridy = ['5', '5', '5', '5', '15', '25', '25', '15', '15', '25', '25', '15']
color_list = ['blue', 'green', 'black', 'red', 'yellow']
for item in questions:
    box1 = []
    box2 = []
    for color in color_list:
        box1 += [color] * item[color + '1']
        box2 += [color] * item[color + '2']
    start1 = r.randrange(item['size1'])
    start2 = r.randrange(item['size2'])
    print('\\tikzset{use png}')
    print("\\tikzsetnextfilename{"+"urn{}".format(item['id'])+"}")
    print('\\begin{tikzpicture}[scale=1.5]')
    print('\\begin{scope}[shift={(-3cm,0)}]')
    print('\\draw[black,line width=1mm, fill=black!20!] (0cm,0cm) rectangle (4cm,4cm);')
    for i in range(0, item['size1']):
        print('\\draw[black!20!{}, fill={}]  ({}mm,{}mm) circle (4mm);'.format(box1[i], box1[i], gridx[(i + start1) % item['size1']], gridy[(i + start1) % item['size1']]))
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
        print('\\draw[black!20!{}, fill={}]  ({}mm,{}mm) circle (4mm);'.format(box2[i], box2[i], gridx[(i + start2) % item['size2']], gridy[(i + start2) % item['size2']]))
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
