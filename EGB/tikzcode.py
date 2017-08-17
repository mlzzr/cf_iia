import random as r
import csv

with open('questions.csv') as f:
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
print("\\title{EGB charts}")
print("\\usepackage{tikz}")
print("\\usepackage[margin=0.5in]{geometry}")
print("\\usetikzlibrary{external}")
print("\\tikzexternalize[prefix=EGB/]")
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

for item in questions:
    print('\\tikzset{use png}')
    print("\\tikzsetnextfilename{"+"chart{}".format(item['id'])+"}")
    print('\\begin{tikzpicture}[x=25, y=1]')
    print('\\node[align = center, below] at(8.25, -20) {Year};')
    print('\\draw[->, very thick] (0, 0) - - (16.5, 0);')
    print('\\draw[fill = blue]  (16, 55) - - (16, 65) - - (16.5, 65) - - (16.5, 55);')
    print('\\node[align = center] at(8.25, 130) ' + '{' + 'Rate of return: ' + '{}\%'.format(item['rate'] * 100) + '};')
    print('\\node[align = center, right] at (16.5, 60) {Withdrawal (\$)};')
    print('\\node[left] at (0, 0) {Now};')
    print('')

    for t in range(16):
        print('\\draw ({}, -2) -- ({}, 2);'.format(t, t))
        print('\\node[align=center, below] at ({},0) '.format(t + 0.5) + '{' + '{}'.format(t + 1) + '};')
        if item['end'] > 15:
            print('\\node[align=center, right] at (16.5,15) {And continues};')
            print('\\node[align=center, right] at (17,5) {forever...};')
            item['end'] = 15
        if t >= item['start'] and t <= item['end']:
            print('\\draw[fill=blue]  ({},0) -- ({},{}) -- ({},{}) -- ({},0);'.format(t - 0.25, t - 0.25, item['withdraw'], t + 0.25, item['withdraw'], t + 0.25))
            print('\\node[align=center, above] at ({},{})'.format(t, item['withdraw']) + '{' + '\small ' + '{}'.format(item['withdraw']) + '};')
    print('\\end{tikzpicture}')
    print('')
print("\\end{document}")