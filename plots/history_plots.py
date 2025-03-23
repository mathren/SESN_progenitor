
import numpy as np
import matplotlib.pyplot as plt
import mesa_reader 
import scipy as spp
from matplotlib import rc
import pandas as pd
import os
import subprocess
from scipy import integrate



G = 6.67430e-8 # Universal gravitation constant in cgs
mu_sun = 1.3271244e26
Lsun = 3.828e33
Msun = mu_sun / G
Rsun = 6.957e10
sectoyr = 24*60*60*365.25
erg_to_mev = 624150.64799632




def np_array(shape):
    return np.array(shape, dtype=object)


'''We calculate the total gravitational potential energy of the system at ZAMS and final fate'''
def U_grav(M1,R1):
    val = -(3./5.)*G*(M1*Msun)**2 / (R1*Rsun)
    return val




# In[6]:


# sol, the four histories to read in

file_names = ['15m1_0.0beta_p20','15m1_0.3beta_p20','15m1_0.5beta_p20','15m1_0.7beta_p20','15m1_1.0beta_p20','15m1_0.0beta_p25','16m1_0.0beta_p20','20m1_0.0beta_p20','20m1_0.0beta_p25','80_single']


pulse_sol = []
ppisn_sol = []


log_star_age_sec = []
log_Teff = []
log_L = []
log_Lneu = []
log_Lnuc = []
compactness_parameter = []

log_center_T = []
log_center_Rho = []
star_age = []
log_R = []
center_ne20 = []
center_entropy = []

center_o16 = []
center_ni56 = []
center_fe56 = []
center_si28 = []
center_c12 = []
center_he4 = []
center_h1 = []
center_N2 = []
mass_conv_core = []
star_mass = []
m_below_vesc = []
log_dt = []

#for analyizing he-flashes and thermal pulses
model_number = []
log_LH = []
log_LHe = []



# add reactions and stuff



log_Lneu_beta = []
log_Lneu_invbeta = []

log_Lneu_pair = []
log_Lneu_plas = []
log_Lneu_phot  = []
log_Lneu_brem = []
log_Lneu_reco  = []

log_Lneu_nonnuc = []
log_Lneu_nuc = []
center_ye = []

mu4 = []
m4 = []
           
co_core_mass = []
one_core_mass = []
fe_core_mass = []
log_total_gravitational_energy = []

'''loop through files and stoore data variables for each file'''

for i in file_names:
    print ('i =',i)
    # importing files from history.data in each model folder
    file_name1 = str(i)
    location = "data/" + file_name1 + "/LOGS1/history.data"
    print ('importing files from model :',file_name1)
    #file_path1 = main_file + "/" + file_name1 + "/LOGS/history.data"
    model = mesa_reader.MesaData(file_name = location, file_type=None)

    #store history.data arrays as
    model_number.append(model.data('model_number'))
    log_R.append(model.data('log_R'))
    log_Teff.append(model.data('log_Teff'))
    log_L.append(model.data('log_L'))
    log_Lneu.append(model.data('log_Lneu'))
    log_Lnuc.append(model.data('log_Lnuc'))
    log_LH.append(model.data('log_LH'))
    log_LHe.append(model.data('log_LHe'))
    log_center_Rho.append(model.data('log_center_Rho'))
    star_age.append(model.data('star_age'))
    log_dt.append(model.data('log_dt'))
    center_c12.append(model.data('center_c12'))
    center_o16.append(model.data('center_o16'))
    # center_si28.append(model.data('center_si28'))
    # center_fe56.append(model.data('center_fe56'))
    center_he4.append(model.data('center_he4'))
    center_h1.append(model.data('center_h1'))
    center_entropy.append(model.data('center_entropy'))

    #center_N2.append(model.data('center_N2'))
    mass_conv_core.append(model.data('mass_conv_core'))
    star_mass.append(model.data('star_mass'))
    log_center_T.append(model.data('log_center_T'))
    #m_below_vesc.append(model.data('M_below_vesc'))

    log_Lneu_nonnuc.append(model.data('log_Lneu_nonnuc'))
    log_Lneu_nuc.append(model.data('log_Lneu_nuc'))
    center_ye.append(model.data('center_ye'))

    co_core_mass.append(model.data('co_core_mass'))
    one_core_mass.append(model.data('one_core_mass'))
    fe_core_mass.append(model.data('fe_core_mass'))

        
    log_star_age_sec.append(model.data('log_star_age_sec'))
    log_total_gravitational_energy.append(model.data('log_total_energy'))
    # mu4.append(model.data('mu4'))
    # m4.append(model.data('m4'))
