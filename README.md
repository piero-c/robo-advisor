# robo-advisor

Enjoy!

Authors: Piero C (Lead), Sathun Suthakaran, Ishaan Bansal

Themes: Quantitative Analysis, Computational Finance, Capital Markets

Dependencies: See imports

Runtime: ~ 1 minute

<b>Achievements:</b>

1. Decreased runtime 50% by implementing multithreading, queues, and recursion to speed up requests from AlphaVantage API.
    - This project had the fastest data cleaning pipeline out of everyone who completed the same project (University class).

2. Generated a portfolio with over 40% less volatility compared to a benchmark by using optimized algorithms to develop accurate predictions and financial analyses.

3. Outperformed the benchmark across 100% of trials in metrics such as standard deviation and expected return through effective mathematical models and strategies, as well as optimization algorithms.
    - Includes a five-hundred thousand iteration Monte Carlo simulation that runs in as little as 15 seconds.

4. Successfully implemented the Capital Asset Pricing Model to accurately predict portfolio expected returns.

5. Scored extremely well when evaluated by professor James Thompson and Teaching Assistants.

<b>Problems we Were Able to Fix / Improvements we Were Able to Make:</b>

1. The initial API used for this project broke.
    - Chose a new API for stock data, and developed alphawrap. Alphawrap was created such that all it took to generate the exact same data as the old API calls was a change of the stock object name.
    -    <i>The old stock objects were called 'yf.Ticker'. Once Piero developed AlphaWrap, all we had to do was CTRL+F yf.Ticker, replace with 'Stock', and everything worked as normal.</i>

2. Selecting a model which would be conducive to the goal of the program.
    - Collaborated to discuss important statistical measures, found a trusted pricing model that accurately implements all of them, modified it to fit our needs.

3. General issues with CPU-bound and IO-bound tasks slowing down the program.
    - Removed redundancies and number of API requests, implemented recursive threading, simplified code, implemented Queues and efficient algorithms. (Especially exemplified in Monte Carlo simulation and data cleaning).

4. No objectively correct way to select the tickers that would be used in the final portfolio.
    - Decided that volatility and correlation were the most important factors to consider, created the points system for selecting tickers.

5. Requesting stock history data from AlphaVantage API in the desired format requires a lot of (repetitive) code.
    - Created alphawrap, a module which simplifies the process of performing the requests. Alphawrap also provides functions for other parts of the program (like risk-free rate, stock 'info')

6. Trying to use just one equation to pick the best portfolio presented changes. While beta does consider both volatility and correlation, it's not a perfect measure for our use case. 
    - De-coupled influencing factors by implementing a brand new weights system that took the points system into consideration.

7. Risk-free rate data was hard-coded and not automatically updated, causing small inaccuracies in the expected return of the portfolio.
    - As part of alphawrap, created a function that collects the risk-free rate from AlphaVantage.

<b>Problems / Improvements that Still Exist:</b>

1. The Monte Carlo simulation is a CPU-heavy task. Since the best_weighting function needs to generate 1 million portfolios, the computer spends most of the runtime crunching numbers. With this being said, multiprocessing may have been preferred for our simulation. Unfortunately, we decided that multiprocessing was beyond our scope of expertise.

2. Small optimizations could be made to improve the runtime of the program. For example, re-using stock price information to limit the number of API calls.

3. AlphaVantage can be inconsistent. This means we have to run the API calls at a slower speed than would be optimal.
