rm *.aux

pdflatex merge_all.tex
#biber _DaBa_Teil2.bcf
#bibtex _DaBa_Teil2.tex
pdflatex merge_all.tex
#pdflatex _DaBa_Teil2.tex
