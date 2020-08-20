#! /usr/local/bin/python3
import math


# 等额本息: (贷款本金 * 月利率 * (1 ＋ 月利率) ^ 还款月数) / ((1 + 月利率) ^ 还款月数 - 1))
def monthly_repayment(principal, yearly_rate, months):
    monthly_rate = yearly_rate / 12
    compound_rate = (1 + monthly_rate) ** months
    return principal * monthly_rate * compound_rate / (compound_rate - 1)


def repayment_months(principal, yearly_rate, repayment):
    monthly_rate = yearly_rate / 12
    a = repayment / (principal * monthly_rate)
    compound_rate = a / (a - 1)
    return math.log(compound_rate, 1 + monthly_rate)


def main():
    repayment = monthly_repayment(100000, 0.08, 12)
    print(repayment)
    print(repayment_months(100000, 0.08, repayment) / 12)
    print(repayment_months(600000 - 180000, 0.08, 3100) / 12)
    print(repayment_months(350000 - 105000, 0.035, 1100) / 12)


if __name__ == "__main__":
    main()
