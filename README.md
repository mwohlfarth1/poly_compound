# poly_compound
A compound interest calculator which allows the user to draw a polynomial for the interest rate over time.

## Tools Used
poetry (https://python-poetry.org/) for dependency management

python 3.9.5

## Usage
To use the app, run it in some way. The easiest way to do this is to run it from powershell. Here are the steps for that:

1. Check to see if you have python installed in powershell: execute ```python``` in powershell
2. If you didn't have python, install it through the windows store or some other way
3. If you did have python, check to make sure the version is compatible (this project supports python versions >=3.7.1,<3.11): ```python --version```
4. Now that you have python, get ```poetry``` installed in your powershell. I assume the poetry docs are sufficient for instructions
5. Clone this repo (or just copy the ```.py```, ```.lock```, and ```.toml``` files to a directory)
6. Run ```poetry install```. This will create a virtual environment and install all the dependencies into that virtual environment. That way they don't clutter up your global python instance.
7. To run the program, just ask ```poetry``` to run the ```main.py``` script using ```python```: ```poetry run python main.py```