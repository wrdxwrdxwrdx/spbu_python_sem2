# spbu_python_sem2


**practices and homeworks of second semester spbu**

All tasks:
* Action Sotrage
* Registry
* Thread sort
* Async chat
* Multiplayer MVVM TicTacToe 
* Bashorg parser 

---

## Requirements

- requests~=2.31.0
- beautifulsoup4~=4.12.3
- numpy~=1.26.4
- ijson~=3.2.3
- simplejson~=3.19.2
- matplotlib~=3.8.4
- loguru~=0.7.2
## Installation

Clone the repository:

```bash
git clone https://github.com/wrdxwrdxwrdx/spbu_python_sem2.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```


## Run TicTacToe

run Server

```bash
python3 -m src.homeworks.TicTacToe.server
```

run App


```bash
python3 -m src.homeworks.TicTacToe.app.app
```

Now you can Choose game mode:
* SinglePlayer (for game with friend on one pc)
* Bot:
    * Random
    * Smart
* Multiplayer

If you choose **Multiplayer**:

- **HOST** Need to choose name, password for a room and his side (X or O) and click "Create"
- **GUEST** Need to enter this name, password and click "Connect"

## Development

Install requirements

```bash
pip install -r requirements.dev.txt
```


