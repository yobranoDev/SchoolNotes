from InterestRates import Rate

class Payment():
    def __init__(self, time, rate: Rate, amount=1):
        self.time = time
        self.rate = rate
        self.amount = amount

        self.attributes  = [self.time, self.amount, self.rate.rate]

    def time_value(self, n, discount= False):
        return self.amount * self.rate.time_value_factor(n, discount= discount) 






class Cashflow():
    def __init__(self, payments: list) -> None:
        self.payments = payments

    def payments_time_value(self, n):
        import numpy as np
        

        return np.array([payment.time_value(n - payment.time) for payment in self.payments])

    def time_value(self, n, discount= False):
        return self.payments_time_value(n, discount= discount).sum()

    def table(self, raw= True, time_idx= False, time_value= False, at = 0, discount= False):
        import numpy as np
        arr_raw= None
    

        arr_raw = [[*payment.attributes] for payment in self.payments] 
        arr = np.array(arr_raw)
        if raw:
            return arr
        else:
            import pandas as pd
            df = pd.DataFrame(data= arr ,columns = ["time", "amount", "rate"])

            if time_idx:
                df.set_index("time", inplace= True)

            return df





    def get_months_range(start, end, inclusive= [True, True], as_range= False):
        """ Returns the number of months between start-month and end-month and if the months are included or not"""
        months = [ "jan", "feb", "mar",
                   "apr", "may", "jun",
                   "jul", "aug", "sep",
                   "oct", "nov", "dec",]
        start = months.index(start.lower()) if(inclusive[0])else(months.index(start.lower()) + 1)
        end = months.index(end.lower()) if(inclusive[-1])else(months.index(end.lower()) -1 )
        rng = end - start + 1 
        return list(range(start ,end+ 1)) if(as_range)else(rng)


if __name__ == "__main__":

    r = Rate(0.06)

    p0 = Payment(0, r)
    p1 = Payment(1, r)
    p2 = Payment(2, r)

    cf = Cashflow([p0, p1, p2])
    print(cf.table( raw= False).sort_values("time", ascending= False))
