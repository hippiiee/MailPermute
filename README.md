# MailPermute
<p align="center">
  Find valid email from a name with permutations
  <br>
      <img alt="img last release" src="https://img.shields.io/github/v/release/hippiiee/MailPermute.svg?color=blue">
  <a href="https://twitter.com/intent/follow?screen_name=hiippiiie" title="Follow"><img src="https://img.shields.io/twitter/follow/hiippiiie?label=hiippiiie&style=social"></a>
  <br>
</p>

## Features
Find valid email from different providers:
  - [x] DuckDuckGo
  - [x] Gmail
  - [x] Posteo
  - [x] Yahoo
  - [x] Yandex

## Requirements

```bash
pip3 install -r requirements.txt
```

## Usage

```
$ python3 mailpermute.py -h

888b     d888          d8b 888                                                  888            
8888b   d8888          Y8P 888                                                  888            
88888b.d88888              888                                                  888            
888Y88888P888  8888b.  888 888 88888b.   .d88b.  888d888 88888b.d88b.  888  888 888888 .d88b.  
888 Y888P 888     "88b 888 888 888 "88b d8P  Y8b 888P"   888 "888 "88b 888  888 888   d8P  Y8b 
888  Y8P  888 .d888888 888 888 888  888 88888888 888     888  888  888 888  888 888   88888888 
888   "   888 888  888 888 888 888 d88P Y8b.     888     888  888  888 Y88b 888 Y88b. Y8b.     
888       888 "Y888888 888 888 88888P"   "Y8888  888     888  888  888  "Y88888  "Y888 "Y8888  
                               888 v1.1                                                       
                               888                                                             
                               888                                                             
By Hippie | https://twitter.com/hiippiiie

usage: mailpermute.py [-h] [-n NAME]
                      [-c CHECKERS]

options:
  -h, --help            show this help message
                        and exit
  -n NAME, --name NAME  Name of the person (e.g.
                        "John Doe") (default:
                        None)
  -c CHECKERS, --checkers CHECKERS
                        Checkers to use (e.g.
                        "gmail, yandex")
                        (default: all)
```

## Example output

```
$ ./mailpermute.py -n "Hippolyte Quere"

[+] querehippolyte@gmail.com
[+] hippolytequere@gmail.com
[+] hquere@yahoo.com
[+] hquere@gmail.com
[+] quereh@yahoo.com
[+] quereh@gmail.com
[+] qhippolyte@gmail.com
[+] hippolyteq@gmail.com

```

## How does it works ?

Mailpermute first creates different permutations from the name provided by the user. It creates permutations adding '-' '_' (note that mailpermute does not add '+' or '.' which can be added to any valid mail not changing the mail itself). Then Mailpermute is sending request to different providers to verify if the mail exist.

Feel free to contribute if you want to add more checkers to the tool !

*Project inspired from [Mailcat](https://github.com/sharsil/mailcat)*
