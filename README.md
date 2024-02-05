# This is KTV : Know the Video

ever after youtube has removed the Dislike button, it has been very hard for us viewers to judge the authenticity of the video we are consuming.

 So, we have developed this Chrome Extension "KTV" which does precisely that. 

## what is the project

### libraries used

Basically, our project utilizes various libraries, including the following for the backend:

- nltk
- pandas
- NumPy
- transformer
- google API client ( fetching the youtube comments)
- scikitlearn - scipy special

### The model

we perform sentiment analysis using the Cardiff NLP Twitter RoBERTa model.

[https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment?library=true](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment?library=true)

The sentiment analysis results are then presented as percentages of negative, positive, and neutral sentiments.

In Addition to that we also provide "Essential Keywords" extracted from the comments along with a brief review of the YouTube comments.

We use it as a chrome extension so as to provide the best user experience. Time is a valuable resource and our projects aims to reserve this resource of yours.

## The Extension

![Untitled](This%20is%20KTV%20Know%20the%20Video%2005b49c851b714d759100d69738c6ef0d/Untitled.png)

![Untitled](This%20is%20KTV%20Know%20the%20Video%2005b49c851b714d759100d69738c6ef0d/Untitled%201.png)
