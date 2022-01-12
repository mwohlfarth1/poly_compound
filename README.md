# poly_compound
A compound interest calculator which allows the user to draw a polynomial for the interest rate over time.

This calculator was created to calculate the final value of the asset $TIME/MEMO.

## Tools Used
poetry (https://python-poetry.org/) for dependency management

python 3.9.5

## Installation and Running
To use the app, you need to run it in some way. The easiest way to do this is to run it from powershell. Here are the steps for that:

1. Check to see if you have python installed in powershell: execute ```python``` in powershell
2. If you didn't have python, install it through the windows store or some other way
3. If you did have python, check to make sure the version is compatible (this project supports python versions >=3.7.1,<3.11): ```python --version```
4. Now that you have python, get ```poetry``` installed in your powershell. Follow the powershell instructions here: https://python-poetry.org/docs/
5. Clone this repository (or just copy the ```.py```, ```.lock```, and ```.toml``` files to a directory)
6. Run ```poetry install``` wherever your files are. This will use the ```.lock``` and ```.toml``` files to create a virtual environment and install all the dependencies into that virtual environment. That way they don't clutter up your global python instance.
7. To run the program, just ask ```poetry``` to run the ```main.py``` script using ```python```: ```poetry run python main.py```

## Usage
1. Type valid inputs into the input boxes. All boxes have default values, so you can just stick with defaults if you want
2. Click and drag to draw points (in red). The program will fit a polynomial (drawn in black) to these points. It will then use the polynomial to determine rebase rates for each epoch and apply them to the initial principle. You'll see the final principle and final value on the left.
3. To copy the polynomial to your clipboard: ctrl-c
4. To clear all the points you've drawn so far: ctrl-z (beware, this has bugs)

## Demo
<img src="https://github.com/mwohlfarth1/poly_compound/blob/main/poly_compound_v0.1_demo.gif" width="90%" height="50%"/> 
