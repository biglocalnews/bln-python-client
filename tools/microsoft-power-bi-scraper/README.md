## Microsoft Power BI Scraper

### Requirements

1. OpenSSL - this is usually already installed on most systems, but if not, can
   easily be installed with a package manager:
```bash
sudo apt install openssl  # debian-based linux systems
sudo yum install openssl  # rpm-based linux systems
sudo apk add openssl      # alpine linux systems (AWS)
sudo pacman -S openssl    # arch linux systems
```
2. [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads):
must already have Google Chrome installed for this to work

### TODO
1. Pull all iframes with src matching https://app.powerbigov.us/view
1. Download and execute embedded javascript
