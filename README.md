# jupyter-pyquil
PyQuil environment preloaded in a Jupiter Notebook

Carrascal, G., del Barrio, A.A. & Botella, G. First experiences of teaching quantum computing. J Supercomput (2020). https://doi.org/10.1007/s11227-020-03376-x

`docker run -d -p 8888:8888 --name pyquil ginescarrascal/jupyter-pyquil`

Find token in the logs.

To run without security on port 8892:
`docker run -d -p 8892:8888 --name pyquil ginescarrascal/jupyter-pyquil /src/pyquil/entrypoint.sh --no-browser --NotebookApp.token='' --NotebookApp.password=''`
