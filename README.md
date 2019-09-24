# Bloomberg Trading Challenge 2019
## Simulation script and supporting figures of our strategy.

Princeton University Team Members: Ziv Batscha, Joshua Eastman, Warren James, Allan Shen, Cindy Song

In Spring 2019, I led a team of 5 Freshmen in the Bloomberg Trading Challenge. The goal of the challenge was to devise a strategy for investing a million dollars of fake money, and execute that strategy on the Bloomberg Terminal over the course of 10 weeks. When developing our strategy, it was important to note the following: team rankings (total P&L) were public and immediate; there was no edge in picking stocks or in execution of trades; and only the top two teams (with the greatest returns) from each index would be invited to the Finals in NY. Effectively, all teams were investing in a random variable with the same mean but different distributions. In this case, we predicted that the optimal strategy was to maximize variance, while not in first or second place, and minimize variance so long as we were guaranteed to be finalists.
 
Our team strategy at the beginning was to bet on the earnings release reports of the highest implied volatility companies; we bought 200K worth of equity in each of the top five most volatile companies every day, immediately before they released an earnings report, and then sold each position within 24 hours. This strategy earned us ~180k (roughly 18% profit) in the first week. 
 
The Monte Carlo script provided in the repo simulates 1000 trials of 50 day Bloomberg Trading competitions, allowing each team to randomly choose from return distributions resembling those normally found in the market, with the Princeton team taking on maximum variance (100% annual implied vol). The simulation, which supported our intuition and allowed us to better design our strategy, proves that our high vol strategy of betting on binary earnings releases (and holding cash while in the lead) is indeed the most optimal one given the challenge guidelines, both in terms of total assets under management at the end of the competition and in terms of maximizing our Sharpe ratio. In the particular script we have provided, we have a 10.8% chance on average of making the finals (3.42 Edge) when considering ranking by total assets, and a 9.4% chance of winning (2.96 Edge) by Sharpe Ratio. Although we had the highest returns among all 61 competing teams in our index (Russel 3000), we were not allowed to attend the Finals (no reason was provided to us).

Some packages may require prior installation through pip, namely: 
```
pip install click
pip install seaborn
```

To run the simulation with the default settings:
```
python ./BloombergSimulation.py
```

To view optional simulation command-line args:
```
python ./BloombergSimulation.py --help
```

To run a new simulation, simply append the args of interest with their corresponding values. Ex:
```
python ./BloombergSimulation.py --opponent-strategy='mixed' --trials=2000
```
