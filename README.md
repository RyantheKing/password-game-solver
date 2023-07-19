# Password Game Solver

## Overview
This is a short proof of concept project to solve [The Password Game](https://neal.fun/password-game/) in as little time as possible with as few failure points as possible.

## Installation
1. Clone the repository
```sh
git clone https://github.com/RyantheKing/password-game-solver.git
```

2. Install the most recent version of [Python](https://www.python.org/downloads/)

3. Install the required packages
```sh
pip install -r requirements.txt
```

4. Install Selenium Driver. (The code is currently setup for Mozilla Firefox's [geckodriver](https://github.com/mozilla/geckodriver/releases) but you can modify the code to use another [selenium driver](https://selenium-python.readthedocs.io/installation.html#drivers))

### Setup Notes
This project was created with python 3.11.4 on a Windows 10 machine running Firefox. You may need to install firefox, update your python version, or modify the code to work with your setup.

## Common Selenium issues
In addition to installing with pip, selenium requires additional setup. \
You will need to download the selenium driver for your browser and operating system. \
This code is currently setup for Firefox. If you install geckodriver without also installing Firefox, selenium will not work! \
MAKE SURE YOUR SELENIUM DRIVER IS IN YOUR PATH!

## Caveats
The bot will occasionally fail in scenarios where a solve is impossible. For example, if the time is 9:59 (digit sum of 23), the bot will most certainly fail because the password length (101) plus the algebraic chess notation digits (between 1 and 8) will sum to more than 25. \
90% of times, however, the bot will succeed, so just wait for a time with a lower digit sum and run it again.

## Credits
Big thanks to not a cat ([GitHub page here](https://github.com/the-non-feline)) for his help with the code and testing of the project \
YouTube video link database, chess answer database, and google maps answer database all by pog5 ([GitHub page here](https://github.com/pog5/)) \
And thanks to [Neal Agarwal](https://nealagarwal.me/) for the game itself. \
Play The Password Game: https://neal.fun/password-game/