rm *.aux
#pdflatex _DaBa.tex
#biber _DaBa.bcf
#bibtex _DaBa.tex
#pdflatex _DaBa.tex
#pdflatex _DaBa.tex

pdflatex _DaBa_Teil2.tex
biber _DaBa_Teil2.bcf
#bibtex _DaBa_Teil2.tex
pdflatex _DaBa_Teil2.tex
pdflatex _DaBa_Teil2.tex
