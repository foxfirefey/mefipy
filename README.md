Basic set up and running

```
git clone git@github.com:foxfirefey/mefipy.git mefipy
cd mefipy
python3 -m venv env
source env/bin/activate
python3 -m pip install .
```

Example of running with a custom tag set:

```
python3 bin/generate.py "2019-09-04 09:00" "2019-09-05 12:30" 2019-09-05.html --tag twitter tumblr
```

Run the tests:

```
python3 -m unittest
```
