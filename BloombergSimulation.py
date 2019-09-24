import numpy as np
import click
import math
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import stats
import datetime
"""
Bloomberg Trading Challenge Simulation
Princeton University Team Members: Ziv Batscha (Leader), Joshua Eastman, Warren James, Allan Shen, Cindy Song


Simulates Princeton taking on maximum variance by betting on 5 highest
volatility stocks with earnings releases within 24 hours. Other teams randomly
choose percent return from return distributions of varying standard deviation
and mean of 0.
"""

# figure settings
sns.set(color_codes=True, font_scale=1.5, rc={'text.usetex' : True})
rcParams['figure.figsize'] = 6.5, 6.5 # figure size – inches

# set numpy seed for reproducibility
np.random.seed(seed=97)

@click.command()
@click.option("--annual-trading-days", nargs=1, required=False, type=click.INT, default=252, help="Annual number of days when the stock exchange is open. Default is 252 (Trading Days for 2019).")
@click.option("--max-implied-vol", nargs=1, required=False, type=click.FLOAT, default=100.0, help="Maximum implied volatility for the year. Expects value in [0.0, 100.0]. Default is 100.0 (100%).")
@click.option("--min-implied-vol", nargs=1, required=False, type=click.FLOAT, default=10.0, help="Minimum implied volatility for the year. Expects value in [0.0, 100.0]. Default is 10.0 (10%).")
@click.option("--opponent-strategy", nargs=1, required=False, type=click.STRING, default="random", help="Return distribution variance of competitors. Choose one of these options: \"random\": between [minVol, maxVol], \"low\": daily minVol, \"high\": daily maxVol, \"mixed\": 1/3 high, 1/3 avg, 1/3 random, \"avg\": mean [minVol, maxVol]. Default is \"random\".")
@click.option("--risk-free-return", nargs=1, required=False, type=click.FLOAT, default = 0.0248, help="Theoretical annual rate of return of an investment with zero risk. Expects value in [0.0, 1.0]. Default is 2.48% (0.0248).")
@click.option("--num-portfolio-return-distributions", nargs=1, required=False, type=click.INT, default=100, help="Number of possible standard deviations (i.e. number of portfolio returns distributions to pick from on any given trading day). Default is 100.")
@click.option("--market-drift", nargs=1, required=False, type=click.FLOAT, default=0.06, help="Average annual stock market growth, enforced penalty for holding cash. Expects value in [0.0, 1.0]. Default is 6% (0.06).")
@click.option("--num-teams", nargs=1, required=False, type=click.INT, default=61, help="Number of teams competing in our index (Russel 3000). Default is 61.")
@click.option("--simulation-length-days", nargs=1, required=False, type=click.INT, default=50, help="Number of of days in the Bloomberg Trading Challenge. Default is 50.")
@click.option("--trials", nargs=1, required=False, type=click.INT, default=1000, help="Total simulation trials, where each trial represents a complete 50 day Bloomberg Challenge. Default is 1000.")
def run(
    annual_trading_days,
    max_implied_vol,
    min_implied_vol,
    opponent_strategy,
    risk_free_return,
    num_portfolio_return_distributions,
    market_drift,
    num_teams,
    simulation_length_days,
    trials):

    # max standard deviation of possible portfolio returns distributions
    maxVol = (max_implied_vol/math.sqrt(annual_trading_days))/100
    # min standard deviation of possible portfolio returns distributions
    minVol = (min_implied_vol/math.sqrt(annual_trading_days))/100
    # risk free returns used for calculating Sharpe Ratio
    riskFreeReturn = ((1+risk_free_return) ** (1/annual_trading_days)) - 1
    # assuming on average stock market grows every year, drift enforces a slight penalty for holding cash
    drift = ((1+market_drift)**(1/annual_trading_days)) - 1

    # all possible standard deviations of portfolio returns distributions to pick from on any given trading day (minVol to maxVol with <num_portfolio_return_distributions> increments between
    vol = np.linspace(minVol, maxVol, num=num_portfolio_return_distributions)
    mu = 0 # mean percent return of all portfolio returns distributions

    princeton = num_teams-1 # set Princeton team number for array indexing

    # Our ranking at the end of each trial (50 day competition) by total assets
    rankingPrincetonAllTrialsByEarnings = np.zeros(trials)
    # Our ranking at the end of each trial (50 day competition) by Sharpe Ratio
    rankingPrincetonAllTrialsBySharpe = np.zeros(trials)
    # Our total assets under management at the end of each trial
    earningsPrincetonAllTrials = np.zeros(trials)
    # Our final sharpe ratio at the end of each trial
    sharpePrincetonAllTrials = np.zeros(trials)


    #######################
    # Monte Carlo: <trials> Trials of <simulation_length_days> Day Competitions
    # Default: 1000 trials of 50 Day Competitions
    #######################

    for trial in range(trials): # perform 1000 trials

        # updates team earnings after each turn (50 turns (i.e. days) total in single competition), each team starts with $1M
        teamEarnings_AssetsGame = np.ones(num_teams)

        # tracks daily returns of all teams to calculate Sharpe Ratio
        teamReturns_SharpeGame = np.zeros((num_teams, simulation_length_days))

        # index positions of top ranking team at end of each day
        teamInd1E = 0; # 1E denotes 1st place team if competition ranked by earnings
        teamInd2E = 0;
        teamInd1SR = 0; # 1SR denotes 1st place team if competition ranked by Sharpe Ratio
        teamInd2SR = 0;

        for day in range(simulation_length_days): # for each day in current competition trial...
            for team in range(num_teams): # ...let each team pick a portfolio return distribution (represented by the mean,mu, above, and a standard deviation selected from all possible standard deviations in the vol array

                if (team == princeton): # if it's our turn to make a decision that day

                    # make a move only if we're not 1st or 2nd by Total Assets Under Management
                    if (princeton != teamInd1E) and (princeton != teamInd2E):

                        # pick a random percent return from distribution with maxVol and mean mu
                        returns = max(-1,min(np.random.normal(mu,maxVol),1))

                        # apply percent return of the day and update earnings, add one since distribution centered at mean of 0
                        teamEarnings_AssetsGame[team] *= (1+drift+returns)

                    # make a move only if we're not 1st or 2nd by Sharpe Ratio
                    if (princeton != teamInd1SR) and (princeton != teamInd2SR):

                        # pick a random percent return from distribution with maxVol and mean mu
                        returns = max(-1,min(np.random.normal(mu,maxVol),1))
                        # save team's daily returns for Sharpe Ratio
                        teamReturns_SharpeGame[team, day] = returns

                # all other teams choose a portfolio returns distribution on their turn (determined by given opponent_strategy, default is "random")
                else:

                    if opponent_strategy == "random":
                        tempVol = vol[np.random.randint(0, len(vol))]
                    elif opponent_strategy == "low":
                        tempVol = minVol
                    elif opponent_strategy == "high":
                        tempVol = maxVol
                    elif opponent_strategy == "mixed":
                        if (team <= (num_teams/3)):
                            tempVol = np.mean(vol)
                        elif (team <= 2*(num_teams/3)):
                            tempVol = maxVol
                        else:
                            tempVol = vol[np.random.randint(0, len(vol))]
                    elif opponent_strategy == "avg":
                        tempVol = np.mean(vol)
                    else:
                        raise Exception("Please choose a valid opponent strategy")
                    # pick a percent return from distribution with tempVol and mean mu
                    returns = max(-1,min(np.random.normal(mu,tempVol),1))

                    # apply percent return of the day and update earnings
                    teamEarnings_AssetsGame[team] *= (1+drift+returns)
                    # save team's daily returns for Sharpe Ratio
                    teamReturns_SharpeGame[team,day] = returns

            # Find top ranking teams (1st & 2nd) at end of trading day of days

            ########## Rankings by Earnings ##########

            # Find team number of 1st place team so far in competition (after x day of 50 days)
            indx_top_two_assets = np.argpartition(teamEarnings_AssetsGame,-2)[-2:]
            teamInd1E = np.where(teamEarnings_AssetsGame == max(teamEarnings_AssetsGame[indx_top_two_assets]))[0].item()

            # Find team number (index = teamInd2) of 2nd place team so far in competition (after day of 50 days)
            teamInd2E = np.where(teamEarnings_AssetsGame == min(teamEarnings_AssetsGame[indx_top_two_assets]))[0].item()


            ########## Rankings by Sharpe Ratio ##########

            if day > 1:
                tempTeamReturns = teamReturns_SharpeGame[:,:day]
                tempTeamSharpe = (np.mean(tempTeamReturns-riskFreeReturn, axis = 1) / np.std(tempTeamReturns-riskFreeReturn, axis=1, ddof=1)) * math.sqrt(annual_trading_days)

                # Find team numbers of 1st and 2nd place teams so far in competition (after day of 50 days)
                indx_top_two_sharpe = np.argpartition(tempTeamSharpe,-2)[-2:]
                teamInd1SR = np.where(tempTeamSharpe == max(tempTeamSharpe[indx_top_two_sharpe]))[0].item()
                teamInd2SR = np.where(tempTeamSharpe == min(tempTeamSharpe[indx_top_two_sharpe]))[0].item()

        # save total assets under management at end of each trial/competition
        earningsPrincetonAllTrials[trial] = teamEarnings_AssetsGame[princeton];

        # sort earnings array in ascending order, maintain association by team number
        sortedTeamIndEarnings = np.argsort(teamEarnings_AssetsGame)
        # Save the Princeton's ranking at the end of each competition by Total Earnings
        rankingPrincetonAllTrialsByEarnings[trial] = num_teams-(np.where(sortedTeamIndEarnings == princeton)[0].item())


        # Annualized Sharpe Ratio for each team
        sharpeRatio = ((np.mean(teamReturns_SharpeGame-riskFreeReturn, axis = 1))/np.std(teamReturns_SharpeGame-riskFreeReturn, axis=1))* math.sqrt(annual_trading_days)
        # Save Princeton's Sharpe Ratio
        sharpePrincetonAllTrials[trial] = sharpeRatio[princeton];

        # save the ranking of Princeton team at the end of each competition by Sharpe Ratio
        sortedTeamIndSharpe = np.argsort(teamReturns_SharpeGame[:,day])
        rankingPrincetonAllTrialsBySharpe[trial] = num_teams -(np.where(sortedTeamIndSharpe == princeton)[0].item())

    ########## Best Stategy by Total Earnings ##########

    # Frequency of Princeton getting to finals
    PrincetonFreqFinalsByEarnings = (rankingPrincetonAllTrialsByEarnings == 1).sum() + (rankingPrincetonAllTrialsByEarnings == 2).sum()

    # Probability of Princeton being first or second and proceeding to finals
    ProbabilityOfPrincetonFinalsByEarnings = PrincetonFreqFinalsByEarnings/trials

    # How much more likely we are to win the competition playing with our strategy
    EdgeByEarnings = PrincetonFreqFinalsByEarnings/ ((2*trials - PrincetonFreqFinalsByEarnings)/(num_teams-1))

    ########## Best Stategy by Sharpe Ratio ##########

    # Frequency of Princeton getting to finals
    PrincetonFreqFinalsBySharpe = (rankingPrincetonAllTrialsBySharpe == 1).sum() + (rankingPrincetonAllTrialsBySharpe == 2).sum()

    # Probability of us being first or second and proceeding to finals
    ProbabilityOfPrincetonFinalsBySharpe = PrincetonFreqFinalsBySharpe/trials

    # How much more likely we are to win the competition playing with our strategy
    EdgeBySharpe = PrincetonFreqFinalsBySharpe/((2*trials - PrincetonFreqFinalsBySharpe)/(num_teams-1))


    ##### Saving simulation results #####

    now = datetime.datetime.now() # used as a label for matching figures to performance stats in txt file

    output_txt = "Simulation_Output.txt"
    with open(output_txt,'a+') as f:
        f.write("Simulation Completed on {0}/{1}/{2} T{3}:{4}:{5}\n".format(now.month, now.day, now.year, now.hour, now.minute, now.second))
        f.write("Simulation Settings: \n\ttrials={0}\n\tsimulation_length_days={1}\n\tnum_teams={2}\n\topponent_strategy={3}\n\tannual_trading_days={4}\n\tmax_implied_vol={5}\n\tmin_implied_vol={6}\n\trisk_free_return={7}\n\tnum_portfolio_return_distributions={8}\n\tmarket_drift={9}\n".format(trials, simulation_length_days, num_teams, opponent_strategy,annual_trading_days, max_implied_vol, min_implied_vol, risk_free_return, num_portfolio_return_distributions, market_drift))

        f.write("––––– If Team Ranking Determined by Total Earnings ––––\n")
        f.write("Frequency of Princeton attending the finals (1st or 2nd place) of {0} trials: {1}\n".format(trials, PrincetonFreqFinalsByEarnings))
        f.write("Probability of Princeton being 1st or 2nd and proceeding to finals: {0}\n".format(ProbabilityOfPrincetonFinalsByEarnings))
        f.write("Princeton's edge (how much more likely we are to win playing our strategy): {0}\n".format(EdgeByEarnings))

        f.write("––––– If Team Ranking Determined by Sharpe Ratio ––––\n")
        f.write("Frequency of Princeton attending the finals (1st or 2nd place) of {0} trials: {1}\n".format(trials, PrincetonFreqFinalsBySharpe))
        f.write("Probability of Princeton being 1st or 2nd place: {0}\n".format(ProbabilityOfPrincetonFinalsBySharpe))
        f.write("Princeton's edge (how much more likely we are to win playing our strategy): {0}\n".format(EdgeBySharpe))

        f.write("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\n")
        f.write("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––\n")

    ##### Figures #####

    ## Princeton ranking across all trials By Total Assets Under Management ##
    ax1 = sns.distplot(rankingPrincetonAllTrialsByEarnings, bins=61, kde=False, norm_hist=True, rug=False, hist_kws=dict(edgecolor="k", linewidth=1))
    ax1.set(xlabel='Princeton Ranking By Total Assets Under Management', ylabel='Probability')
    plt.show()
    fig1 = ax1.get_figure()
    fig1.savefig('Princeton_Ranking_Total_Assets_Under_Management_{0}_{1}_{2}_{3}_{4}_{5}_{6}.png'.format(opponent_strategy, now.month, now.day, now.year, now.hour, now.minute, now.second))

    ## Princeton's total percent return across all trials considering ranking by Assets (with 0.02% Drift) ##
    ax2 = sns.distplot(earningsPrincetonAllTrials, bins=100, kde=False, norm_hist=True, rug=False, hist_kws=dict(edgecolor="k", linewidth=1))
    ax2.set(xlabel='Princeton Total Percent Return on Assets', ylabel='Probability')
    plt.show()
    fig2 = ax2.get_figure()
    fig2.savefig('Princeton_Total_Percent_Return_On_Assets_{0}_{1}_{2}_{3}_{4}_{5}_{6}.png'.format(opponent_strategy, now.month, now.day, now.year, now.hour, now.minute, now.second))

    ## Princeton's ranking across all trials by Sharpe Ratio ##
    ax3 = sns.distplot(rankingPrincetonAllTrialsBySharpe, bins=61, kde=False, norm_hist=True, rug=False, hist_kws=dict(edgecolor="k", linewidth=1))
    ax3.set(xlabel='Princeton Ranking By Sharpe Ratio', ylabel='Probability')
    plt.show()
    fig3 = ax3.get_figure()
    fig3.savefig('Princeton_Ranking_By_Sharpe_Ratio_{0}_{1}_{2}_{3}_{4}_{5}_{6}.png'.format(opponent_strategy, now.month, now.day, now.year, now.hour, now.minute, now.second))

    ## Distribution of Princeton's final Sharpe Ratio at end of each trial ##
    ax4 = sns.distplot(sharpePrincetonAllTrials, bins=100, kde=False, norm_hist=True, rug=False, hist_kws=dict(edgecolor="k", linewidth=1))
    ax4.set(xlabel='Princeton Sharpe Ratio at End of Competition', ylabel='Probability')
    plt.show()
    fig4 = ax4.get_figure()
    fig4.savefig('Princeton_Sharpe_Ratio_Competition_End_{0}_{1}_{2}_{3}_{4}_{5}_{6}.png'.format(opponent_strategy, now.month, now.day, now.year, now.hour, now.minute, now.second))

if __name__ == "__main__":
    run()
