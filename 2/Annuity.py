from InterestRates import Rate


class Annuity():
    def __init__(self, 
                 rate: Rate, 
                 inherit_rate_props= False, 

                 time_span=1,
                 effect_periods=1, 

                 amt= 1, 
                 is_effect_amt = True, 
                 vary_amt=0, 

                 payment_mode= "arrear",
                 
                 differ=0,
                 differ_rate= 0,
                 ):

        """ 
            (The rate, amount, and time are the core attributes when obtaining the time value of an annuity)

            rate -> a rate object with the properties of the annuity's interest rate.
            time_span -> for how long will the payments be recieved.

            inherit_rate_prop -> inherit the effect period of the rate object(if true inherit else use declared values )
            effect_periods -> how many time is the interest rate compounded within one year(one time unit)

            payment_mode -> at what intervals are the payments recieved(at the begining, at the end or continuously over the effect period).

            amt -> the amount paid in one time unit.
            vary_amt -> by what amount are the annuity payments increasing(+ value) or decreasing(- value).
            is_effect_amt -> The amount is paid for each effect period if True. ( The amount is paid once each year but compounded for each effect period if False)

            ----------------
            MAIN CONCEPT
            ----------------
            Given any type of annuity we can convert it from an arrear annuity then find its present value, how the actuarial tables are desingned to be used. 

        """

        self.differ = differ
        self.differ_rate = differ_rate if(differ_rate)else(rate)
        self.rate = rate 
        self.time_span = time_span

        self.is_effect_amt = is_effect_amt
        self.amt  = amt if( self.is_effect_amt)else(amt  * self.effect_periods)
        self.vary_amt = vary_amt

        self.inherit_rate_props = inherit_rate_props
        self.effect_periods = effect_periods if(not inherit_rate_props)else(rate.effect_periods)
        self.payment_mode = payment_mode.lower()
        # annuity properties
        
        
    def annuity(self, n= None ):     
        """ Convets the initialized annuity to an arrear annuity convetible annually(once per unit time). """

        annuity = None
        n = n if(n)else(self.time_span)

    
        if self.vary_amt:
            """ A vary ammount implies that the annuity is a varying annuity. """
            return self.vary_annuity()
        
        # Infinite payments time periods. 
        if self.effect_periods=="inf" or self.payment_mode=="perpetual":
            return self.perpetual()
        
        #  An annuity can be either.
        if self.payment_mode=="arrear":
            annuity = self.arrear(n= n)

        elif(self.payment_mode == "advance"): 
            annuity = self.advance(n= n)
        
        elif(self.payment_mode == "continuous"):
            annuity = self.continuous(n= n)

        return annuity



    
    def time_value(self, value= None,  n=None, differ=0, differ_rate=0, future= False ):
        """ Returns the time value of the annuity. """

        n  = n if(n)else(self.time_span) # how long the payments were made.

        differ = differ if(differ)else(self.differ) # differ time 
        differ_rate = differ_rate if(differ_rate)else(self.differ_rate) # differ rate
        
        amt = (self.amt * self.effect_periods ) if(not self.is_effect_amt)else(self.amt)

    
        annuity_amt = self.annuity(n= n)

        # time value of varying annuity
        if self.vary_amt:

            const_annuity_amt = None
            if self.payment_mode== "advance":
                const_annuity_amt = self.advance()

            elif self.payment_mode == "arrear":
                const_annuity_amt = self.arrear()

            elif self.payment_mode == "continuous":
                const_annuity_amt = self.continuous()

            elif self.payment_mode == "time-continuous":
                const_annuity_amt = 0 # there is no initial amount(self.amt) thus const_annuity  will be 0

            annuity_amt = (amt - self.vary_amt)*const_annuity_amt + self.vary_amt* annuity_amt
            amt = 1 # the amount paid is accounted for.
            

        # finding the present value and future value
        if future:
            # future value
            return amt * (annuity_amt * differ_rate.time_value_factor(n = n + differ))

        else:
            # present value
            return amt  * (annuity_amt * differ_rate.time_value_factor(n = differ, discount= True))




    def arrear(self, n= None ):
        """ Present value of annuity arrear. """
        n  = n if(n)else(self.time_span) # how long the payments were made.

        rate = self.rate.effective_to_norminal(self.effect_periods)
        arrear = (1 - self.rate.time_value_factor(n=n, discount= True)) / rate  # the present value of the annuity.

        return arrear

    def advance(self, n= None):
        """ Converts present value of an annuity arrear to annuity advance. """
        n  = n if(n)else(self.time_span) # how long the payments were made.  

        factor = self.rate.effective_to_norminal(self.effect_periods) / self.rate.discount_rate(effect_periods= self.effect_periods)
        return self.arrear(n= n) * factor

    # Obsolete
    def norminal(self,n = None, effect_periods= None):
        """ Convert present value of an arrear annuity to a annnuity convertible pthly """
        n  = n if(n)else(self.time_span) # how long the payments were made.

        p = effect_periods if(effect_periods)else(self.effect_periods)
        factor = self.rate.rate / self.rate.effective_to_norminal(p)
        return self.arrear(n = n) * factor


    def continuous(self, n= None):
        """ Converts present value of an  annuity arrear to a continuous annuity. """
        n  = n if(n)else(self.time_span) # how long the payments were made.

        factor = self.rate.rate/ self.rate.force_of_interest()
        return self.arrear(n= n) * factor  


    def perpetual(self): 
        """ Returns present value of a perpetural annuity """
        return self.arrear(n= 0)

    def vary_annuity(self, payment_mode= None):
        """ The amount paid per installment is either increasing(+ve vary_amt) or decreasing(-ve vary_amt).  """
        payment_mode = payment_mode if(payment_mode)else(self.payment_mode)
        factor= None

        if payment_mode=="arrear":
            factor = self.rate.rate

        elif payment_mode == "advance":
            factor = self.rate.discount_factor

        elif payment_mode == "continuous":
            """ A constant amount is paid continuously but an increment will be made in the subsequent time unit (annual increments). """
            factor = self.rate.force_of_interest()

        elif payment_mode == "time-continuous":
            """ The amount paid is continuously increasing with time. """
            factor = self.rate.force_of_interest()
            return (self.continuous() - self.time_span * self.rate.time_value_factor(n= self.time_span, discount= True )) / factor

        vary_ann = (self.advance() - self.time_span * self.rate.time_value_factor(n= self.time_span, discount= True)) / factor
        return vary_ann


    def gen_cashflow(self):
        """Returns the annuity as a series of annual payments."""
        import pandas as pd
        df= pd.DataFrame
        from Cashflows import Cashflow, Payment
        payments = [Payment(t, self.rate, amount= self.amt) for t in range(1, self.time_span + 1)]

        return Cashflow(payments)


if __name__ == "__main__":
    from InterestRates import Rate
    from Cashflows import Cashflow


    print("Made by ambition. Made by Brian.")

