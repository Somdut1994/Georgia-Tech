Final Report: Team02.pdf
Final Presentation: Presentation02_S20.pdf

Extracted and filtered Yelp data in "Yelp-Dataset + GUI-Implementation-Code" folder: Avondale_Restaurant_Review.csv

For running codes for analysis part:
> For Analysis with SVM, run Sentiment-Analysis+Recommendation_SVM.ipynb on Google Colab
> For Analysis with Logistic Regression, run Sentiment-Analysis+Recommendation_Logistic-Regression.ipynb on Google Colab
> For Dataset Insights, run dataset_insights.ipynb on Google Colab
Note: Modify the drive path for Avondale_Restaurant_Review.csv per your necessity, in lines where it is called.

For running the GUI App,
1. Download the entire folder "Yelp-Dataset + GUI-Implementation-Code"
2. set location to inside the folder and run the following command with user name in command line:
python RecommenderEngine.py -user <enter user name>
Example:
for running the app for user id "uFVAAe0JC81IPmxgT49Hcw", run
python RecommenderEngine.py -user uFVAAe0JC81IPmxgT49Hcw
