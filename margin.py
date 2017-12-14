#This program was developed by Hsiao Weng
#Copyright 2015, Common Development and Distribution License
#This code is open source

import os

#delcare the trading class
class trading:
    #trading class constructor takes self and min_max as parameters
    def __init__(self, min_max):
        self.key_level = min_max
        self.mybase = 'USD'
        self.base = ''
        self.quote = ''
        self.price = None
        self.leverage = None
        self.balance = None
        self.output = None
        self.input = None
        self.size = None
        self.size_estimate = None
        self.margin_base = None
        self.pip_value = None
        self.lot_round = 1000
        self.margin_round = 10000
        self.pips_tolerance = 23
        self.quote_ref = .0001
        self.eur_usd_base = None
        self.mypip_value = None
        self.margin_space = None
        self.currencies = ['USD', 'AUD', 'CAD', 'EUR', 'CHF', 'GBP', 'NZD', 'XAU', 'XAG' ] 

    #define clear_screen method
    def clear_screen(self):
        #use cls for windows and clear for linux
        #os.system('cls' if os.name == 'nt' else 'clear')
        pass
    
    #define make method
    def make(self):
        self.get_balance()
        self.set_leverage()

    #define set pairs method; sets the pairs 
    def set_pairs(self):
        #call methods in this order
        self.pairs()
        self.pair_base()
        self.pair_quote()
        self.pair_check()

    #define get_balance method; takes self as parameter
    def get_balance(self):
        #try getting input
        try:
            self.balance = int(input("\nEnter your current balance (no cents): "))
        #catch if error and callback to get_balance
        except Exception:
            print("\n... Invalid.  Enter valid values ...")
            self.get_balance()

    #define set_leverage
    def set_leverage(self):
        try:
            self.leverage = int(input("Enter the leverage ratio: ")) 
        except Exception:
            print("\n... Invalid.  Enter valid values ...")
            self.set_leverage()
            
    #define pairs_write
    def pairs_write(self):
        #open file for writing, (possibly pickle self.base and self.quote)
        try:
            self.output = open('data.txt', 'w')
            self.output.write(base + " " + quote)
            self.output.close()
        #catch if error
        except Exception as erexc:
            print("\n Invalid: \n", erexc)
            print(" ...", end="")
        
    #define pairs method that prints info on screen
    def pairs(self):
        print("\n230-50:\t   EUR/CAD   EUR/GBP   EUR/NZD   EUR/USD   USD/CAD")
        print("250-33:\t   AUD/CAD   AUD/USD")
        print("30-33:\t   EUR/AUD")

    #define method for checking if pairs haven been previously used
    def pair_check(self):
        pair_check = ''
        line = None
        place_holder = None
        #open file for reading; read and pass contents to variable              
        try:
            self.input = open('data.txt', 'r')
            line = self.input.readline()
            place_holder = line.split(' ')
            base_prev = place_holder[0]
            quote_prev = place_holder[1]
            self.input.close()                    
        #catch if error                      
        except Exception as ere:
            print("\n... Invalid: ", ere)
            print(" ...", end='')
            
        if self.base != base_prev and self.quote != quote_prev:
            pair_check += base_prev.strip('\n')
            pair_check += ' '
            pair_check += quote_prev.strip('\n')
            pair_check
            #write values for base and quote to writer; in this case set to 000
            try:
                self.output = open('data.txt', 'w')
                base = self.base.upper()
                quote = self.quote.upper()
                self.output.write(base + ' ' + quote)
                self.output.close()
            #generate error is unable to write
            except Exception as erex:
                 print("... Invalid: \n", erex)
                 print(" ...", end='')
        else:
            pass   
            
        pair_use = self.base.upper() + ' ' + self.quote.upper()               
        if pair_check == pair_use:
            self.clear_screen()
            print("... Used in previous trade.  Use another pair ...")
            #call method set_pairs()
            self.set_pairs()

    #define method to declare base
    def pair_base(self):
        t = False
        #ask for user input of currency base
        try:
            self.base = str(input("Enter the base currency of pair.\n(BASE/quote): "))
            for i in self.currencies:
                if self.base.upper() == i:
                    t = True

            if t == False:
                print("... Invalid.  Enter valid value ...")
                self.pair_base()
            
        #catch if error and callback to pair_base
        except Exception:
            print("... Invalid.  Enter valid value ...")
            self.pair_base()
                                
    #define method to declare qoute                          
    def pair_quote(self):
        t = False
        #ask for user input of currency quote
        try:
            self.quote = str(input("Enter the quote currency of pair.\n(base/QUOTE): "))
            for i in self.currencies:
                if self.quote.upper() == i:
                    t = True
            if t == False:
                print("... Invalid.  Enter valid value ...")
                self.pair_base()
                    
        #catch if error and callback to pair_base
        except Exception:
            print("... Invalid.  Enter valid value ...")
            self.pair_quote()
            
    #define method for calculating the margin                           
    def calculate(self):
        self.clear_screen()
        #declare scope variables
        size_lots = None
        margin_spc = None
        spc_round = 30

        #calculate pip value and space for margin call
        try:
            #use to calculate size and pip value if quote is equal to usd
            if self.mybase.upper() == self.quote.upper():
                #call methods to get values
                self.mybase_is_quote()
                self.margin_spacing()

                #set margin_spc to value from margin_space() times mypip_value
                margin_spc = self.margin_space * self.mypip_value
                margin_spc = margin_spc - (margin_spc % spc_round)

                size_lots = ((self.balance - margin_spc) / self.margin_base) * self.leverage
                #cast size to int
                self.size = int(size_lots)
                self.size_estimate = self.size - (self.size % self.lot_round)
                #set pip value
                self.pip_value = self.quote_ref * self.size_estimate
                #call to print_calculation method
                self.print_calculation()
            elif currencies[3] == self.base.upper() & currencies[2] == self.quote.upper():
                #call to method to get values
                self.myquote_is_cad()
                self.margin_spacing()

                #set margin_spc to value from margin_space() times mypip_value
                margin_spc = self.margin_space * self.mypip_value
                margin_spc = margin_spc - (margin_spc % spc_round)

                size_lots = ((self.balance - margin_spc) / self.eur_usd_base) * self.leverage
                self.size = int(size_lots)
                self.size_estimate = self.size - (self.size % self.lot_round)
                self.pip_value = self.quote_ref * self.size_estimate * self.margin_base
                #call to print_calculation method
                self.print_calculation()
            else:
                self.mybase_is_base()
                self.margin_spacing()

                #set margin_spc to value from margin_space() times mypip_value
                margin_spc = self.margin_space * self.mypip_value
                margin_spc = margin_spc - (margin_spc % spc_round)

                size_lots = ((self.balance - margin_spc) / self.eur_usd_base) * self.leverage
                self.size = int(size_lots)
                self.size_estimate = self.size - (self.size % self.lot_round)
                self.pip_value = self.quote_ref * self.size_estimate * (1/self.margin_base)
                #call to print_calculation method
                self.print_calculation()
        except Exception:
            print("... Invalid.  Enter valid values ...")
            self.calculate()

    #define method for finding the margin space                      
    def margin_spacing(self):
        #declare scope variables
        margin_pips_convert = None
        raw_pips = None
        try:
            raw_pips = abs(self.price - self.key_level)
            margin_pips_convert = int(self.margin_round * raw_pips)
            self.margin_space = int(margin_pips_convert + self.pips_tolerance)
            print("... Stop distance (pips): ", self.margin_space, 
                 " (unadjusted: ", margin_pips_convert, ") ...")
        #generate error if input is invalid and recurse method 
        except Exception:
            print("... Invalid.  Enter valid values ...")
            self.margin_spacing()

    #define mehtod for calculating the lot size if base is usd
    def mybase_is_base(self):
        size_lots = 0.0
        eur_usd_price = 0.0
        
        try:
            self.price = float(input("Enter current price of " + str(self.base.upper()) 
                 + "/" + str(self.quote.upper()) + ": "))
            eur_usd_price = float(input("Enter current price for EUR/USD: "))
        #generate error if input is invalid and recurse method  
        except TypeError:
            print("... Invalid.  Enter valid values ...")

        self.mybase_is_base()                                
        self.margin_base = self.price
        self.eur_usd_price = eur_usd_price

        size_lots = (self.balance / self.eur_usd_price) * self.leverage
        #cast size to int
        self.size = int(size_lots)
        self.mypip_value = self.quote_ref * self.size * (1/self.margin_base)
                        
    #method definition for calculating the lot size if quote is usd                              
    def mybase_is_quote(self):
        size_lots = 0.0
        quote_price = 0.0
        try:
            self.price = float(input("   Enter current price of " + self.base.upper() 
                 + "/" + self.quote.upper() +": "))
            self.margin_base = self.price

            size_lots = (self.balance / self.margin_base) * self.leverage
            #cast size to int
            self.size = int(size_lots)
            self.mypip_value = self.quote_ref * self.size
        #generate error if input is invalid and recurse method  
        except Exception:
            print("... Invalid.  Enter valid values ...")
            self.mybase_is_quote()

    #define method for calculating the lot size if quote is usd 
    def myquote_is_cad(self):
        size_lots = 0.0
        quote_price = 0.0
        eur_usd_price = 0.0

        try:
            self.price = float(input("   Enter current price for " + self.mybase.upper() 
                    + "/" + self.quote.upper() + ": "))
            quote_price = float(input("   Enter current price for " + self.mybase.upper() 
                    + "/" + self.quote.upper() + ": "))
            eur_usd_price = float(input("   Enter current price for EUR/USD: "))

            #set margin_base to 1/(*/CAD)
            self.margin_base = 1/quote_price
            self.eur_usd_base = eur_usd_price

            size_lots = (self.balance / self.eur_usd_base) * self.leverage
            #cast size to int
            self.size = int(size_lots)
            self.mypip_value = self.quote_ref * self.margin_base * self.size           
        #generate error if input is invalid and recurse method  
        except Exception:
            print("... Invalid.  Enter valid values ...")
            self.myquote_is_cad()    
    
    #define method for printing calculations 
    def print_calculation(self):
        if self.size > 0:
            print("... optimium number of units: ", self.size_estimate,
                " (unadjusted: ", self.size, ") ...")
            print("... point in percentage value: %.4f" % self.pip_value)
            print(" ...", end="")
        else:
            print("... Not enough to cover margin space ...")
        
class margin:
    def __init__(self):
         self.ref_min_max = None                      
    def calc_margin(self):
        try:
            self.ref_min_max = float(input("Enter stop loss reference: "))
        except Exception:
            print("... Invalid.  Enter valid values ...")
            self.calc_margin()
    
def main():
    print(".. Margin Caculator 1.0 ...")
    mg = margin()
    mg.calc_margin()
    trade = trading(mg.ref_min_max)
    trade.set_pairs()
    trade.make()
    trade.calculate()

main()
