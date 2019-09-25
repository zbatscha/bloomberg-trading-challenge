# Bloomberg Trading Challenge 2019

### Team Members
Ziv Batscha, Joshua Eastman, Warren James, Allan Shen, Cindy Song

## Rules

- Teams are given $1M notional to paper trade products in the Russell 3000 Index (long positions only)
- Teams could invest a max of $200K per position
- The 2 teams with the top returns are invited to NYC for finals (out of 61 in our division)
- The competition lasted 10-weeks

## Key Ideas

The rules of the competition did not make it a realistic simulation of actual trading for the following reason:

When dealing with actual dollars, a rational person’s utility curve is increasing at a decreasing rate (e.g. sqrt(x) or log(x)). Hence one would need additional edge to justify taking on additional risk.

However, in the case of the competition, finishing 3rd is effectively equivalent to finishing last in terms of realized utility, regardless of paper returns (neither gets to go to NYC).

In such a case, where there is a kink in the utility curve (0U for places 61 to 3, 1U for places 1 and 2), the optimal strategy, aside from obviously maximizing edge, is to maximize variance so long as one is not in the top 2 positions.

## Our Strategy

We took the view that markets are relatively efficient, at least from the point of view of Freshmen, and that we would not find mispricings in the actual stock market.

Further, trades we entered through the competition portal were executed with a 15 minute delay, so ideas we had to market-make wide markets or exploit latency in the competition portal were off the table.

Given that, our strategy was to maximize our variance whenever we weren’t top 2, and hold cash so long as we were top 2.

Because we could only take long positions in stock (no options allowed), the way we would maximize variance would be to invest the maximum possible in a few stocks with the highest variance.

When seeking to maximize variance, we chose which stocks to “invest” in on any given day by evaluating which stocks with earnings on the close had the highest Implied Volatility based on their nearest-dated options. So long as we were top 2, we would hold cash.

To confirm our intuition, we ran some simulations, that supported the idea.

We found that the above strategy gave us above a 50% chance of winning (assuming that other teams were seeking to minimize risk), and that when other teams were maximizing risk, this strategy was still optimal.

## The Results

We were lucky to end up on the right side of the distribution, as our first week of “gambols” paid off (+18%)

We then switched to cash for the remaining 9-weeks of the competition, and no one caught up to us.

Sadly, the judges decided that what we were doing was not investing. And we agree! And we were not invited to the finals.

## To Run Code

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
