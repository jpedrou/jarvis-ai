# Jarvis AI

<img src="https://miro.medium.com/v2/resize:fit:3840/1*1YUR0pyV-WSKH9KrsCstCA.jpeg"/>

An AI assistant inspired by Iron Man’s JARVIS, equipped with facial recognition capabilities and powered by Google and Microsoft LLM APIs.

## Technologies

<div style="display: flex; gap: 10px; align-items: center;">
    <img src="https://img.icons8.com/?size=100&id=17949&format=png&color=000000" width="75"/>
    <img src="https://img.icons8.com/?size=100&id=22989&format=png&color=000000" width="75"/>
    <img src="https://img.icons8.com/?size=100&id=13441&format=png&color=000000" width="75"/>
    <img src="https://img.icons8.com/?size=100&id=laVIsJnTtYoj&format=png&color=000000" width="75"/>
    <img src="https://img.icons8.com/?size=100&id=20909&format=png&color=000000" width="75"/>
    <img src="https://img.icons8.com/?size=100&id=21278&format=png&color=000000" width="75"/>
</div>

## Running

With Python already installed in your computer, go to the project root and, in the terminal run:

**Linux**

```bash
python3 -m venv venv
```

To activate the env, run:


```bash
source venv/bin/activate
```


**Windows**

```bash
python3 -m venv venv
```

To activate the env, run:

`cmd`

```bash
.\venv\Scripts\activate.bat
```

`PowerShell`

```bash
.\venv\Scripts\activate.ps1
```

To install all python dependencies of this project, with the virtual env already configured, run in the terminal:

```bash
pip install -r requirements.txt
```

To check if the libs were installed correctly, run in the terminal:

```bash
pip list
```

Then, you can run the file `run.py`.

**⚠️ ATTENTION**

This project relies on some libraries that require native system dependencies. As a result, you may encounter errors when running the project until these dependencies are installed.

For Ubuntu (Debian) 24.04, some native dependencies are required.
For other systems, you may need to identify and install equivalent packages manually.
