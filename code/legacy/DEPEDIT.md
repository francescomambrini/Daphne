# How to use Depedit

Depedit is incredibly useful to make quick edits to conllu files.

## The script `run_depedit.py`

The script `run_depedit.py` in the `scripts/depedit` folder will recursively search to the given folder and look for conllu files. It will apply the scenario described in the INI file and overwrite the original file. It will, however, save a copy of the original file as `filename.conllu.bak` in the same directory as the original file.

The syntax of the script:

```bash
python run_depedit.py <PATH_TO_FILE.ini> <PATH_TO_DIR>
```
If you pass `<path-to-Daphne>/data/annotation/latest` as second argument, it will edit all the files.

## Makefile

In the folder `scripts` there is a `Makefile` that can be used to:
1. mass edit the file; just change the path to the INI config file and to the conllu folder
2. purge the `conllu.bak` files once that everything has been checked

Just use it as

```bash
make edit
make purge
```