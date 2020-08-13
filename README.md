## bluditcracker.py 1.0.1
Password cracking tool that can be used to recover credentials to Bludit CMS

## Usage

```
usage: bluditcracker.py [-h] -t [url] [-d [dir]] (-u [username] | -U [filename]) (-p [password] | -P [filename]) [-s [time in seconds]] [-v]

Enterprise usernames wordlist generator

optional arguments:
  -h, --help            show this help message and exit
  -s [time in seconds]  sleep time after blocking IP
  -v                    show program's version number and exit

required:
  -t [url]              target, ex.: http://10.10.10.99
  -d [dir]              admin panel dir, default: /admin/login
  -u [username]         username
  -U [filename]         usernames wordlist file
  -p [password]         password
  -P [filename]         passwords wordlist file
```

## Example

```
./bluditcracker.py -t http://10.10.10.99 -U users.txt -P ./passwords.txt
```
