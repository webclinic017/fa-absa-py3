import traceback
import acm

testtrade = acm.FTrade[58716235]

ael_variables = []
def ael_main(something):
    try:
        testtrade.o()
    except Exception as e:
        print(e)
        traceback.print_exc()
        
        
