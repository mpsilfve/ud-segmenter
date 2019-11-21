## What is it?
It's a UD segmenter.  
More on UD [here](https://universaldependencies.org/).


## How to use it?
### PyPy
It is highly recommended to use [PyPy](https://www.pypy.org/) istead of standard CPython interpreter.  
To install al necessary third-party libraries for PyPy, run the following commands:
```
wget https://bootstrap.pypa.io/get-pip.py
pypy3 get-pip.py --user
pypy3 -m pip install distance --user
pypy3 -m pip install tqdm --user
```
### Data
The segmenter accepts data in lemma-tag format. Example input:
```
avata number=singv person=3 avaa
hauska case=par number=plur hauskoja
erikoinen case=par number=plur erikoisia
...
```
Example output:
```
avaa/avata >/person=3,number=singv
hausko/hauska j/number=plur a>/case=par
erikois/erikoinen i/number=plur a>/case=par
...
```

### Script
Example usage:
```
pypy3 ud_segmenter.py --train data/fitrain+test --test data/fitest -n 1000 -o fi_segmented
```
#### Arguments
* `--train` — train dataset file in lemma-tags form.
* `--test` — test dataset file in lemma-tags form.
* `-n` or `--number_of_passes` — number of passes for the model.
* `-o` or `--output` — output file for the result of the segmentation.

### Module
Instead of running the program as a script you could use it as a module.  
```python
import ud_segmenter
segmented = ud_segmenter.run(train_data, test_data, N=1000)
```
