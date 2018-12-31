# Final Feature List

## User Management
1. User account.
    1. **Username** is the main identifier
    2. Username and password are the only mandatory things to register. Users can also optionally add email address during registration. After registration they can additionally add 2FA or email.
    3. How does 2FA work?
        1. 2FA via Google authenticator. (for logins)
    4. The user won't be able to reset their password if they don’t enter an email address.
2. Automatic password recovery emails.
3. reCAPTCHA for logins after 5 incorrect tries, and for registration.

## Payments System
1. On-chain means that a person has not registered an account and is only sending crypto to fund a certain bet, after the bet is graded he either receives his crypto instantly to the address that he provided if he won or not if he lost. Off-chain means that a user has registered an account and funded it with crypto so he can make bets from his account and doesn't need to send crypto every time he makes a bet. And after the bet is graded he receives his winning back to his account.
    1. So there will be a account model stored in the database.
2. Hot wallet from which transactions are made for on-chain and off-chain payments (on-chain as in payments made on sportsbook without an account and off-chain as in withdrawals from user account).
3. Multi-currency support (BTC, ETH, LTC, DASH, DOGE, BCH) 
4. Sportsbook balance:
    2. Because payments are made from hot wallet, a separate balance tracking system has to be made for sportsbook. 
    3. This only applies to alts (not BTC), this is to avoid currency conversions on every bet. For example if a bet of 1ETH at x2 odds is made (regardless if it's on-chain or off-chain) and won (extra logic in "Sportsbook" paragraph) check if there is enough ETH in sportsbook balance if no convert to have enough if yes credit the players account(off-chain) or make a payout(on-chain). 
    4. This balance can be viewed and funded manually through admin panel.

### Wallet
1. Each of the coins must have their own daemon installed and no 3rd party payment channels should be used.
2. Input selection (to consume as least inputs as possible) change always goes to a new address. Spend those outputs that are most relevant to size, for example if a person withdraws 1BTC search for output that is closest to 1BTC, if a person withdraws 0.01BTC search for output that is closest to 0.01BTC, applies to all coins.
    1. Address selection for the user payout
        1. Pick the address such that SUM(BALANCES) = PAYOUT
    2. Input is the amount and currency
    3. output 
        2. is the list of addresses
        3. Or insufficient fund in currency error
            1. Then call exchange API and retry the transaction
3. Procedure of a payout
    4. *ADMIN_TRANSACTION_FEE = **Get transaction fee from admin service*
        4. A transaction fee is always deducted from withdrawal, that fee is different for each coin and is configurable through admin's control panel. 
    5. *ACTUAL_TRANSATION_FEE: Get the transaction fee for acceptance in 1 block from 3rd party API*
        5. When making withdrawals always use the fee that guarantees that a transaction will get included in the next block regardless of what the transaction fee is configured to be charged in admin's panel
    6. Deduct the ADMIN_TRANSACTION_FEE from the payout, pay it to the user with the ACTUAL TRANSACTION FEE
4. Managing Transaction Outputs
    7. A change amount should never be lower than the minimum standard output for that coin, and there must always be a change even if the withdraw perfectly matches the output we spend.
    8. Consolidation: automatically spends all outputs that are smaller than 0.001 for all coins and sends them to one new address, this is manually triggered on admin panel.
5. *3rd party API*: Integration with blockcypher for 0-confirmation BTC transactions.
6. *Combined Register and Place Bet API*
    9. Ability to deposit into account and to fund the bet directly. After the creation of account a new deposit address is not generated, only when a user presses the deposit button for a specific coin will a deposit address be generated.
7. Node Settings
    10. All BTC deposit and change addresses should be segwit.
    11. Withdrawal address validity check, only support normal addresses (starts with 1 or 3) and no bech32 support for BTC, or other standard addresses for other coins.
        6. An API to check whether address is valid
8. Fetch Exchange Rates
    12. Admin data management
    13. Cron Job for Automatic
        7. Fetching of Exchange rates can be either "STATIC" or “AUTOMATIC” where the term “or other currency equivalent” is mentioned.  Static means that once set it will not change unless otherwise manually done so. Automatic means that, it will update every hour.

#### Circuit breakers
1. No more than 2BTC (or other coins equivalent) unconfirmed transactions for each coin each (both on-chain and off-chain applies).  "STATIC"
2. If this 2BTC is reached ask for 1 confirmation on all transactions. Except ether because it's always required to have 1 confirmation.
3. No payouts if there are any unconfirmed transactions.
4. Minimum withdraw is 0.0001BTC or other currency equivalent, with no minimum deposit. "STATIC"

5. Transfer funds to cold storage if hot wallets become larger than 20BTC or other currency equivalent (no global limit), cold storage address is specified in admin's panel. "STATIC"

1. [RBF]
    6. If transaction got replaced (via RBF) and amount sent is correct accept the new transaction. (on-chain)
    7. If transaction got replaced (via RBF) and amount sent is incorrect reject the bet and return deposit. (on-chain)
    8. If transaction got replaced (via RBF) accept the new deposit (off-chain).
2. ADMIN Settings
    9. Transactions sent to deposit address (off-chain) require confirmations:
        1. BTC: 0 (upto 1BTC after being deemed safe via blockcypher, anything bigger requires 1)=
        2. ETH: 2
        3. LTC: 1
    10. Transactions sent to deposit address (on-chain) require confirmations:
        4. BTC: 0 (upto 1BTC after being deemed safe via blockcypher, anything bigger requires 1)
        5. ETH: 1
        6. LTC: 0
3. Generate new address
    11. Every user can request a new deposit address when at least one deposit is made to the most recent address, deposits to all previous wallets must also be credited even after a new address is generated.
4. Accept transaction
    12. No transaction for any coin should be accepted that:
        7. Has lower than standard fees, has unconfirmed parents, is non-standard (though if we're running up to date node that shouldn't happen)
        8. If withdraw amount is 10 times larger than deposit AND is more than 1BTC strike for manual review. (except on-chain bets, they should have no restrictions)
5. When making payouts for on-chain wagers always make sure that deposit has at least 1 confirmation regardless of coin. Same applies for withdrawals from accounts.
6. When making withdraw from account only spend confirmed outputs unless they are deposited to admin's account, or have been made by site itself.

## Internal Exchange System
1. Purpose exchange our given currency against another one
2. Will used by both the internal services and the frontend too
4. Inbuilt currency exchange via shapeshift api (to exchange between accepted currencies) (0.5% fee on top of shapeshift)
    1. The maximum amount to be allowed to exchange is 0.5BTC or other currency equivalent and the minimum amount should be 25000 satoshi or other currency equivalent. After a command is received to exchange funds and if it's higher than 0.001BTC or other currency equivalent immediately exchange the funds on shapeshift otherwise wait till it piles up. "AUTOMATIC"

#### Circuit breakers
    1. No exchanging if there are any unconfirmed deposits.

## P2P Transfer System
1. API to initiate rain
    1. Description: a user initiated rain which is processed as an off chain payment to some random users
    2. Request
        1. Number of User(N)
        2. Amount
            1. Min: 10k satoshi or other currency equivalent "Static
        3. Currency
    3. Response
        4. None

2. Rain Initiated by User
    4. Users can rain in the chat themselves , they can choose how much(X) to rain and to how many people(N). 
    5. X divided by N, every person gets equally. For example 0.005BTC (X) to 5(N) people would give 0.001BTC each.
        5. This will be just recorded as a transaction our database
    6. Minimum X is 10k satoshi or other currency equivalent "Static

### Circuit breakers
No rain if there are any unconfirmed deposits.
1. Tipping users:
    1. Sends crypto from one account to another.
    2. Minimum is 1k satoshi or other currency equivalent "Static"
    3. A fee of 100 satoshi is charged for BTC transfers. (only BTC).
1. Rain Initiated by the System:
    4. Get the list of users who have written more than 500 words in the last 30 mins, let's call this list "u".
    5. Choose a random number between 5 and 25(Both Included) with a uniform probability distribution, let's call this number "n".
    6. Choose "n" users out of “u” randomly with a uniform probability distribution.
    7. How much(X) to rain and how frequently (P mins) will be specified in Admin panel. (How much will be specified for each coin.)
    8. Select a coin to rain and that coin should be random for every rain.
    9. Award the amount X to each chosen users
    10. Admin Panel Feature: This process will be repeated every x minutes, this value is static but can be edited
    11. The starting reference for this rain 00:00 UTC.

## Sportsbook
1. For on-chain betting there are 3 options that is Flexible, Negotiate and Firm odds.
2. When using Flexible option, confirm bet(s) at the best available odds upon receiving deposit
3. When using Negotiate option, confirm bet(s) at the best available odds upon receiving deposit and if some bet(s) odds became lower than quoted in the betslip allow user to confirm/decline odds change. If no confirmation is received from the player wait till odds reach the quoted odds, or refund the bet after the event has ended.
4. When using Firm option, confirm bet(s) at the best available odds upon receiving deposit and if some bet(s) odds became lower than quoted in the betslip refund the wager.
5. If sent wager is bigger than max bet (on single bets or parlays) or not equal (on multiple selections) return bet.
6. Return deposit for bet (this will in Sportsbook)
    1. If a transaction is received after the start of the event (at least one of them) or is not deemed safe until then, return the deposit.
7. Show recommended transaction fee for each coin for fastest confirmation time.
8. Each on-chain betslip, whether it's multiple selections or just one, must have a unique address generated upon its creation.
9. To create an on-chain betslip a person needs to choose his event, amount to bet, and specify his address where the winnings will be sent.
10. Both for on-chain and off-chain min bet is 0.0001BTC or other currency equivalent, and max bet is indicated by MonsterByte. "STATIC"
11. For betting data use the MonsterByte API.
12. In Sportsbook "best available odds" means odds by provider whether it got bigger or smaller than previously quoted odds.
13. MonsterByte API implementation.
    2. Do not accept any more sportsbook wagers if monsterbyte's account is not sufficient enough.
    3. Do not accept any more wagers for the certain events if max bet on MBI was reached.
    4. Do not accept any bet if it cannot be placed on monsterbyte API.
    5. After receiving the wager (regardless if it's on-chain or off-chain) place that wager on monsterbyte.

### Placing sportsbook bet logic:
1. When making wagers in alts on sportsbook:
2. Convert altcoin to BTC at the exchange rate at the time of placing wager "Automatic" (do NOT actually convert it through shapeshift) ->
3. Check if there's enough balance on MonsterByte to place that wager, if no:
4. On on-chain return message "Bet rejected" and return crypto to specified address (minus transaction fee)
5. On off-chain return message "Bet rejected" and do not allow to place a wager. If there's enough BTC then ->
6. Place that bet in BTC on MonsterByte, If lost keep the alts if won ->
7. Check if there's enough of the alt, that the bet was placed in, in the sportsbook's balance, if yes and it was on:
8. On-chain -> pay the winnings
9. Off-chain -> credit the account with the winnings
10. If no, convert enough BTC on shapeshift to that alt to pay out the winnings.

### When making wagers in BTC on sportsbook:
1. Check if there's enough balance on MonsterByte to place that wager, if no:
2. On on-chain return message "Bet rejected" and return crypto to specified address (minus transaction fee)
3. On off-chain return message "Bet rejected" and do not allow to place the wager. If there's enough BTC then ->
4. Place that bet in BTC on MonsterByte, If lost keep the BTC if won ->
5. On-chain -> pay the winnings
6. Off-chain -> credit the account with the winnings
1. USA it's territories, UK and Australia blocking.
    1. Frontend side feature: Allow to navigate the site, but when trying to add a bet or pressing the login/register button a pop-up will appear.

## Stats
1. Investment stats on investment page
    1. Bankroll: Each coin will have it's own bankroll.
    2. Effective bankroll
    3. Investor's profit
    4. User's bankroll
    5. User's effective bankroll
    6. User's profit.
    7. All of the above is separate for each coin.
2. Stats on individual users for dice game (wagered, profit, total bets, luck) (users can choose not to display wagered and profit to the public)
3. Bet status page for on-chain bets. 
4. Ability to share off-chain bet slips through links that can be generated from wager history tab.
    8. A link for each bet slip can be generated, if shared it would redirect to page where it contains bet slip's details.
        1. "Bet status" (won, lost, pending)
        2. "Time" (when bet was placed)
        3. "Event"
        4. "Selection"
        5. "Odds"
        6. "Amount bet"
        7. "Amount to win"

## Plinko Dice
### Game Engine:
1. A number between x0.01 and xX is rolled. The X is variable and can be adjusted from x1.01 to x10000.00
2. The number that is rolled is the result of the game.
3. Say a player sets the X to x100 any number rolled (x10.03, x80.56, x0.12) will be the result of the game and the wager will be multiplied by the result of the game.
4. The lower X the more likely it is to hit winning multipliers (over x1.00) and the higher the X the more likely it is to hit losing multipliers (under x1.00)
    1. Use a exponentially decreasing probability function
    2. So for example if the player chooses X as x100 the outcomes will be lower with infrequent higher multipliers. Because the higher the multiplier the lower the chances of hitting it.
    3. And if the player chooses X as x1.1 the outcomes will be higher with infrequent lower multipliers.
    5. The game will have a house edge of 1% so no matter what the multiplier is the average outcome will always be x0.99 for each bet.
6. Everything will have to be made provably fair (Client seed + server seed + %chance + nonce = result)
7. Balance has to update after every bet. After a win it flashes green and after a loss red.
8. Minimum bet is always 1 satoshi, and the minimum positive displayed balance is also 1 satoshi, however the balance must be tracked upto a 100th of satoshi. For example player has 1 satoshi exactly, goes all in with it and wins 0.6 satoshi, the balance must still be displayed as 1 satoshi, he then bets all in again (1 satoshi, can't bet x.x satoshi) and wins 0.4 satoshi, only then his balance is updated to 2 satoshi.
9. Maximum bet is 0.75% of effective bankroll.
10. 0.25% commission of each bet made win or loss gets deducted from the bankroll and is deposited into admin's account.
11. List bets over 0.005BTC or other currency equivalent under the high rollers tab. "STATIC"
    4. Every person can view high roller's tab for dice game. However both, bets on dice and sports book would be listed on admins panel (no user can view sports book wagers)
12. Update all bets tab every 0.5 seconds.
    5. Information that is displayed all bets, my bets, highrollers tab:
"Beti ID",“User”,“Time” (24 hour clock, only hour and minute is shown), “Bet amount”, “Payout” “Chance” (percentage that shows the possibility to roll x1.01 or above), “Game” (potential maximum payout between x1.01 and x10000), “Profit” (if won positive, if lost negative)
1. Delay bets of:
    1. 0 BTC by 1 second
    2. 1-10 satoshi by 0.5 second
    3. 11-100 satoshi by 0.1 second
    4. 101-999 satoshi by 0.05 second
    5. 1000 satoshi and above 0.01 second
    6. And other currency equivalent. "STATIC"
    7. Obviously only registered users can make bets.
1. Disable the seed when the user makes a
    8. Tip
    9. Investment change
    10. Withdraw
    11. Exchange
    12. Withdraw

## Investment System:
1. Investment system for the dice game with variable leverage (from x1 to x10)
    1. Users can choose to invest in bankroll that is used to finance bets for dice game.
    2. The moment an investment is opened, the initial investment amount is exchanged for the share in site effective bankroll with percentage equal to the ratio of contributed funds to the effective bankroll fund. When an investment is closed, the share is exchanged back for funds according to the current bankroll amount.
    3. Say the effective bankroll is 50BTC userA decides to invest 50BTC at leverage x1. His share in effective bankroll is now 50%. Players are losing and bankroll has now risen to 150BTC. UserA's share is still 50% but now it’s 50% of 150BTC and not 100BTC. He can then choose to withdraw his share for 75BTC.
    4. If for example the effective bankroll is 100BTC (2 user each 50BTC at x1 leverage both own 50% of the effective bankroll each). Another user decides to invest 100BTC his share would now be 50% of the bankroll and the previous people's share would be diluted to 25%. Making it 25%+25%+50%.
    5. Leverage works like this. Say a person has 10BTC but wants to have a higher stake in effective bankroll. So he chooses to invest at x10 leverage making his investment worth 10 times more in the effective bankroll. Let's say that he is the only investor making the effective bankroll 100BTC, this allows for a max profit of 0.75BTC per bet. Someone bets that and wins 0.75BTC. The effective bankroll has now dropped to 92.5BTC. The user still has 100% share in the bankroll and can choose to withdraw it, but now it would only be worth 9.25BTC.
    6. If there's one investor who has 10BTC invested at x10 leverage (making effective bankroll 100BTC), the max profit a player can get from single bet is 0.75BTC (because max bet is always 0.75% of the effective bankroll). If player wins the available max bet, the effective bankroll will decrease by 0.75BTC x10 (7.5BTC) and after that the max profit per bet would be 0.69375BTC (0.75% of 92.5BTC)
    7. One more example. Let's say there are 3 investors. A who has 10BTC at x1, B who has 10BTC at x5 and C who has 10BTC at x10 making the total effective bankroll of 160BTC and the stake in it are as follow: A(6.25%), B(31.25%) and C(62.5%). The max available bet would be 1.2BTC (0.75% of 160BTC). If player bets and wins 1.2BTC, that loss is shared between the investors proportional to their share in the bankroll.
    8. Afterwards the effective bankroll would be 150.55BTC. The stake in the bankroll remains the same between investors but it's worth as follows: A(9.925BTC), B(9.625BTC) and C(9.25) when all of their initial investment before leverage was 10BTC each. Investor's profit (or loss) is proportional to stake (%) in the effective bankroll, the higher the investor's share in the bankroll is the bigger the win/loss is (higher exposure).
    9. 0.25% fee for the owner works like this: the moment someone bets any amount 0.25% of that amount is deducted straight from the effective bankroll. Say someone bets 1BTC regardless of whether the result is win or loss, 0.0025BTC is deducted from effective bankroll.

### Circuit breakers:
1. No investing if there are any unconfirmed deposits.
2. Min investment is 0.001BTC or other currency equivalent with no max. "STATIC"

## History
1. Every user can review it's:
    1. Game History
        1. Complete sportsbook wager history.
    2. Transactional History
        2. Complete invest/divest history.
        3. Complete deposit/withdraw history.
        4. Complete tipping history.

## Notifications
1. User will get notified in the notification bar when:
    1. One deposits, but that deposit requires confirmation.
    2. A deposit is confirmed and credited.
    3. Someone has messaged (PM) that user.
    4. Someone has tipped that user.
    5. A bet is graded (sportsbook).
    6. All these notifications have to be updated in real time.

## Chat Room
1. Admin Panel Feature: Ability to promote certain people to mod status. This allows them to ban other people for a certain time.
2. No more than one chat message per 2 seconds per user is allowed to prevent spam.
3. Direct messaging with users (PMs)
    1. The user can find other users username through chat.
4. Ability to block user by another user (does not show user's chat and blocks pms) (nothing shows up when a blocked person sends a pm or writes in chat)
5. ChatBot features:
    2. Make Rain every x minutes. See P2P Transfers in Payments System

## Admin Panel 
1. Only 1 Admin Account is needed with complete access
2. Use G-Suite for Email Support
3. Easily editable circuit breakers:
    1. Max unconfirmed transactions value.
    2. Max hot wallet.
4. Hot wallet status.
5. Sportsbook balance status
6. Ability to fund sportsbook's balance.
7. Fee to be charged for each coin on withdrawals.
8. Rain settings.
9. Consolidation, this has to be triggered manually.
10. "Static" value updating.
11. Ability to view each user's bet history, account balance, deposit/withdraw history.
12. Global stats for both plinko dice and sports book (total wagered, profit/loss, total bets for selected time period) this lists all of the bets for selected time period and highlights highroller wagers.
13. Ability to process a withdrawal manually if the bet win range is 10x higher (and is above 1BTC) than the difference between the amount deposited in BTC and won in BTC. (applies to alts as well)
14. Ability to view any pending withdrawals.

### Panic buttons
1. Stop all withdrawals or for certain accounts.
2. Stop accepting bets for certain currencies (or all) on sports book and/or on dice game.
3. Stop accepting bets for certain leagues, games on sports book. ( both on-chain and off-chain)

## DevOps
1. The development environment will be set up on AWS.
2. Project should be made scalable to handle traffic/bets in huge amounts.
3. Servers should be DDoS protected and other security measures such as middle men-attack/SQL etc.  injections, should be taken care of.
4. Test-net should be set-up for every coin
5. Care should be taken so no private information is leaked to unauthorized sources including breach of our user database to other 3rd parties.
