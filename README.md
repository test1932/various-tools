To run on Linux:

    make
    . venv/bin/activate
    python -B server.py <filename>.html

To run on Windows (manual version of makefile):

    python -m venv venv
    .\venv\Scripts\activate.ps1
    pip install -r requirements.txt
    python -B server.py <filename>.html