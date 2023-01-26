# modified version of https://github.com/nickdesaulniers/profitnloss
import numpy as np
import math
import PyOT.Option as ops

#parent_pointer is the Call or Put from Option.py module that this option represents, used for syncing values. could instead generate unique IDS but this seems easier and could be used in future
class Call_Option:
    def __init__(self, strike, premium, parent_pointer, num_shares=100):
        self.strike = float(strike)
        self.premium = float(premium)
        self.num_shares = int(num_shares)
        self.parent_pointer = parent_pointer

    def payoff(self, spot):
        return self.num_shares * (max(spot - self.strike, 0) - self.premium)

    def break_even(self):
        return self.strike + self.premium

    def update_premium(self, new_premium):
        self.premium = float(new_premium)


class Put_Option:
    def __init__(self, strike, premium, parent_pointer, num_shares=100):
        self.strike = float(strike)
        self.premium = float(premium)
        self.num_shares = int(num_shares)
        self.parent_pointer = parent_pointer

    def payoff(self, spot):
        return self.num_shares * (max(self.strike - spot, 0) - self.premium)

    def break_even(self):
        return self.strike - self.premium

    def update_premium(self, new_premium):
        self.premium = float(new_premium)


class Strategy:
    def __init__(self):
        self.longs = []
        self.shorts = []

    #Buy To Open
    def BTO(self, contract):
        self.longs.append(contract)

    #Sell To Open
    def STO(self, contract):
        self.shorts.append(contract)

    #Need contract type (short/long) for longs or shorts, and direction (put/call) for put_option or call_option
    def open(self, contract):
        if contract.type == "LONG" and type(contract) == ops.Call:
            self.longs.append(Call_Option(contract.strike, contract.current_value, contract))
        elif contract.type == "SHORT" and type(contract) == ops.Call:
            self.shorts.append(Call_Option(contract.strike, contract.current_value, contract))
        elif contract.type == "LONG" and type(contract) == ops.Put:
            self.longs.append(Put_Option(contract.strike, contract.current_value, contract))
        elif contract.type == "SHORT" and type(contract) == ops.Put:
            self.shorts.append(Put_Option(contract.strike, contract.current_value, contract))

    def remove_via_parent(self, option):
        for c in self.longs:
            if c.parent_pointer == option:
                self.longs.remove(c)
                return
        for c in self.shorts:
            if c.parent_pointer == option:
                self.shorts.remove(c)
                return

    def strikes(self):
        return sorted(list(set([c.strike for c in self.longs + self.shorts])))

    def payoff_precise(self, spot):
        profit = sum(c.payoff(spot) for c in self.longs)
        loss = sum(c.payoff(spot) for c in self.shorts)
        if math.isinf(profit) and math.isinf(loss):
            # TODO: is this right? shouldn't it be the highest non-inf payoff?
            # TODO: what if there is no non-inf payoff?
            return self.payoff_precise(self.strikes()[-1])
        return profit - loss

    def payoff(self, spot):
        return round(self.payoff_precise(spot), 2)

    def payoffs(self, spots):
        return list(map(self.payoff, spots))

    def net_cost(self):
        credit = sum(c.premium * c.num_shares for c in self.longs)
        debit = sum(c.premium * c.num_shares for c in self.shorts)
        return round(credit - debit, 2)

    def _interesting_spots(self):
        return [0, *self.strikes(), math.inf]

    def break_evens(self):
        roots = []
        spots = self._interesting_spots()
        payoffs = list(map(self.payoff_precise, spots))
        is_inf_payoff = math.isinf(payoffs[-1])
        for i in range(len(spots) - (2 if is_inf_payoff else 1)):
            if ((payoffs[i] > 0) != (payoffs[i + 1] > 0)):
                m = (payoffs[i + 1] - payoffs[i]) / (spots[i + 1] - spots[i])
                c = payoffs[i] - m * spots[i]
                roots.append(round(-c / m, 2))
        if is_inf_payoff:
            y2 = self.payoff_precise(spots[-2] + 1)
            m = y2 - payoffs[-2]
            c = payoffs[-2] - m * spots[-2]
            roots.append(round(-c / m, 2))
        return roots

    def max_loss(self):
        return min(self.payoffs(self._interesting_spots()))

    def max_gain(self):
        return max(self.payoffs(self._interesting_spots()))
    # def plot(self):
    #     strikes = self.strikes()
    #     x = np.array([int(strikes[0] * .9)] + strikes + [int(strikes[-1] * 1.1)])
    #     y1 = np.array(self.payoffs(x))
    #     y2 = np.zeros(len(y1))
    #     plt.plot(x, y1, color='red')
    #     plt.plot(x, y2, color='black')
    #     plt.fill_between(x, y1, y2,  where=y1>0, color='green', alpha=0.2,
    #                      interpolate=True)
    #     plt.fill_between(x, y1, y2,  where=y1<0, color='red', alpha=0.2,
    #                      interpolate=True)
    #     plt.show()
