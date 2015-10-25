PyConCanada2015
##################


My scrapers + data + analysis for PyConCanada2015 Keynote

(sorry github)




## Frequency of libraries in `requirements.txt` files in Github Python repositories


This was done by scraping 10k+ Python repositories on Github that contain a `requirements.txt` file. This file is commonly used to store dependencies of the repository. 

![freq_libs](http://i.imgur.com/Kft8vUl.png)

It's clear that the majority of repositories on Python are web development related, or web developers are most likely to include a proper requirements.txt file in their repositories. 


## Relationships between libraries

Using the data in `requirements.txt' files, we can find common co-occurences of libraries. For example, it's not hard to imagine that whenever django is a requirement, so is psycopg2. In fact, in the dataset I had, 41% of all django apps also included psycopg2. These relationships can be mined using a simple algorithm called the apriori algorithm. It's history goes back to large department stores that were interested in what products were commonly bought together. The naive solution, compare all possible pairs, results in a quadratic algorithm: in if you have thousands of products, this becomes inefficient quickly. The apriori algorithm intelligently cuts through this massive space. 

Here are the other common libraries paired with django:

|starting_with | ending_with      |  starting_with_occurrences |confidence     | occurrences |ending_with_occurrences |
|------------|-----------------|-------------------------|---------------|-------------|-----------------------|
|django      | requests        |  2714                   |0.243920412675 | 662         |2463                   |
|django      | wheel           |  2714                   |0.22402358143  | 608         |1649                   |
|django      | six             |  2714                   |0.245394252027 | 666         |1985                   |
|django      | psycopg2        |  2714                   |0.411569638909 | 1117        |1573                   |
|django      | gunicorn        |  2714                   |0.320191599116 | 869         |1531                   |
|django      | dj-database-url |  2714                   |0.263448784083 | 715         |728                    |


[Here are the results for other libraries](https://github.com/CamDavidsonPilon/PyconCanada2015/blob/master/analysis/library_association_rules.csv)
 including some metrics to sort on. To read more about these metrics, see [this link](http://michael.hahsler.net/research/association_rules/measures.html).

## Now, let's recommend libaries based on these relationships

So, if we know a user installed django, we can perhaps recommend that they also install psycopg2 (according to above, we would be right 41% of the time). We can turn these co-occurences into a very simple recommendation algorithm for Python Libaries! So I've gone ahead and done that. 

### `pipp`: one of the `p`s stands for personalized!

Yes, that's right - we can bring you library recommendations right to the command line. Try it out!

`pip install pipp`

```
$ pipp install jsmin
Requirement already satisfied (use --upgrade to upgrade): jsmin in /Users/camerondavidson-pilon/.virtualenvs/data/lib/python2.7/site-packages
pipp: Other users who installed jsmin also installed cssmin
```

Command line too nerdy for you? How about recommendations on PyPI?

![pypi](http://i.imgur.com/BCyumQV.png)

## Network force-layout of libraries in `requirements.txt` files in Github Python repositories

This is biased, as some libaries have their own requirements. For example, Pandas depends on Numpy, so it would be less common to have both Pandas and Numpy in a requirements.txt file. 

![network_graph](http://i.imgur.com/XzjKuzs.png)



## Most controversial Python StackOverflow answer

StackOverflow has become the most popular forum for developers to ask, answer and importantly *promote* or *demote* content. StackOverflow does something even more incredible: they expose all their interaction data (questions, answers, views, votes) through a [public query interface](http://data.stackexchange.com/). Using this, we can compute, what is the most controversial Python answer?


To do this, we will use the following algorithm: find the answer that has an upvote/downvote ratio close to 0.5, and also has lots of votes. The former requirement is a good definition of "controversial", and the latter requirement protects use against answers with trivial counts (ex: 1 upvote and 1 downvote). Think of it as a balancing act between "how confident are we that this question is indeed the most controversial?" The following query accomplishes this (based on a similar equation in [this post](http://camdp.com/blogs/how-sort-comments-intelligently-reddit-and-hacker-))

```SQL
declare @VoteStats table (parentid int, id int, U float, D float) 

insert @VoteStats
SELECT 
  a.parentid,
  a.id,
  CAST(SUM(case when (VoteTypeID = 2) then 1. else 0. end) + 1. as float) as U,
  CAST(SUM(case when (VoteTypeID = 3) then 1. else 0. end) + 1. as float) as D
FROM Posts q
JOIN PostTags qt 
  ON qt.postid = q.ID
JOIN Tags T 
  ON T.Id = qt.TagId
JOIN Posts a 
  ON q.id = a.parentid
JOIN Votes 
  ON Votes.PostId = a.Id
WHERE TagName  = 'python'
   and a.PostTypeID = 2 -- these are answers
Group BY a.id, a.parentid

set nocount off

SELECT 
 TOP 100
 parentid,
 id,
 U, D,
 ABS(0.5 - U/(U+D) - 3.5*SQRT(U*D / ((U+D) * (U+D) * (U+D+1)))) + 
   ABS(0.5 - U/(U+D) + 3.5*SQRT(U*D / ((U+D) * (U+D) * (U+D+1)))) as Score
FROM @VoteStats 
ORDER BY Score 
```

Running this produces the following table (as of Oct. 24, 2015):

| parentid | url      | U   | D  | Score             |
|----------|---------|-----|----|-------------------|
| 1641219  | http://stackoverflow.com/questions/1641305 | 100 | 58 | 0.267581687129904 |
| 366980   | http://stackoverflow.com/questions/367082  | 55  | 29 | 0.360985397926758 |
| 904928   | http://stackoverflow.com/questions/904941  | 44  | 40 | 0.379197639329681 |
| 1641219  | http://stackoverflow.com/questions/1945699 | 49  | 23 | 0.382002382488145 |
| 734368   | http://stackoverflow.com/questions/734910  | 48  | 30 | 0.38315203605798  |
| 7479442  | http://stackoverflow.com/questions/7479473 | 46  | 23 | 0.394405318873308 |
| 620367   | http://stackoverflow.com/questions/620397  | 42  | 24 | 0.411383595098925 |
| 969285   | http://stackoverflow.com/questions/969324  | 49  | 20 | 0.420289855072464 |
| 1566266  | http://stackoverflow.com/questions/1566285 | 39  | 24 | 0.424918292799399 |


The closer the score is to 0, the more controversial it is. Take a look at the answers comment's to see debates about why the answer is controversial. 


## 2-Spaces vs 4-Spaces

Let's not argue: let's look at the empirical data. I looked at over 23 thousand Python repos and [computed what the most common](https://github.com/CamDavidsonPilon/PyconCanada2015/blob/master/analysis/indent_analysis.py) indenting practice was in each repo. The results were quite infavor of 4-spaces: **88% of repos used 4-spaces, and only 7% of repos use 2-spaces**. What about the remaining 5%? Well, some repos use 8-spaces, and some used 1-spaces! Examples: https://github.com/aqt01/UnderWaterWorld uses 8-spaces, and https://github.com/sanglech/CSC326 uses 1-space. 

## What is the most popular testing framework?

Passing through the tens of thousands of repos, [I looked for imports](https://github.com/CamDavidsonPilon/PyconCanada2015/blob/master/analysis/test_frameworks.py) of the most popular testing libaries: pytest, unittest, nose and testify. Here where the results:

| package  | count | percent of total |
|----------|-------|------------------|
| None     | 22162 |       86%        |
| unittest |  3032 |       12%        |
| nose     |   379 |      1.5%        |
| pytest   |   293 |        1%        |
| testify  |     4 |       ~0%        |


## What about using Python for functional programming?

If you are going to use Python for functional programming, or semi-functional programming, you're probably going to be using libraries like `functools`, 'itertools', 'toolz' and others. How many Python repos use this style of programming? Data shows about 15% of repos do this. 


## How often do we disobey *flat is better than nested*?

```
from com.sun.org.apache.xerces.internal.impl.io import \
            MalformedByteSequenceException
```
(from [here](https://github.com/kurtmckee/listparser/blob/c280d6619241cb6e46ec1f708063f0c05b28933c/listparser/__init__.py#L66-L67))
 
Is this ugly or beautiful? Python says it's ugly - after all, *flat is better than nested*. How often we break this? For this, I looked at the *maximum* import nest in each repo. Here's the breakdown: 


![nest_dist](http://i.imgur.com/9uq8b4M.png)


