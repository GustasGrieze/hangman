# Hangman

Hangman is a popular word guessing game where the player attempts to guess a word or phrase by suggesting letters or numbers. The game is won if the player successfully guesses the word, and is lost if they run out of guesses.

## Installation

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python](https://www.python.org/downloads/) installed on your computer.

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/GustasGrieze/hangman
```

You'll need to have the required extensions.

```bash
# To install them
$ pip install -r requirements.txt
```

Otherwise, you could opt to creating a virtual environment to store the extensions.

```bash
# Install the virtualenv package
$ pip install virtualenv

# Create your virtual environment
$ python -m venv venv

# Activate it
$ source venv/Scripts/activate

# Finally install the extensions
$ pip install -r requirements.txt
```

## How To Use

From here you can run it by typing:

```bash
$ python run.py
```

Go to your browser and enter the URL **localhost:8000**

## Features

- Ability to register and log in
- Change your name and profile picture
- Simple art representation of the hangman figure
- Keeps track of the player's remaining guesses
- Supports words with letters only
- Player stats and game history
