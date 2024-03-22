# Nato-Dex-BkmkPorter
#### A selenium-based Python script to transfer bookmarked titles on manganato to MangaDex's Follow directory
--- 
### 1. Prerequisites 
- Relevant accounts on [manganato](www.manganato.com) / [manganelo](www.manganelo.com) and [MangaDex](www.mangadex.org) logged in and passwords remembered by the browser you wish to initiate the transfer with.
- Minimum Python 3.12 and dependencies in the requirements.txt file installed.
- Compatible webdrivers for your prefered browser(s) installed in the default location
> [!TIP]
> Get webdrivers here:
> - [Google Chrome](https://chromedriver.chromium.org/downloads)
> - [Mozilla Firefox](https://github.com/mozilla/geckodriver/releases)
> - [Microsoft Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH)
### 2. Basic Command
- The simplest command configuration for first / one time use:
```bash
python bkmk.py run -br <browser> -dir <path/to/the/directory/containing/browser/profile> -p <profile>
```
> [!TIP]
> How to find your browser's profile directory and profiles:
> - Chrome:
>     - Enter `chrome://version/` into the address bar.
>     - Find **Profile path**, it should be something like `C:\Users\USER\AppData\Local\Google\Chrome\User Data\Default`. The path to the User Data folder is your directory, while the last folder is the profile.
> - Edge: Similar to Chrome, but enter `edge://version/` instead.
> - Firefox:
>     - Enter `about:profiles` into the address bar.
>     - In the (usually) first profile listed, the Root (not Local) path to the *Profiles* folder is the directory, while the final folder is the profile.
### 3. Documentation 
#### a. The `run` command
The `run` command initiates the webdriver session using the three arguments `--browser`, `--directory` and `--profile`. For first time use, all three arguments must be provided, which will then be saved into the default profile in `config.json`. 
- Example:
```bash
python bkmk.py -br firefox -dir "C:\Users\USER\AppData\Roaming\Mozilla\Firefox\Profiles" -p "qqgixor9.default-release"
```
If `run` is used with `--browser` plus either or none of the others, the rest will be retrieved from their respective browser-specific profile in `config.json`.
- Example:
```bash
python bkmk.py run -br chrome
```
Otherwise, if `run` is used without any arguments, they will be retrieved from the default profile in `config.json`, provided that the default profile is not missing any information. 
```bash
python bkmk.py run -p "Profile 1"
```
> [!NOTE]
> Arguments, especially those of `--directory` and `--profile`, should be quoted.
#### b. The `set` command 
The `set` command sets the default arguments to be used with `run` . Arguments are the same as `run`.
- Example:
```bash
python bkmk.py set -br firefox -dir "C:\Users\USER\AppData\Roaming\Mozilla\Firefox\Profiles" -p "qqgixor9.default-release"
> [!CAUTION]
> While `--directory` and `--browser` will be checked for validity when used with either `run` or `set`, `--browser` will not. Make sure the browser you set default is compatible with other elements in the default profile.
---
#### Contact:
- Discord: emberfox205
