A Python environment with all required libraries to generate/solve each challenge.

## Docker environment setup

```
sudo docker build -t 30hours-learn .
sudo docker run -it -v "$(pwd)"/../challenge:/app/challenge 30hours-learn sh
```

## Quick start script to Docker environment

```
sudo ./run.sh
```

## Run a Python script

```
python challenge/<challenge_folder>/<folder>/main.py
```


