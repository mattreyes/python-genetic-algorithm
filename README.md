# python-genetic-algorithm
Implementation of a genetic algorithm using Python. Solves the following problem:

"Given the digits 0 through 9 and the operators +, -, * and /,  find a sequence that will represent a given target number. The operators will be applied sequentially from left to right as you read."

Problem statement taken from http://www.ai-junkie.com/ga/intro/gat3.html

For the selection stage, a stochastic acceptance O(1) search is implemented rather than a linear search. Source: http://arxiv.org/pdf/1109.3627v2.pdf
