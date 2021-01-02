# GooglePlayStore_Review_Scraper_Project

## Back-End Explanation

This is the set of instructions that will need to be followed for the scarapper to work.

1. make sure you have all the needed libraries installed
To intall libraries use "pip install libraryname"
Suggested libraries to install: matplotlib;numpy; beautifulsoup4; selenium; vaderSentiment; wordcloud.
matplotlib==3.3.1
numpy==1.19.3
beautifulsoup4==4.9.3
selenium==3.141.0
vaderSentiment==3.3.2
wordcloud==1.8.1

2. Open the notebook Main in Jupiter or any other channel you use.

3. Open config file here you can do the following:
	- change application link please make sure the link ends with "&showAllReviews=true". This can be done after selecting your app when in Google Play Store by clicking on "Read all Reviews"
	
	- wordcloud colour: make sure you choose a colour that suits you best (recommended not black)
	- mask: in "img" folder you can find all the masks to change how the wordcloud looks like

	- max_words: Currently there are just 200 words selected to appear in a wordcloud. You can increase or decrease. 
	IMPORTANT: don't forget to save changes if not the script will give an error or not the right information will be scrapped

4: Run script. Once you run at the bottom check for: Input filename results. In the box input the name of the app you are scrapping (THIS IS VERY IMPORTANT WHEN OVERVIEWING THE RESULTS - Point 5) (However this feature is hidden)
	- make sure you input the app name

	- Chrome browser will open and the scrolling will start. IMPORTANT: make sure you keep Chrome in full screen mode like it opened

	- Chrome when finished will automatically close

	- Displayed message: "wait 5 seconds to next scroll" this is when the "Show More reviews" botton is clicked

	- the script will run for approximatively 2 minutes. 

5. Output: Result will show in output section of Jupiter section.
	- They will be stored in results directory by "filename_postive/negative/neutral/histogram/analyze results"
	- Result folder: Wordclouds, historgram and txt file with the sentiment analysis per sentance

6. Blocked Words: Open blocked.txt file to add or delete blocked words (Make sure you are writting them correctly)

Additional information:
main.py file is the base file for the script to run in PowerShell (if wanted); 
main.py will be used for the front-end (please check ReadMe file in front-end folder);

Chromedriver files - should not be tampered with;

temporary folder:
	- sentiment_analysis.py file: This is where the sentiment analysis code is located
	 	- "sentance" variable: VADER learn differentiation between pos, net and neutral sentances and words
	- temp.py file:script for scraping reviews and ordering them
test.py and Test.ipynb files (same):checking script 




Python 3 script running by using PowerShell

Download python3.8.2 from https://www.python.org/downloads/release/python-382/ and install downloaded exe file
Check your OS before downloading


Go to project directory config file (see section 2)

Install requirements: ‘py.exe -m pip install -r .\requirements.txt’ . wait until finished. (this step need run 1 time only to install requirements libraries needed. 

Run:   ‘py.exe .\main.py’ to start scraping. This step the chrome browser opens automatically. let it process


You can see the results in "results" directory.

