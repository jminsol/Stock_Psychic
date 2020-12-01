'''
 * @ Module Name : stock_psychic.py
 * @ Description : Stock Prediction based on stock histody, COVID-19 cases and News sentiment analysis
 * @ since 2020.10.01
 * @ version 1.0
 * @ Modification Information
 * @ authors: Minsol Jeong, Areum Kwak, YoungWoo Lee
 * @ special reference libraries
 *     finance_datareader, konlpy
 * @ Date         Editor              Description
 *  -------    ----------------    ---------------------------
 *  2020.10.01    Minsol Jeong          Initial development
 *  2020.11.25    Minsol Jeong          final development



 # Stock_Psychic
Predict short-term stock prices based on the first half of 2020 stock price history, covid 19 cases, and related stock news. Goals to implement machine learning models by tensorflow, data processing, and Restful API. My contribution is Apple and Tesla stock prediction from NASDAQ.

Goals: 1. Develop sophsicated neural network architecture with the best cost function and optimizer
       2. Analyse sentiment from related stock news to determine positive, netural, and negative tone and come up with scores
       3. Find correlation with covid 19 cases and stock prices by prediction modeling
       4. Implement the system on RESTful API (Web)
       5. Support member services and individual stock recommendations
       
Used skills: Flask, Python, tensorflow, React.js, MariaDB

''' 

* The result of NASDAQ Stock - Apple - Prediction Model
![apple_pred_final](https://user-images.githubusercontent.com/60868240/100791122-222de200-345c-11eb-9edd-754c53abdcd9.png) 
- Compare to real closing price from test set and predicted closing price from the model
![learning 2](https://user-images.githubusercontent.com/60868240/100791409-9072a480-345c-11eb-8c99-9311c06ff1b8.png)

* The result of NASDAQ Stock - Tesla - Prediction Model
![tesla_final2](https://user-images.githubusercontent.com/60868240/100791804-10990a00-345d-11eb-9ea7-0dd0f092c503.png)
- Compare to real closing price from test set and predicted closing price from the model
![tesla_validate](https://user-images.githubusercontent.com/60868240/100791816-142c9100-345d-11eb-952c-add87f56fc7c.png)