#    compactness_parameter.append(model.data('compactness_parameter'))

# '''store all data variables as numpy arrays, (better for calculation)'''
# model_number = np_array(model_number)
log_LH = np_array(log_LH)
log_LHe = np_array(log_LHe)
log_total_gravitational_energy = np_array(log_total_gravitational_energy)
log_R = np_array(log_R)
log_Teff = np_array(log_Teff)
log_dt = np_array(log_dt)
log_L = np_array(log_L)
log_Lneu = np_array(log_Lneu)
log_Lnuc = np_array(log_Lnuc)
log_center_T = np_array(log_center_T)
log_center_Rho = np_array(log_center_Rho)
star_age = np_array(star_age)
center_c12 = np_array(center_c12)
center_o16 = np_array(center_o16)
# center_si28 = np_array(center_si28)
# center_fe56 = np_array(center_fe56)
center_entropy = np_array(center_entropy)

center_he4 = np_array(center_he4)
center_h1 = np_array(center_h1)
#center_N2 = np_array(center_N2)
mass_conv_core = np_array(mass_conv_core)
one_core_mass = np_array(one_core_mass)
co_core_mass = np_array(co_core_mass)
fe_core_mass = np_array(fe_core_mass)

star_mass = np_array(star_mass)
#compactness_parameter = np_array(compactness_parameter)
#m4 = np_array(m4)
#mu4 = np_array(mu4)


log_Lneu_nonnuc = np_array(log_Lneu_nonnuc)
log_Lneu_nuc = np_array(log_Lneu_nuc)
center_ye = np_array(center_ye)


log_star_age_sec = np_array(log_star_age_sec)












'''Let's find the ZAMS for each model, we do this by finding when Lnuc/L ~> 0.99, a good estimate '''
ZAMS_marker = []
for i in range(0,len(star_mass)):
    check_val = log_Lnuc[i]-log_L[i]
    check_val = 10**check_val
    value = np.argmax(check_val>=0.99999)    
#     value = np.argmax(check_val>0.99)
    ZAMS_marker.append(value)

ZAMS_marker= np_array(ZAMS_marker)
R = 10**log_R




star_initial_mass = []
for i in range(0,len(star_mass)):
    star_initial_mass.append(star_mass[i][0])
star_initial_mass = np_array(star_initial_mass)




######-------------------------------------------------------------------
######-------------------------------------------------------------------
######-------------------------------------------------------------------





# In[7]:
# Calculate log_age and age for each model in sol based on log_dt, summing backwards
log_age = []
age = []

for i in range(len(file_names)):
    age_val = 0
    store_age = []
    store_log_age = []
    for j in reversed(range(len(log_dt[i]))):  # Start summing from the end
        age_val += 10**log_dt[i][j]  # Accumulate age backwards using log_dt
        log_age_val = np.log10(age_val)  # Calculate log_age directly
        store_age.append(age_val)
        store_log_age.append(log_age_val)

    # Reverse the arrays since we accumulated backwards
    store_age.reverse()
    store_log_age.reverse()

    age.append(store_age)        # Store the calculated age for each model
    log_age.append(store_log_age)  # Store log_age for each model

# Now, calculate the time to core collapse for each model using store_log_age
tcc = []
log_tcc = []

