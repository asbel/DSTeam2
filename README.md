# Distributed Systems Team 2
By Asbel and Katelyn 

# Premise

Automated trading systems are taking over the industry (and in a way, the world, too!). Every single day, computer applications and platforms trade various instruments/asset classes across the market such as commodities, equities, options, futures, and many more. The modern-day trader is equipped with so much more than the old school trader -- we now have advanced algorithms that have been designed by PhD quants and some of the smartest developers in the world. How on earth can the average Joe compete against those with such complex systems? It’s getting so out of hand. So, let’s explore some of these things that make today’s traders so advanced. We will be delving into low-latency trading, parallel computing, and concurrent systems that are making trading processes so robust. We will be utilizing concepts we've reviewed in the course including low latency and parallel computing/HPC. 

One application we are currently using is Stampede 2 in the XSEDE supercomputer portal, using SSH (PuTTy, linux). We will also be using C++ and Python to code our scripts. In addition, we will be running Python scripts from an exchange and improving latency. 
  
# Research

Distributed Systems in Trading: 
https://medium.com/coinmonks/why-a-distributed-system-for-the-trading-industry-instead-of-a-centralised-one-8c21236ae899 

Low-Latency and DS in financial applications: 
https://queue.acm.org/detail.cfm?id=2770868 

Stampede 2 documentation:
https://portal.xsede.org/web/xup/single-sign-on-hub

# Binance directions: Data Folder
binance_api.py
Basic functions to get historical (kline) and real-time market information on Binance.

binance_kline_info.py
Pull data from Binance and save kline data to csv files.
