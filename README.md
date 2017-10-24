# Blink - Traffic Control Model

## Overview
Blink is a traffic model.

## Instructions

## Python3 Virtualenv Setup

#### Requirements
* Python 3
* Pip 3

```bash
$ brew install python3
```

#### Installation
To install virtualenv via pip run:
```bash
$ pip3 install virtualenv
```

#### Usage
Creation of virtualenv:
```bash
$ virtualenv -p python3 <desired-path>
```

Activate the virtualenv:
```bash
$ source <desired-path>/bin/activate
```

Deactivate the virtualenv:
```bash
$ deactivate
```

#### Maintanence
Install required libraries
```bash
$ pip3 install -r requirements.txt
```

Install new libraries
```bash
$ pip3 install <library-name>
```

Update requirements
```bash
$ pip3 freeze > requirements.txt
```