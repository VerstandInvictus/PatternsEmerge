# PatternsEmerge
An automated toolkit for graphing the results of simulated day trading on MarketDelta Cloud.

### Project description

First: This is not an attempt at algorithmic trading. I am not that foolish or that flush with cash that I'm prepared to simply light on fire. Nothing in this code is intended to interact with the market directly. 

What this is is an attempt to interact with MarketDelta Cloud, a surprisingly robust and useful (at least at my introductory level) cloud based trading platform, in order that I can automatically graph and analyze my attempts (via realistically simulated trading) to identify a workable edge.
 
This project will be based on Python, Flask, MongoDB, jQuery, and c3.js.

### Why are you trying to day trade?
#### (or, *You fool, you'll lose your shirt!*)

Because I'm interested in the challenge, and because the potential upside is too big to ignore, and because I can learn with no risk via simulation. And because I'm tired of watching this strange mathematical organism writhe and slither its way across the economy, its very life reflecting our collective hopes and fears, without taking a crack at understanding its behavior.

### So what's your strategy?
You can buy it from me for four very reasonable monthly payments of $1337.25... aw, I'm just kidding. But seriously, that's about the response that seems to be standard in blogs and resources about this. There are hints, enough to get you into a position where you can lose, but not much more. It seems that on Wall Street, unlike in tech and software development, nothing is free, especially not information. I don't, obviously, agree with this.

I don't have a strategy that I'm confident in yet; that's the point. The instrument that seems most reasonable is the CME E-mini S&P 500 futures, which are highly liquid, highly volatile, and an index representation. +/- 1 tick is +/- $12.50 per contract not counting commission and fees. Currently I'm attempting to gauge the direction of the previous day's trading and any off-hours activity and call the direction of the first swing immediately post-market open (6:30AM PST) and enter either long or short right before the bell, accordingly, with a -6 stop-loss and a +12 target. If I catch a trend and it appears in my best estimation to be slowing or reversing while I'm net positive, I'll dump rather than risk staying in. The whole trade should last no longer than 20-30 minutes, and ideally much less. One trade a day, then move on to real life.

This risk/reward ratio should, if I can correctly call the first swing and execute successfully about 40-45% of the time, result in an edge. I'm also interested in seeing what -20/+40 would do on a longer timescale (fire and forget) but that's well past pushing the risk I'd be willing to take on if this was for real, and I'm reasonably sure there won't be that much volatility in this instrument once the fallout of Brexit passes - and part of the point of this exercise is to keep my mindset as close as possible to what it would be if this was real.
