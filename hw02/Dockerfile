FROM conda/c3i-linux-64
COPY main.py main.py
COPY latex.py latex.py
COPY utils.py utils.py
RUN conda update --all
RUN conda install -c anaconda networkx
RUN conda install -c conda-forge matplotlib
RUN conda install -c anaconda pydot
RUN conda install -c conda-forge pygraphviz
RUN conda install -c glebmarin beautiful_ast
RUN ./main.py ast ast.tex
RUN apt-get update
RUN apt-get install -y texlive
RUN pdflatex ast.tex
RUN rm ast.aux ast.log
