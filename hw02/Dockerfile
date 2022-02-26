# Default python image

FROM python

# Explicitly set working directory

WORKDIR /ast_pdf

# Update

RUN apt-get update

# Install latex builder

RUN apt install -y texlive

# Update & install python modules

RUN apt install graphviz -y
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install networkx
RUN python3 -m pip install matplotlib
RUN python3 -m pip install pydot
RUN python3 -m pip install graphviz
RUN python3 -m pip install -i https://test.pypi.org/simple/ beautiful-ast==0.0.1

# Copy pdf generation sources

COPY main.py main.py
COPY latex.py latex.py
COPY utils.py utils.py
COPY defaults defaults

# Generate ast.pdf

RUN ./main.py ast ast.tex
RUN pdflatex ast.tex
