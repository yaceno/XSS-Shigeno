# XSShigeno

## Presentation
A tool for detecting a potential XSS on a page. It's just the beginning of it, I'm planning to add more and more features.
For the moment, it allows to detect input texts and run a lot of xss payloads in it until a dialog box appears.

## Usage
- `pip3 install -r requirements.txt`
- Launch the tool with the site you want, example : `python3 xsshigeno.py -s https://xss-game.appspot.com/level1/frame`
- To run the tool showing the actions on the browser (non-headless mode) add `-b` option