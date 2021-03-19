# all-in-one-code

`_build.py` in this repository will encode and embed the repository into a single Python code which can run in Jupyter Notebook services such as Kaggle and Google Colab.

This repository was developed based on [kaggle-script-template](https://github.com/lopuhin/kaggle-script-template) with the following modifications:

- Support to encode all the necessary files (e.g. `.py`, `.yml`, etc.) in the repository (rather than specifying the directory name).

- Support to show the stdout in the Jupyter output by replacing `os.system` with `!`.

- Simplified by removing `setup.py` and embedding the template to the code to build.

- Clarified by renaming.


## How to use

1. Copy `_build.py` to your (local) repository root directory.

2. Open `_build.py` and modify the last line of `template` (`!python main.py`) if your main code is not `main.py`. 

3. Run:

    ```bash 
    python _build.py
    ```

3. Copy the content of `_one_code.py` generated in the current directory to your Jupyter Notebook cell and run it.
