PyConCanada2015
##################


My scrapers + data + analysis for PyConCanada2015 Keynote

(sorry github)




## Frequency of libraries in `requirements.txt` files in Github Python repositories


This was done by scraping 10k+ Python repositories on Github that contain a `requirements.txt` file. This file is commonly used to store dependencies of the repository. 

![freq_libs](http://i.imgur.com/Kft8vUl.png)

It's clear that the majority of repositories on Python are web development related, or web developers are most likely to include a proper requirements.txt file in their repositories. 


## Network force-layout of libraries in `requirements.txt` files in Github Python repositories

This is biased, as some libaries have their own requirements. For example, Pandas depends on Numpy, so it would be less common to have both Pandas and Numpy in a requirements.txt file. 

![network_graph](http://i.imgur.com/XzjKuzs.png)