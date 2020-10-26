import numpy as np
import matplotlib.pyplot as plt
import math

Fs = 1000
Ts = 1 / Fs


def simulate(Ns, t, input_signal, idx, output_order, input_order, a, b):
    """plot output signal and state variables and compute state space representation

        Args:
            Ns: number of samples of the signal
            t: time vector
            input_signal: vector of input signal values with respect to t
            idx: index of element in input vector where value rises when input is unit impulse
             or unit step
            output_order: the highest order of output signal
            input_order: the highest order of input signal
            a: list of coefficients of output signal
            b: list of coefficients of input signal

        Returns:
            vector of differentiated signal
    """

    b.extend([0 for _ in range(output_order - input_order)])

    # compute RHS of input/output eqn
    u = computing_input_derivatives(b, input_order, input_signal, Ns)

    # compute output signal numerically
    y = np.zeros(Ns)
    coefficients = get_coefficients(a, output_order)
    out_coeff = output_coefficient(a, output_order)

    # calculate input response assuming zero initial conditions
    for k in range(output_order, Ns):
        y[k] = u[k] / out_coeff
        for i in range(1, output_order + 1):
            y[k] += (y[k - i] * coefficients[i - 1]) / out_coeff

    temp1 = y[idx]
    y[idx] = y[idx + 1]

    if idx == output_order:
        temp2 = y[:idx]
        y[:idx] = y[idx]

    # plot input signal
    plt.figure()
    plt.title('Plot of Input Signal: u(t)')
    plt.xlabel('t')
    plt.ylabel('u(t)')
    plt.grid(True)
    plt.plot(t, input_signal)

    # plot output signal
    plt.figure()
    plt.title('Plot of Output Signal: y(t)')
    plt.xlabel('t')
    plt.ylabel('y(t)')
    plt.grid(True)
    plt.plot(t, y)

    if idx == output_order:
        y[:idx] = temp2

    # calculate new coefficients of input (Beta) to eliminate input derivatives
    beta = []
    for i in range(output_order + 1):
        temp = b[output_order - i]
        for j in range(i - 1, -1, -1):
            temp -= a[output_order + j - i] * beta[j]
        beta.append(temp / a[output_order])

    # calculate matrix A
    A = np.zeros((output_order, output_order))
    for i in range(output_order - 1):
        A[i][i + 1] = 1
    for i in range(output_order):
        A[output_order - 1][i] = -1 * a[i] / a[output_order]

    # calculate matrix B
    B = np.array([beta[i] for i in range(1, output_order + 1)])

    # calculate matrix C
    C = np.zeros((1, output_order))
    C[0][0] = 1

    # matrix D
    D = [beta[0]]

    y[idx] = temp1
    # calculate state variables
    state_x = [y - beta[0] * input_signal]
    for i in range(1, output_order):
        state_x.append(differentiate(state_x[i - 1], 1, Ns) - beta[i] * input_signal)

    # plot state variables
    for i, state in enumerate(state_x):
        plt.figure()
        plt.title('Plot of State Variable:x{}(t)'.format(i + 1))
        plt.xlabel('t')
        plt.ylabel('x{}(t)'.format(i + 1))
        plt.grid(True)
        plt.plot(t, state)

    return "A = " + np.array2string(A, precision=3, suppress_small=True) + "\tB = " + \
           np.array2string(B, precision=3, suppress_small=True) + "\nC = " +\
           np.array2string(C, precision=3, suppress_small=True) + "\tD = " + str(D)


def get_coefficients(a, order):
    """Get coefficients of order points backward of the output signal

        Args:
            a: list of coefficient of output derivatives
            order: order of LTI system

        Returns:
            A list of coefficients of order points backward of the output signal
    """

    # declaring empty list of coefficients
    coefficient = []
    for point_back in range(1, order + 1):
        temp_coeff = 0
        # formula derived from substituting derivatives of output signal in input/output eqn
        for i in range(point_back, order + 1):
            temp_coeff += (math.factorial(i)/(math.factorial(i - point_back)*math.factorial(point_back))) * \
                          a[i] / (Ts**i)
        coefficient.append(temp_coeff * ((-1) ** (point_back + 1)))

    return coefficient


def output_coefficient(a, order):
    """Compute the coefficient of output signal after substituting derivatives of output signal in input/output eqn

        Args:
            a: list of coefficient of output derivatives
            order: order of LTI system

        Returns:
            The computed coefficient
    """

    return sum([a[i]/(Ts**i) for i in range(order + 1)])


def computing_input_derivatives(b, order, input_signal, Ns):
    """Sum the input signal and its derivatives numerically

        Args:
            b: list of coefficients of input derivatives
            order: order of input derivatives
            input_signal: vector of numerical values of input signal along time t
            Ns: number of samples of the signal


         Returns:
            Summation of the input signal and its derivatives
    """

    u = b[0] * input_signal
    for i in range(1, order + 1):
        # To optimize performance and not to calculate derivatives if its coefficient equal zero
        if b[i] == 0:
            continue
        u += b[i] * differentiate(input_signal, i, Ns)

    return u


def differentiate_one_time(signal, order, Ns):
    """Compute signal derivative numerically by using two points backward formula

        Args:
            signal: vector of numerical values of the signal along time t
            order: order of differentiation. When differentiate signal` to signal`` then order is 2
            Ns: number of samples of the signal

        Returns:
            vector of differentiated signal
    """

    # initialize differentiated signal
    signal_ = np.zeros(Ns)
    for i in range(order, Ns):
        signal_[i] = (signal[i] - signal[i - 1]) / Ts

    return signal_


def differentiate(signal, order, Ns):
    """differentiate signal order times

        Args:
            signal: vector of numerical values of the signal along time t
            order: number of times the signal be differentiated
            Ns: number of samples of the signal

        Returns:
            vector of differentiated signal
    """

    signal_ = signal
    for i in range(order):
        signal_ = differentiate_one_time(signal_, i + 1, Ns)

    signal_[:order] = signal_[order]
    return signal_
