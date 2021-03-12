import numpy as np
import datetime

USD_notional = 10000000;
USDJPY = 107
JPY_notional = 1070000000
row_count = 12;

float_rate = np.zeros(row_count ,dtype=np.float64);
payment_dates = np.zeros(row_count,dtype=object);
float_rate = np.zeros(row_count ,dtype=np.float64);
JPY_rate = np.empty(row_count,dtype=np.float64);
USD_rate = np.empty(row_count,dtype=np.float64);
JPY_FV_factor = np.empty(row_count,dtype=np.float64);
USD_FV_factor = np.empty(row_count,dtype=np.float64);
Forward_rate = np.empty(row_count,dtype=np.float64);
JPY_payment = np.empty(row_count,dtype=np.float64);
USD_payment = np.empty(row_count,dtype=np.float64);
PV_JPY_payment = np.empty(row_count,dtype=np.float64);
PV_USD_payment = np.empty(row_count,dtype=np.float64);
time_in_years = np.zeros(row_count,dtype=np.float64);

#Allocate
payment_dates[0] = np.datetime64(datetime.date.today());
time_in_years[0] = 0;
JPY_rate.fill(0.01);
USD_rate.fill(0.05)
JPY_payment[0]  = -JPY_notional
USD_payment[0] = USD_notional

#######Main code
for i in range(1,row_count-1):
    payment_dates[i] = payment_dates[i - 1] + np.timedelta64(365,'D')
    time_in_years[i] = (payment_dates[i]- payment_dates[0])/np.timedelta64(365,'D');
    JPY_payment[i] = JPY_rate[i] * JPY_notional
    USD_payment[i] = -USD_rate[i] * USD_notional

## Fill last row
payment_dates[row_count - 1] = payment_dates[row_count - 2];
time_in_years[row_count - 1] = time_in_years[row_count - 2];
JPY_FV_factor = ( 1 + JPY_rate)**time_in_years
USD_FV_factor = ( 1 + USD_rate)**time_in_years
JPY_payment[row_count - 1] =  JPY_notional
USD_payment[row_count - 1] = -USD_notional

#Vectorized
Forward_rate = USDJPY*JPY_FV_factor/USD_FV_factor
PV_JPY_payment = JPY_payment/JPY_FV_factor
PV_USD_payment = USD_payment/USD_FV_factor

print('________________________________________________________________________________________________________________________________________________________________________')

row = ['|Payment_date |','JPY_rate |', 'USD_rate |','Maturity |','JPY_FV_factor |','USD_FV_Factor |','Forward_Rate |','JPY_Payment |','USD_Payment |','PV_JPY_Payment |','PV_USD_Payment |']
print("{: >10} {: >10} {: >10} {: >10} {: >10} {: >10} {: >10} {: >10} {: >10} {: >15} {: >15}".format(*row))
print('________________________________________________________________________________________________________________________________________________________________________')

for i in range(0,row_count):
    row = [payment_dates[i],round(JPY_rate[i],4), round(USD_rate[i],4),round(time_in_years[i],4),round(JPY_FV_factor[i],4),round(USD_FV_factor[i],4),round(Forward_rate[i],4),round(JPY_payment[i],4),round(USD_payment[i],4),round(PV_JPY_payment[i],4),round(PV_USD_payment[i],4)]
    print("{: >10} {: >10} {: >15} {: >13} {: >10} {: >14} {: >20} {: >15} {: >15} {: >15} {: >15}".format(*row))


