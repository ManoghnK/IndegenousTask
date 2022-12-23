# IndegenousTask
Take any newspaper data through their API and classify the sentiment within the articles. Find the topic of the article and the sentiment. Share the github link to codebase.


The API used for the task is newsapi.org
The free version of the API fails to provide the full article, as a result the sentiment analysis and classification is performed on the limited content available. Considering the above tresholds the results are not entirely precise but the process followed is absolutely correct.

The newspaper considered is the bbc-news and the news is sorted based on the popularity and it can be filtered otherwise in the code. 
The csv file with the results are attached. 

Inorder to run the python file:
1> Navigate to the folder consisting the code in the terminal
2> Since the code involves displaying encoded text, please run the following snippets in the terminal
       -> py -mpip install win-unicode-console
       -> py -mrun news.py

Output:
The csv file consists of 7 columns namely- description, raw article, Article post-processing, Polarity (polarity of the article), Sentiment (sentiment of the entire article based on the polarity), Category (category of the news), Score (similarity-score with respect to category).


      
