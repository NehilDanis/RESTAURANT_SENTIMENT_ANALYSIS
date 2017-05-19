#!/usr/bin/python
import ReadCsv
import Convert
import twittertweets
import sys

def main(argv):
    if len(argv) == 1:
        # Convert.readBusinesAndReviews()
        # Convert.readUser()
        ReadCsv.startReadFromCsv()
        twittertweets.getLastestTweet(argv[0])
        ReadCsv.readTxt()
    else:
        print("You must enter one parameter")

    return
if __name__ == "__main__":
   main(sys.argv[1:])