for i in range(len(file_names)):
    array1 = 10**np.array(log_age[i], dtype='float64')  # Use log_age from the loop above
    endval = 10**log_age[i][-1]  # The last value in log_age is the end value
    print(endval)
    value10 = -(endval - array1) * sectoyr / 3600  # Convert years to seconds, then to hours
    tcc.append(value10)
    log_tcc.append(np.log10(value10))  # Store the logarithmic time to core collapse

# Convert lists to arrays
tcc = np_array(tcc)
log_tcc = np_array(log_tcc)






# In[8]:


erg_to_mev = 624150.64799632

# for smoothing 

mean_kernel100 = np.full((50,), 1/50)

def conv(input_array):
    value =  np.convolve(input_array, mean_kernel100,mode='same')
    return (value)






# In[9]:


# colors
c1 = plt.cm.tab20(0)
c2 = plt.cm.tab20(1)
c3 = plt.cm.tab20(2)
c4 = plt.cm.tab20(3)
c5 = plt.cm.tab20(4)
c6 = plt.cm.tab20(5)
c7 = plt.cm.tab20(6)
c8 = plt.cm.tab20(7)
c9 = plt.cm.tab20(8)
c10 = plt.cm.tab20(9)
c11 = plt.cm.tab20(10)
c12 = plt.cm.tab20(11)
c13 = plt.cm.tab20(12)
c14 = plt.cm.tab20(13)
c15 = plt.cm.tab20(14)
c16 = plt.cm.tab20(15)
c17 = plt.cm.tab20(16)
c18 = plt.cm.tab20(17)
c19 = plt.cm.tab20(18)
c20 = plt.cm.tab20(19)



# In[58]:





# In[88]:


# Plotting
fig1 = plt.figure(figsize=(24,24))

plt.style.use('mesa.mplstyle')


'column 1'
ax2 = fig1.add_subplot(221) # hr
ax4 = fig1.add_subplot(223) # hr


'column 2'

ax1 = fig1.add_subplot(222) # rho-T
ax3 = fig1.add_subplot(224) # rho-T














'''here is top left panel'''


ax2.plot(log_Teff[0], log_L[0], label=r'15m1_0.0beta_p20', linewidth=5, color=c1, linestyle='-', zorder=6)
ax2.plot(log_Teff[1], log_L[1], label=r'15m1_0.3beta_p20', linewidth=5, color=c3, linestyle='-', zorder=10,alpha = 0.9)
ax2.plot(log_Teff[2], log_L[2], label=r'15m1_0.5beta_p20', linewidth=5, color='darkred', linestyle='-', zorder=10,alpha = 0.9)
ax2.plot(log_Teff[3], log_L[3], label=r'15m1_0.7beta_p20', linewidth=5, color='black', linestyle='-', zorder=10,alpha = 0.9)
ax2.plot(log_Teff[4], log_L[4], label=r'15m1_1.0beta_p20', linewidth=5, color='darkblue', linestyle='--', zorder=10,alpha = 0.9)







ax2.set_xlabel(r'log $T_\textrm{eff}$ [K]', fontsize=40)
ax2.set_ylabel(r'log L [L$_{\odot}$]', fontsize=40)


# ax2.text(7e5,5.3,r'C', fontsize = 30,ha = 'center')
# ax2.text(4e4,5.8,r'Ne ', fontsize = 30,ha = 'center')
# ax2.text(2e3,7.25,r'O', fontsize = 30,ha = 'center')

# ax2.text(15,7.5,r'Si', fontsize = 30,ha = 'center')


ax2.invert_xaxis()

# ax2.set_xlim([5e6,1e-6])
# ax2.set_ylim(2,16)

ax2.legend(fontsize = '24',ncol = 1)














'''here is bottom left panel'''

# file_names = ['15m1_0.0beta_p20','15m1_0.3beta_p20','15m1_0.5beta_p20',
#               '15m1_0.7beta_p20','15m1_1.0beta_p20','15m1_0.0beta_p25','16m1_0.0beta_p20',
#               '20m1_0.0beta_p20','20m1_0.0beta_p25','80_single']

