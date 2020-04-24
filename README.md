# jupyter-pyquil
PyQuil environment preloaded in a Jupiter Notebook


`docker run -d -p 8888:8888 --name pyquil ginescarrascal/jupyter-pyquil`

Find token in the logs.

To run without security on port 8892:
`docker run -d -p 8892:8888 --name pyquil ginescarrascal/jupyter-pyquil /src/pyquil/entrypoint.sh --no-browser --NotebookApp.token='' --NotebookApp.password=''`