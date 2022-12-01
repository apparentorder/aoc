This year it's back to python.

This uses a small AOC tools collection -- see [here](shs-tools/setup.py)
for author and license information.

Setup, roughly:
```
python3 -m venv ~/pyenv/aoc
source ~/pyenv/aoc/bin/activate
pip install -e shs-tools
pip install -r shs-tools/requirements.txt 
./main.py --help
```

Then create a `.session` file with your adventofcode.com session cookie for
downloading input and submitting results. Both are triggered when
`AOCDay.inputs[*].0` is `None`.

Copy `.day.py.skel` to `dayXX.py` as necessary. The `return ""` in the
skeleton file has special meaning: it suppresses result submission.

Use `./loop` to watch for and run on file changes; arguments are passed
to `main.py`.

