GENETIC MONKEYS
===============

Genetic monkeys is an exploration into the building blocks of an artificial intelligence based upon the principles of synthetic biology. The ultimate goal is to solve the problem of problem solving using a combination of evolutionary computing, genetic algorithms, machine learning, statistics, and biology. These are some initial sandbox explorations.

### geneticmonkeys.py

This module is a play on the ["infinite monkey theorem"](https://en.wikipedia.org/wiki/Infinite_monkey_theorem), an np-hard combinatorial optimization problem. We define an objective phrase, such as 'To be or not to be', spawn an initial population of 'monkeys' each representing a solution, which evolves across generations, or iterations, using the process of selection and reproduction.This process is defined according to a set of 'genetic' 'Environment' variables passed through the command line: maximum population, mutation rate, birth rate, and mortality rate.

Presently in a 95 symbol set, the algorithm is able to resolve unknown phrases under 5 symbols almost instantly; phrases under 20 symbols can be expected to be found anywhere between seconds to several minutes.

It has been noticed that a significant aspect of performance is determined by the suitibility of the objective function for the respective phrase being used. For example, one function might work well for longer phrases, but return poor performance for short phrases. For this reason implementing learning / optimization within the objective function at iself is being considered.

Taboo search was explored, but worsened performance. However the functionality is only commented out so you may explore this.

Further work includes developing embedded metrics to be able to collect runtime statistics, a closer examination into the objective function, and perhaps even generalizing the functionality to perform combinatorial optimization for a number of different variations, for example, travelling salesman, and the knapsack problem.

### metamonkeys.py

While we certainly could have built a plain old analytical algorithm which exhaustively explored the viable parameter space for the optimal set of parameters for the `geneticmonkeys.py`, I decided to spin up a second genetic layer instead. Of course by doing this we subject the optimization of the first layer to the unverifiable optimality of the second layer, but to mitigate this I plan on spinning up a third layer. (You may say, "well, we'll find ourself in the same situation as before, only a layer up", you should read [this](https://en.wikipedia.org/wiki/Turtles_all_the_way_down)!)

Installation
-----------

Make a virtualenv, install requirements.txt

Usage
-----
To run the genetic model:
```python
python geneticmonkeys/metamonkeys.py [phrase]
                                     [max_pop]
                                     [mutation_rate]
                                     [birth_rate]
                                     [mortality_rate]
```
To run the metagenetic model:
```python
python geneticmonkeys/geneticmonkeys.py [phrase]
                                        [max_pop]
                                        [mutation_rate]
                                        [mutation_significance]
                                        [birth_rate]
                                        [mortality_rate]
```

Command line arguments can also be set in the appropriate configuration file under `config`.

Contributing
------------
1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

Authors
------------
Yazan Obeidi

Copyright
------------
2016, Yazan Obeidi (GNU GPLv3)