ax4.plot(log_Teff[0], log_L[0], label=r'15m1_0.0beta_p20', linewidth=5, color=c1, linestyle='-', zorder=6)
ax4.plot(log_Teff[5], log_L[5], label=r'15m1_0.0beta_p25', linewidth=5, color=c3, linestyle='-', zorder=10,alpha = 0.9)
ax4.plot(log_Teff[6], log_L[6], label=r'16m1_0.0beta_p20', linewidth=5, color='darkred', linestyle='-', zorder=10,alpha = 0.9)
ax4.plot(log_Teff[7], log_L[7], label=r'20m1_0.0beta_p20', linewidth=5, color='black', linestyle='-', zorder=10,alpha = 0.9)
ax4.plot(log_Teff[8], log_L[8], label=r'20m1_0.0beta_p25', linewidth=5, color='darkblue', linestyle='--', zorder=10,alpha = 0.9)
ax4.plot(log_Teff[9], log_L[9], label=r'80_wide_orbit', linewidth=5, color='orchid', linestyle='--', zorder=10,alpha = 0.9)







ax4.set_xlabel(r'log $T_\textrm{eff}$ [K]', fontsize=40)
ax4.set_ylabel(r'log L [L$_{\odot}$]', fontsize=40)


# ax4.text(7e5,5.3,r'C', fontsize = 30,ha = 'center')
# ax4.text(4e4,5.8,r'Ne ', fontsize = 30,ha = 'center')
# ax4.text(2e3,7.25,r'O', fontsize = 30,ha = 'center')

# ax4.text(15,7.5,r'Si', fontsize = 30,ha = 'center')


ax4.invert_xaxis()

# ax4.set_xlim([5e6,1e-6])
ax4.set_ylim(4.,6.5)

ax4.legend(fontsize = '24',ncol = 1, loc = 'center', bbox_to_anchor=(0.8, 0.7))


















''' top right panel '''

ax1.plot(log_center_Rho[0],log_center_T[0], label = r'15m1_0.0beta_p20', linewidth = 5, color = c1, linestyle = '-')

ax1.plot(log_center_Rho[1],log_center_T[1], label = r'15m1_0.3beta_p20', linewidth = 5, color = c3, linestyle = '-')

ax1.plot(log_center_Rho[2],log_center_T[2], label = r'15m1_0.5beta_p20', linewidth = 5, color = 'darkred', linestyle = '-')

ax1.plot(log_center_Rho[3],log_center_T[3], label = r'15m1_0.7beta_p20', linewidth = 5, color = 'black', linestyle = '-')

ax1.plot(log_center_Rho[4],log_center_T[4], label = r'15m1_1.0beta_p20', linewidth = 5, color = 'darkblue', linestyle = '--')

ax1.text(6.3,9.2,r'Ne ', fontsize = 30,ha = 'center')
ax1.text(6.65,9.33,r'O', fontsize = 30,ha = 'center')
ax1.text(7.55,9.55,r'Si', fontsize = 30,ha = 'center')





# plot entropy contours
for i in (19,20,21,22,23,24):
        
    s0 = i  # Example value for constant entropy
    
    # Generate a range of logT values
    logT_val = np.linspace(8.6, 10, 100)
    
    # Calculate corresponding logrho values
    logrho_val = 3 * logT_val - s0
    
    # Plot the line of constant entropy
    ax1.plot(logrho_val, logT_val, linewidth = 4, zorder =1, color = 'gray', linestyle = '--')
    
ax1.text(6.5,9.5,r'$s\propto T^{3}/\rho$', fontsize = 30,ha = 'center', rotation = 54.5)

# ax2.text(8.95,3.1,r'$\beta$+', fontsize = 36,ha = 'center')


ax1.set_xlim(5.0,10.2)
ax1.set_ylim(8.8,10)

#ax2.set_xlabel(r'Log (T\textsubscript{center}) [K]', fontsize = 40)
# ax2.set_ylabel(r'$\epsilon_{\nu_{e}}$ [Mev]', fontsize = 40)



