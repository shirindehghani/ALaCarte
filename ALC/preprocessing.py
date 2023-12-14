import re
import emoji
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from tqdm import tqdm
import warnings

tqdm.pandas()
warnings.filterwarnings("ignore")


list_stop_words=stopwords.words("english")
def delete_stopwords(text, list_stop_words=list_stop_words):
    text=text.lower()
    removed_stop_words=[word for word in text.split() if not word in list_stop_words]
    return " ".join(removed_stop_words)

######################################   

def convert_emoji(text):
    text2=emoji.demojize(text)
    text3=text2.replace(":", " ")
    return text3

######################################

def replace_repeated_punctuations(text):
    return re.sub(r'([،٪؟\?!*•♪×)(÷»«^,&$;٫@.=\n""؛+|#–…+“”)))(/])\1+', r' \1 <repeat>', text)

######################################

def replace_repeated_characters(tweet):
    # Use regex to remove repeated characters
    list_words=[re.sub(r'([a-zA-Z_])\1+', r'\1', word)+" <elong>" \
                if re.search(r'([a-zA-Z_])\1+', word) else word \
                for word in tweet.split()]
    return " ".join(list_words)

######################################

def remove_punctuations(text):
    return re.sub(f'[،٪؟\?!*•♪×)(🇮🇷#÷»🇮«^,🇫&:🇦;@.=\n""؛+|–…_+“”:)))(/]', '', text)

######################################

def remove_extra_spaces(tweet):
    tweet=tweet.replace('\s+', '')
    tweet=tweet.strip()
    return tweet

######################################

def replace_numbers(tweet):
    cleaned_tweet=re.sub('[1234567890]', " <number>", tweet)
    return cleaned_tweet

######################################

def replace_urls(tweet):
    urls=re.sub(r'(https?://\S+)', " <url>", tweet)
    return urls

######################################

def replace_mentions(tweet):
    mentions=re.sub(r"@([a-zA-Z0-9_]{1,50})", " <user>", tweet)
    return mentions

######################################

def replace_hashtags(tweet):
    hashtags=re.sub(r"#([a-zA-Z0-9_]{1,50})", " <hashtag>", tweet)
    return hashtags

######################################

def replace_uppercase(tweet):
    splited_tweet=tweet.split()
    splited_tweet2=[word+" <allcaps>" if word.isupper() else word for word in splited_tweet]
    return " ".join(splited_tweet2)

######################################

def preprocess(text):
    tweet=replace_repeated_characters(text)
    tweet=replace_repeated_punctuations(tweet)
    tweet=replace_uppercase(tweet).lower()
    tweet=convert_emoji(tweet)
    tweet=replace_urls(tweet)
    tweet=replace_mentions(tweet)
    tweet=replace_hashtags(tweet)
    tweet=replace_numbers(tweet)
    tweet=delete_stopwords(tweet)
    tweet=remove_extra_spaces(tweet)
    return tweet