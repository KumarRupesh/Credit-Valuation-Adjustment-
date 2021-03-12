import numpy as np
import datetime

swap_notional = 1e7;
swap_rate = .0683736171278209;
row_count = 22;

payment_dates = np.zeros(row_count,dtype=object);
# initialize
payment_dates[0] = np.datetime64(datetime.date.today());
payment_dates[1] = np.datetime64(datetime.date.today()) + np.timedelta64(182,'D')
float_rate = np.array([0.06 ,0.060,0.061,0.063,0.064,0.066,0.068,0.069,0.071,0.073,0.075,0.077,0.079,0.081,0.083,0.085,0.088,\
                0.090,0.093,0.095,0.098,0.098])
# allocate
year_fraction = np.zeros(row_count,dtype=np.float64);
time_in_years = np.zeros(row_count,dtype=np.float64);

# initialize
year_fraction[0] = 0;
time_in_years[0] = 0;

# allocate
FV_factor = np.zeros(row_count,dtype=np.float64);
df = np.zeros(row_count,dtype=np.float64);

# initialize
FV_factor[0] = 1.0;
df[0] = 1.0;

#allocate
FV_float_payment =np.zeros(row_count,dtype=np.float64);
PV_float_payment = np.zeros(row_count,dtype=np.float64);

# initialize
FV_float_payment[0] = -swap_notional;
PV_float_payment[0] = -swap_notional;

# allocate
term_rate = np.zeros(row_count,dtype=np.float64);
fixed_payment = np.zeros(row_count,dtype=np.float64);
PV_fixed_payment = np.zeros(row_count,dtype=np.float64);

# initialize
term_rate[0] = float_rate[0];
fixed_payment[0] = swap_notional;
PV_fixed_payment[0] = swap_notional;

#######Main code

for i in range(1,row_count - 1):
    payment_dates[i+1] = payment_dates[i-1] + np.timedelta64(365,'D')
    year_fraction[i] = (payment_dates[i]- payment_dates[i-1])/np.timedelta64(1,'D');
    time_in_years[i] = (payment_dates[i]- payment_dates[0])/np.timedelta64(1,'D');
    
year_fraction = year_fraction/365;
time_in_years = time_in_years/365;


for i in range(1,row_count - 1):
    FV_float_payment[i] = swap_notional*year_fraction[i]*float_rate[i-1];
    FV_factor[i] = FV_factor[i-1]*(1+year_fraction[i]*float_rate[i-1]);
    df[i] = 1/FV_factor[i];
    PV_float_payment[i] = df[i]*FV_float_payment[i];
    fixed_payment[i] = -swap_notional*year_fraction[i]*swap_rate;
    PV_fixed_payment[i] = df[i]*fixed_payment[i];
    term_rate[i] = (FV_factor[i] - 1) / time_in_years[i];

#handle final row separately
payment_dates[row_count - 1] = payment_dates[row_count - 2];
year_fraction[row_count-1] = 0;
time_in_years[row_count - 1] = time_in_years[row_count - 2];
FV_factor[row_count-1] = FV_factor[row_count - 2];
df[row_count-1] = df[row_count - 2];
FV_float_payment[row_count-1] = swap_notional;
PV_float_payment[row_count-1] = df[row_count-1]  * FV_float_payment[row_count-1];
term_rate[row_count-1] = term_rate[row_count-2];
fixed_payment[row_count-1] = -swap_notional;
PV_fixed_payment[row_count-1] = df[row_count-1] * fixed_payment[row_count-1];

#Print Output
print('________________________________________________________________________________________________________________________________________________________________________')

row = ['|Payment_date |','float rate |', 'year fraction |','Maturity |','FV_factor |','Discount_Factor |','FV_float_payment |','PV_float_payment |','term_rate |','fixed_payment |','PV_fixed_payment |']
print("{: >10} {: >10} {: >10} {: >10} {: >10} {: >10} {: >10} {: >10} {: >10} {: >15} {: >15}".format(*row))
print('________________________________________________________________________________________________________________________________________________________________________')

for i in range(0,row_count):
    row = [payment_dates[i],round(float_rate[i],4), round(year_fraction[i],4),round(time_in_years[i],4),round(FV_factor[i],4),round(df[i],4),round(FV_float_payment[i],4),round(PV_float_payment[i],4),round(term_rate[i],4),round(fixed_payment[i],4),round(PV_fixed_payment[i],4)]
    print("{: >10} {: >10} {: >15} {: >13} {: >10} {: >14} {: >20} {: >15} {: >15} {: >15} {: >15}".format(*row))


