
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



# sol, the four histories to read in

file_names = ['15m1_0.0beta_p20','15m1_0.3beta_p20','15m1_0.5beta_p20','15m1_0.7beta_p20','15m1_1.0beta_p20','15m1_0.0beta_p25','16m1_0.0beta_p20','20m1_0.0beta_p20','20m1_0.0beta_p25','80_single']

#model_number = []
non_nuc_neu = []
ye = []

mass = []
radius = []
logR = []
logT = []
logRho = []
'''loop through files and store data variables for each file'''

for i in file_names:
    print ('i =',i)
    # importing files from history.data in each model folder
    file_name1 = str(i)
    location = "data/" + file_name1 + "/LOGS1/final_profile.data"
    print ('importing files from model :',file_name1)
    model = mesa_reader.MesaData(file_name = location, file_type=None)

#    model_number.append(model.data('model_number'))
   
    ye.append(model.data('ye'))
    non_nuc_neu.append(model.data('non_nuc_neu'))

    mass.append(model.data('mass'))
    radius.append(model.data('radius'))
    logR.append(model.data('logR'))
    logT.append(model.data('logT'))
    logRho.append(model.data('logRho'))
    
# '''store all data variables as numpy arrays, (better for calculation)'''
# model_number = np_array(model_number)
#model_number = np_array(model_number)

ye = np_array(ye)
non_nuc_neu = np_array(non_nuc_neu)

mass = np_array(mass)
radius = np_array(radius)
logR = np_array(logR)
logT = np_array(logT)
logRho = np_array(logRho)



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



# Figure (1), mass resolution
'''---------------------------------------------------------------------------------'''
fig1 = plt.figure(figsize=(12,18)) # 2x 8,6 on 27 inch 16:9 1440p monitor.
plt.style.use('mesa.mplstyle')

ax1 = fig1.add_subplot(211)
ax2 = fig1.add_subplot(212)
# ax3 = fig1.add_subplot(313)







ax1.plot(mass[0],ye[0], label = r'15m1_0.0beta_p20', linewidth = 5, color = c1, linestyle = '--',zorder = 3)
ax1.plot(mass[1],ye[1], label = r'15m1_0.3beta_p20', linewidth = 5, color = c3, linestyle = '-',zorder = 2)
ax1.plot(mass[2],ye[2], label = r'15m1_0.5beta_p20', linewidth = 5, color = c5,zorder = 2)
ax1.plot(mass[3],ye[3], label = r'15m1_0.7beta_p20', linewidth = 5, color = c6,zorder = 2)
ax1.plot(mass[4],ye[4], label = r'15m1_1.0beta_p20', linewidth = 5, color = c7,zorder = 2)
ax1.plot(mass[5],ye[5], label = r'15m1_0.0beta_p25', linewidth = 5, color = c8,zorder = 2)
ax1.plot(mass[6],ye[6], label = r'16m1_0.0beta_p20', linewidth = 5, color = c9,zorder = 2)
ax1.plot(mass[7],ye[7], label = r'20m1_0.0beta_p20', linewidth = 6, color = c10,zorder = 4)
ax1.plot(mass[8],ye[8], label = r'20m1_0.0beta_p25', linewidth = 6, color = c11,zorder = 4)
ax1.plot(mass[9],ye[9], label = r'80_wide_binary', linewidth = 6, color = 'k',zorder = 4)








ax1.legend(fontsize = '20',ncol = 1)#,bbox_to_anchor=(0, 0))
# ax2.legend(fontsize = '20',ncol = 2,loc = 6,bbox_to_anchor=(0.12, 0.7))


        
ax1.set_xlim(0.,2.5)

# ax1.set_xlabel(r'mass [M$_{\odot}$]', fontsize=40)
ax1.set_ylabel(r'y$_{e}$', fontsize=40)


# modify ticks
# ax1.tick_params(labelbottom=False)


ax1.tick_params(axis = 'x', labelsize = 30,pad = 10)
ax1.tick_params(axis = 'y', labelsize = 30,pad = 10)


# turn off  x axis labels on top panels
ax1.set_xticklabels([])










'second panel middle'



ax2.plot(mass[0],logRho[0], label = r'15m1_0.0beta_p20', linewidth = 5, color = c1, linestyle = '--',zorder = 3)
ax2.plot(mass[1],logRho[1], label = r'15m1_0.3beta_p20', linewidth = 5, color = c3, linestyle = '-',zorder = 2)
ax2.plot(mass[2],logRho[2], label = r'15m1_0.5beta_p20', linewidth = 5, color = c5,zorder = 2)
ax2.plot(mass[3],logRho[3], label = r'15m1_0.7beta_p20', linewidth = 5, color = c6,zorder = 2)
ax2.plot(mass[4],logRho[4], label = r'15m1_1.0beta_p20', linewidth = 5, color = c7,zorder = 2)
ax2.plot(mass[5],logRho[5], label = r'15m1_0.0beta_p25', linewidth = 5, color = c8,zorder = 2)
ax2.plot(mass[6],logRho[6], label = r'16m1_0.0beta_p20', linewidth = 5, color = c9,zorder = 2)
ax2.plot(mass[7],logRho[7], label = r'20m1_0.0beta_p20', linewidth = 6, color = c10,zorder = 4)
ax2.plot(mass[8],logRho[8], label = r'20m1_0.0beta_p25', linewidth = 6, color = c11,zorder = 4)
ax2.plot(mass[9],logRho[9], label = r'80_wide_binary', linewidth = 6, color = 'k',zorder = 4)






#ax2.set_xticklabels([])
# ax2.legend(fontsize = '20',ncol = 1)#,bbox_to_anchor=(0, 0))


        
ax2.set_xlim(0.,2.5)
ax2.set_ylim(7.,10.2)

ax2.set_xlabel(r'mass [M$_{\odot}$]', fontsize=40)
ax2.set_ylabel(r'log $\rho$ [g/cm$^{3}$]', fontsize=40)


# modify ticks
# ax2.tick_params(labelbottom=False)

ax2.tick_params(axis = 'x', labelsize = 30,pad = 10)
ax2.tick_params(axis = 'y', labelsize = 30,pad = 10)



# bring panels closer together
fig1.subplots_adjust(hspace=0)  






#fig1.tight_layout()
fig1.savefig('profile.pdf',dpi=400)





