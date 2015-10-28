##Assignment 6 for CSCI 3202 - Artificial Intelligence.
####Assignment Description
This assignment focuses on Bayes's Networks and the associated probability.
In this Bayes Network, the probability of a person being a smoker or being exposed to pollution is given. Conditioned on these is the probability of that person having cancer. Conditioned on the person having cancer is the probability of the person having "soft evidence", a positive XRay or dyspnoea.
####Assignment Implementation
This program can handle four functions: setting the prior probability for pollution or smoker, returning the marginal probability distribution for a variable, calculating the joint probability for up to 4 variables, and returning the conditional probability of a variable given 3 conditionals.
- To set the prior, the command is: ```-pP.80```, where P is the variable you want to set (either P or S) and .8 is the new probability you wish to assign to it.
- To calculate the marginal probability, the command is: ```-mD```, where D is the variable you'd like to receive the marginal probability for.
- To calculate, the joint probability, the command is ```-jDPS``` or ```-jdps```. In ```-jDPS```, the joint distribution for the given variables is returned, while in ```jdps``` the joint probability for the three variables is given.
- To calculate the conditional probability, the command is ```-g"c|dps"```. This will calculate the conditional probability of cancer given dyspnoea, pollution, and smoker. The conditional probability cannot handle more than three conditonals. It also can't handle calculating the conditional probability for joint variables (i.e. ```-g"cd|xsp"```). Furthermore, it expects arguments of lowercase letters (while other commands can also accept uppercase letters).
- To denote that a variable is False (as opposed to True), the expected syntax is ```~``` before the variable name.