# ax2

ax1.set_xlabel(r'log $\rho$\textsubscript{center} [g/cm$^{3}$]', fontsize = 40)
ax1.set_ylabel(r'log T\textsubscript{center} [K]', fontsize = 40)





ax1.legend(fontsize = '24',ncol = 1)#,bbox_to_anchor=(0, 0))












''' bottom right panel '''
# file_names = ['15m1_0.0beta_p20','15m1_0.3beta_p20','15m1_0.5beta_p20',
#               '15m1_0.7beta_p20','15m1_1.0beta_p20','15m1_0.0beta_p25','16m1_0.0beta_p20',
#               '20m1_0.0beta_p20','20m1_0.0beta_p25','80_single']

ax3.plot(log_center_Rho[0],log_center_T[0], label = r'15m1_0.0beta_p20', linewidth = 5, color = c1, linestyle = '-')

ax3.plot(log_center_Rho[5],log_center_T[5], label = r'15m1_0.0beta_p25', linewidth = 5, color = c3, linestyle = '-')

ax3.plot(log_center_Rho[6],log_center_T[6], label = r'16m1_0.0beta_p20', linewidth = 5, color = 'darkred', linestyle = '-')

ax3.plot(log_center_Rho[7],log_center_T[7], label = r'20m1_0.0beta_p20', linewidth = 5, color = 'black', linestyle = '-')

ax3.plot(log_center_Rho[8],log_center_T[8], label = r'20m1_0.0beta_p25', linewidth = 5, color = 'darkblue', linestyle = '--')

ax3.plot(log_center_Rho[9],log_center_T[9], label = r'80_wide_orbit', linewidth = 5, color = 'orchid', linestyle = '--')





# plot entropy contours
for i in (19,20,21,22,23,24):
        
    s0 = i  # Example value for constant entropy
    
    # Generate a range of logT values
    logT_val = np.linspace(8.6, 10, 100)
    
    # Calculate corresponding logrho values
    logrho_val = 3 * logT_val - s0
    
    # Plot the line of constant entropy
    ax3.plot(logrho_val, logT_val, linewidth = 4, zorder =1, color = 'gray', linestyle = '--')
    
ax3.text(6.5,9.5,r'$s\propto T^{3}/\rho$', fontsize = 30,ha = 'center', rotation = 54.5)

# ax2.text(8.95,3.1,r'$\beta$+', fontsize = 36,ha = 'center')


ax3.set_xlim(5.0,10.2)
ax3.set_ylim(8.8,10)

#ax2.set_xlabel(r'Log (T\textsubscript{center}) [K]', fontsize = 40)
# ax2.set_ylabel(r'$\epsilon_{\nu_{e}}$ [Mev]', fontsize = 40)



# ax2

ax3.set_xlabel(r'log $\rho$\textsubscript{center} [g/cm$^{3}$]', fontsize = 40)
ax3.set_ylabel(r'log T\textsubscript{center} [K]', fontsize = 40)





ax3.legend(fontsize = '24',ncol = 1)#,bbox_to_anchor=(0, 0))

















' final formatting'
# modify ticks
# ax2.tick_params(labelbottom=False)

plt.xticks(fontsize = 36)



ax1.tick_params(axis = 'x', labelsize = 36,pad = 10)
ax2.tick_params(axis = 'x', labelsize = 36,pad = 10)
ax3.tick_params(axis = 'x', labelsize = 36,pad = 10)
ax4.tick_params(axis = 'x', labelsize = 36,pad = 10)


ax1.tick_params(axis = 'y', labelsize = 36,pad = 10)
ax2.tick_params(axis = 'y', labelsize = 36,pad = 10)
ax3.tick_params(axis = 'y', labelsize = 36,pad = 10)
ax4.tick_params(axis = 'y', labelsize = 36,pad = 10)


# fig1.subplots_adjust(right=0.)




fig1.tight_layout()
fig1.savefig('history.pdf',dpi=400)



# In[ ]:






