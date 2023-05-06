# XSShigeno

## Presentation
A tool for detecting a potential XSS on a page. It's just the beginning of it, I'm planning to add more and more features.
For the moment, it allows to detect input texts and run a lot of xss payloads in it until a dialog box appears.

## Usage
- `chmod 755 cmds.sh` (to give yourself the right to install the libraries)
- Install the libraries : `./cmds.sh`
- Launch the tool with the site you want, example : `python3 xsshigeno.py -s https://xss-game.appspot.com/level1/frame`
