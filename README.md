AmAlert
==================

An asynchronous Amazon product tracker that sends alerts on slack when the price of product(s) reaches a threshold.

## Dependencies
```
requests_futures
bs4
slackclient
html5lib
```
## Installation
The code was written in python 3.6 , may work for python 3.2+.
In the command prompt/terminal run the following commands
```
git clone https://github.com/vaibhavk97/AmAlert.git
cd AmAlert/
pip install -r requirements.txt
```
## Configuration
Configuration is held in json format in the file `config.json` . 
```
slack-token : the token for your slack workspace.
main-channel : The channel on your workspace where you will receive the main alerts.
error-channel : The channel where errors will be reported if found.
status-channel : The channel where the state of the program will be updated hourly.
fail_delay : The time for pausing in between sending the requests (low value might lead to ip ban).
```
you can get the slack token for your workspace from here : https://goo.gl/duqpz5.


The details for products are also held in json format in the `data.json` file. The fields are as follows
```
checkprime : Whether to check for prime seller or not {true/false}.
alert_price : the threshold price to send alert.
single_alert : Whether to send a single alert or multiple alerts when the condition is met.
```
The key represents the asin of the product which can be found in the product info on the amazon page. A sample product has been added to the file.

## TODO

```
Add proxy support
Add dynamic updation and changes in the data files via slack.
Add price history graphs.
Add support for amazon pantry.
Add support for amazon in other countries than india.
```

