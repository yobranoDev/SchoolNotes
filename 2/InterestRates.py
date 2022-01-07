




class Rate:
    def __init__(self, rate, effect_periods =1, accumulation= True, use_norminal_time=False): 
        """ 
            rate -> float value of the interest rate.
            effect_periods -> number of times the rate is converted within one year(a unit time period ). 
            accumulation -> is the rate above an interest or discounting rate.
            norminal -> use the effect_periods effective rate vs using the annual effective rate
        """
        self.effect_periods = effect_periods
        self.raw_rate = rate
        self.accumulation = accumulation
        self.use_norminal_time = use_norminal_time

        # effective interest rates and derivertives
        self.rate = self.normalize(rate) 

        self.accumulation_factor = self.time_value_factor()
        self.discount_factor = self.time_value_factor(discount= True)

        self.foi =self.force_of_interest()

    def __str__(self):
        return str(self.rate)

    def __add__(self, other):
        return self.rate + Rate._value(other)

    def __sub__(self, other):
        return self.rate - Rate._value(other)
     
    
    def __mul__(self, other):
        return self.rate * Rate._value(other)
     
    def __truediv__(self, other):
        return self.rate / Rate._value(other)
     
    def __pow__(self, other):
        return self.rate ** Rate._value(other)
     
    def _value( other):
        if type(other) == Rate:
            return other.rate
        else:
            return other

    def normalize(self, rate): 
        """ Convert any rate to an effective annual interest rate """
        # convert from norminal to effective rate


        if not self.effect_periods == 1:
            rate = self.norminal_to_effective(rate= rate) 
        
        # convert to interest rate
        if not self.accumulation:
            rate = self.discount_to_accumulation(rate)

        return rate 


    def time_value_factor(self, n= 1, rate = None, discount=False, ):
        """ Returns the accumulation factor (discounting if discount= True or n is negative) """
        rate = rate if(rate)else(self.rate)
        return (1 + rate)**n if(not discount)else((1 + rate)**-n )
 


    def norminal_to_effective(self, rate= None):
        """ Returns the effective interest rate given the norminal interst rate. """
        import math
        # force of interest
        rate= rate if(rate)else(self.raw_rate)
        if self.effect_periods=="inf":
            # force of interest is neither for accumulation nor for discounting thus, we assume its always for accumulation.
            self.accumulation = True
            return math.exp(rate) - 1


        # use the effect_periods effective rate 
        if self.use_norminal_time:
            return rate/ self.effect_periods


        # If discount or interest rate was passed in as the rate
        if self.accumulation:
            return ((1 + rate/self.effect_periods)** self.effect_periods) - 1

        else:
            return 1- (1 - rate/self.effect_periods)** self.effect_periods

    def discount_to_accumulation(self, rate=None):
        """ Retruns the interest rate from discount rate """
        rate = rate if(rate)else(self.rate)
        return rate/(1-rate) 

    def effective_to_norminal(self, effect_periods, rate= None, time_span= 1 ):
        """ Returns the effective interst rate given the norminal rate compounded pthly. """
        # time_span -> used when assuming for accumulation factor is used as rate
        rate = rate if(rate)else(self.rate)
        
        # Obtaining the force of interest.
        if effect_periods== "inf":
            return self.force_of_interest(rate= rate, n= time_span)
            
        return effect_periods*((1 + rate)**(time_span/effect_periods ) - 1)
    


    def discount_rate(self, rate= None, effect_periods=1):
        """ Retruns the discounting rate given the rate of interest. """
        rate = rate if(rate)else(self.rate)
        return effect_periods*(1 - self.time_value_factor(discount= True)**(1/effect_periods))


    def force_of_interest(self, rate= None, n=1):
        """ Returns the force of interest given the effective interest rate. """
        import math
        rate = rate if(rate)else(self.rate)
        return math.log(self.time_value_factor(rate= rate, n = n))

        





if __name__ == "__main__":
    r = Rate(0.02)
    print(r / r)




