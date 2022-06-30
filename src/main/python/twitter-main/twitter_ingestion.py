import tweepy
import pprint
import json
import os

pp = pprint.PrettyPrinter(indent = 1)

def authenticate(filename):
    """
    authenticate with creds.json
    input: filename (str)
            - args:
            {
                client-id,
                secret-id,
                access-token,
                access-token-secret,
                bearer
            }

    returns: headers (dict)
    """
    with open(filename, "r") as f:
        creds = json.load(f)
        pp.pprint(creds)
        f.close()

    return(creds)

def twitter_ingestion():
    
    authenticate("creds.json")
    # print("authenticated successfully.")
    #...


if __name__ == "__main__":

    twitter_ingestion()