#! /usr/local/bin/python3


class Payroll:
    @staticmethod
    def calculate_tax(amount):
        ranks = [(0, 3, 0)
            , (36000, 10, 2520)
            , (144000, 20, 16920)
            , (300000, 25, 31920)
            , (420000, 30, 52920)
            , (660000, 35, 85920)
            , (960000, 45, 181920)]
        rate = delta = 0
        for rank in ranks:
            if amount < rank[0]:
                break
            rate = rank[1]
            delta = rank[2]
        return round(amount * rate / 100.0 - delta, 2)

    def __init__(self, y2d_grand, y2d_iit, earnings, deductions, asd, deductions2):
        """
        :param y2d_grand:   Year To Date Grand Total
        :param y2d_iit:     Year To Date IIT
        :param earnings:    Total Earnings Before Tax
        :param deductions:  Total Deductions Before Tax
        :param asd:         Additional Special Deduction
        :param deductions2: Total Deductions After Tax
        """
        tax_exemption = 5000
        self.y2d_grand = earnings - tax_exemption - deductions - asd + y2d_grand
        self.y2d_iit = self.calculate_tax(self.y2d_grand)
        self.itt = round(self.y2d_iit - y2d_iit, 2)
        self.earnings = earnings - deductions - self.itt - deductions2

    def __str__(self):
        return 'y2d_grand({}, y2d_iit({}), itt({}), earnings({})'\
            .format(self.y2d_grand, self.y2d_iit, self.itt, self.earnings)


def main():
    """
    payroll = Payroll(0, 0, 30000, 3000, 0, 0)
    print(payroll)
    payroll = Payroll(payroll.y2d_grand, payroll.y2d_iit, 32000, 4000, 0, 0)
    print(payroll)
    payroll = Payroll(payroll.y2d_grand, payroll.y2d_iit, 35000, 6000, 0, 0)
    print(payroll)
    """
    earnings = 30000
    deductions = 5000
    asd = 2000
    deductions2 = round(earnings * 0.05) - 10   # PFund - One Child Fee
    payroll = ''
    for i in range(0, 12):
        if not payroll:
            payroll = Payroll(0, 0, earnings, deductions, asd, deductions2)
        else:
            payroll = Payroll(payroll.y2d_grand, payroll.y2d_iit, earnings, deductions, asd, deductions2)
        print('{:2d}: '.format(i + 1) + str(payroll))


if __name__ == "__main__":
    main()
