# LTI-Solver

LTI-Solver is a python script that solves linear time-invariant systems up to the tenth degree.

## Abstract

Linear time-invariant systems (LTI systems) are types of systems used in signals and
systems that are both linear and time-invariant. Linear systems are systems whose outputs for a
linear combination of inputs are the same as a linear combination of individual responses to those
inputs. Time-invariant systems are systems where the output does not depend on when the input
was applied. These properties make LTI systems easy to represent and understand graphically.

LTI systems are superior to simple state machines for representation because they have
more memory. LTI systems, unlike state machines, have a memory of past states and have the
ability to predict the future. LTI systems are used to predict long-term behavior in a system. So,
they are often used to model systems like power plants. Another important application of LTI
systems is electrical circuits. These circuits made up of inductors, transistors, and resistors, are the
basis upon which modern technology is built.

## Usage

This system solves linear time-invariant systems in the form of:

![alt text](https://drive.google.com/file/d/1ZXODKQH78LUBaEnh4V0RXm-HcIpDbRJB/view?usp=sharing/)

where m <= n.

It’s implemented by using python 3.8, NumPy, Matplotlib, and Tkinter modules. It has the following
features:
1. User determines the time interval of the solution/graphs.
2. Determine the input signal (u) between the available options (unit step / unit impulse / sin
/ cos / exponential).
3. User determines the input and output orders up to the tenth order.
4. User determines the step/impulse time if the input signal is unit-step or unit-impulse.
5. User determines a’s and b’s coefficients.
6. Plot the output signal (y) with the assumption of zero initial conditions.
7. Plot system states.
8. Computes the state space representation matrices (A, B, C, D) of the system.


## Mathematical Background
There are several methods to approximate the first derivative at a point using the values at two or
more of its neighboring points. These points can be chosen to the left, to the right, or on both sides
of the point at which the first derivative is to be approximated. The method chosen is Two-Point.

* For more information and examples [click here](https://drive.google.com/file/d/15MS7B7o_O4Ac3zQMvDtpvqLP0wP2womw/view?usp=sharing)