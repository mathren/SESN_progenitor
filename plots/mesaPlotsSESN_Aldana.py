# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 10:53:17 2025

@author: aldana
"""


import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from collections import OrderedDict
from matplotlib.ticker import AutoMinorLocator  


Rsun = 6.96*10**10
Msun = 1.989*10**33


def importData(pathToFile):
    with open(pathToFile, 'r') as file:
        lines = file.readlines()
    
    # Step 1: Skip the first line
    # Step 2: Second line as headers for the first section
    first_section_headers = lines[1].strip().split()

    # Step 3: Third line as values for the first section
    first_section_values = lines[2].strip().split()

    # Step 4: Skip the blank line (already skipped in indexing)
    # Step 5: Skip the line with numbers (already skipped in indexing)

    # Step 6: Sixth line as headers for the second section
    second_section_headers = lines[5].strip().split()

    # Step 7: The remaining lines as data for the second section
    second_section_data = []
    for line in lines[6:]:
        second_section_data.append(line.strip().split())

    # Converting the first section to a dictionary
    generalProperties = dict(zip(first_section_headers, first_section_values))

    # Creating an ordered dictionary for the second section
    data = OrderedDict((header, []) for header in second_section_headers)

    # Filling in the second section dictionary with data
    for row in second_section_data:
        for i, header in enumerate(second_section_headers):
            data[header].append(row[i])

    return generalProperties, data



def extractVariablesFromProfile(generalProfileProperties,profileData):
    

    radius = np.array(profileData['radius']).astype(float) # solar units
    radius = np.flip(radius)

    mass = np.array(profileData['mass']).astype(float) # solar units
    mass = np.flip(mass)

    
    logRho = np.array(profileData['logRho']).astype(float) 
    logRho = np.flip(logRho)
    
    logT = np.array(profileData['logT']).astype(float) 
    logT = np.flip(logT)
     
    Ye = np.array(profileData['ye']).astype(float) 
    Ye = np.flip(Ye)
    
    # si27 = np.array(profileData['si27']).astype(float) 
    # si27 = np.flip(si27)
    # si28 = np.array(profileData['si28']).astype(float) 
    # si28 = np.flip(si28)
    # si29 = np.array(profileData['si29']).astype(float) 
    # si29 = np.flip(si29)
    # si30 = np.array(profileData['si30']).astype(float) 
    # si30 = np.flip(si30)
    
    # fe52 = np.array(profileData['fe52']).astype(float) 
    # fe52 = np.flip(fe52)
    # fe53 = np.array(profileData['fe53']).astype(float) 
    # fe53 = np.flip(fe53)
    # fe54 = np.array(profileData['fe54']).astype(float) 
    # fe54 = np.flip(fe54)
    # fe55 = np.array(profileData['fe55']).astype(float) 
    # fe55 = np.flip(fe55)
    # fe56 = np.array(profileData['fe56']).astype(float) 
    # fe56 = np.flip(fe56)
    # fe57 = np.array(profileData['fe57']).astype(float) 
    # fe57 = np.flip(fe57)
    # fe58 = np.array(profileData['fe58']).astype(float) 
    # fe58 = np.flip(fe58)


    
    # data_dict = {'dr': dr,'tau': tau,'radius': radius,'mass': mass,'conv_vel': conv_vel, 'sound_speed':sound_speed,
    #     'logT': logT,'logRho': logRho,'Ye': Ye,'timestep':timestep, 'co_core_mass':co_core_mass, 
    #     'timestep':timestep, 'star_age':star_age, 'log_dt':log_dt, 
    #     'si28':si28, 'si29':si29, 'si30':si30,'fe52':fe52,'fe53':fe53, 'fe54':fe54,'fe56':fe56,
    #     'fe57':fe57,'fe58':fe58,'si27':si27,'fe55':fe55}
    
    profile_data_dict = {'radius': radius,'mass': mass,'logT': logT,'logRho': logRho,'Ye': Ye}
    
    return profile_data_dict

def plotStellarProfiles(profile_data_dict):
    
    radius = profile_data_dict['radius']
    mass = profile_data_dict['mass']
    logT = profile_data_dict['logT']
    logRho = profile_data_dict['logRho']
    Ye = profile_data_dict['Ye']

        
    plt.figure()
    plt.rcParams['font.size'] = 10
    plt.rcParams['figure.dpi'] = 300
    plt.plot(mass,logRho)  
    plt.xlabel(r"$log [m (M_{\rm \odot})]$")
    plt.ylabel(r"$\rm log \rho[g/cm^{3}]$")
    plt.legend(loc='lower left',frameon=False)

    return

def gather_all_profile_paths(baseDir):
    """
    Gather paths to all 'final_profile.data' files in subdirectories of baseDir.
    """
    profile_paths = []
    for root, dirs, files in os.walk(baseDir):
        for file in files:
            if file == 'final_profile.data':
                profile_paths.append(os.path.join(root, file))
    return profile_paths

def plot_combined_profiles(profile_data_dicts, labels):
    """
    Plot multiple profiles on the same graph.
    """

    fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=True)

        
    plt.subplots_adjust(left=0.15, right=0.85, top=0.95, bottom=0.1, hspace=0.1)
    
    fig.align_ylabels() # Ensures both y-labels are aligned
    
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['font.serif'] = ['Times New Roman']
    plt.rcParams['font.size'] = 18  # Set the default font size
    plt.rcParams['mathtext.fontset'] = 'stix'

    # Adjust the spacing between the subplots to make them touch each other
    plt.subplots_adjust(hspace=0, wspace=0)
    for i, profile_data_dict in enumerate(profile_data_dicts):
        mass = profile_data_dict['mass']
        logT = profile_data_dict['logT']
        ye = profile_data_dict['Ye']
        logRho = profile_data_dict['logRho']
        
        axes[0].plot(mass, ye, label=labels[i])
        axes[0].set_xlim(([0,2.5]))
        axes[2].set_ylim(([0.42,0.5]))
        axes[0].yaxis.set_minor_locator(AutoMinorLocator())  # Minor ticks for the primary y-axis
        axes[0].set_ylabel(r"$\rm Y_{\rm e}$")
        axes[0].legend(loc='lower right', frameon=False,fontsize=11)
        
        axes[1].plot(mass, logT, label=labels[i])
        axes[1].set_xlim(([0,2.5]))
        axes[1].set_ylim(([8.7,9.99]))
        axes[1].yaxis.set_minor_locator(AutoMinorLocator())  # Minor ticks for the primary y-axis
        axes[1].set_xlabel(r"$m [M_{\rm \odot}]$")
        axes[1].set_ylabel(r"$\rm log T[k]$")
        
        axes[2].plot(mass, logRho, label=labels[i])
        axes[2].set_xlim(([0,2.5]))
        axes[2].set_ylim(([4,10.2]))
        axes[2].yaxis.set_minor_locator(AutoMinorLocator())  # Minor ticks for the primary y-axis
        axes[2].set_xlabel(r"$m [M_{\rm \odot}]$")
        axes[2].set_ylabel(r"$\rm log \rho[g/cm^{3}]$")
        

def mainAnalysisMultipleProfiles(baseDir):
    """
    Analyze and plot profiles from all final_profile.data files found in subdirectories.
    """
    profile_paths = gather_all_profile_paths(baseDir)
    profile_data_dicts = []
    labels = []
    manual_lables = []
    
    for path in profile_paths:
        generalProfileProperties, profileData = importData(path)
        profile_data_dict = extractVariablesFromProfile(generalProfileProperties, profileData)
        profile_data_dicts.append(profile_data_dict)
        labels.append(os.path.basename(os.path.dirname(path)))
        
    plot_combined_profiles(profile_data_dicts, labels)


# def extractVariablesFromHistory(generalHistoryProperties,historyData):
    


#     star_age = np.array(historyData['star_age']).astype(float) 
#     star_age = np.flip(star_age)
    
#     log_dt = np.array(historyData['log_dt']).astype(float) 
#     log_dt = np.flip(log_dt)


        

    
#     data_dict = {'dr': dr,'tau': tau,'radius': radius,'mass': mass,'conv_vel': conv_vel, 'sound_speed':sound_speed,
#         'logT': logT,'logRho': logRho,'Ye': Ye,'timestep':timestep, 'co_core_mass':co_core_mass, 
#         'timestep':timestep, 'star_age':star_age, 'log_dt':log_dt, 
#         'si28':si28, 'si29':si29, 'si30':si30,'fe52':fe52,'fe53':fe53, 'fe54':fe54,'fe56':fe56,
#         'fe57':fe57,'fe58':fe58,'si27':si27,'fe55':fe55}
    
#     return data_dict






    
# def plotHistoryProperties(data_dict):
    
#     timestep = data_dict['timestep']
#     star_age = data_dict['star_age']
#     log_dt = data_dict['log_dt'] # in yers
#     log_dt_sec = np.log10((31556926*(10**log_dt)))
#     log_center_T = data_dict['log_center_T']
#     log_center_Rho = data_dict['log_center_Rho']
#     center_h1 = data_dict['center_h1']
#     center_he4 = data_dict['center_he4']
#     center_c12 = data_dict['center_c12']
#     center_o16 = data_dict['center_o16']
#     center_si28 = data_dict['center_si28']
#     center_fe56 = data_dict['center_fe56']
   
    
#     x_axis = np.log10(np.array(star_age)[0]-np.array(star_age)) #last profile 
#     #print('star age',star_age)
    
#     plt.figure()
#     plt.rcParams['font.size'] = 10
#     #plt.rcParams['figure.dpi'] = 300
#     #plt.plot(np.log10(star_age),log_dt_sec,'o',color='grey')
#     plt.plot(x_axis,log_dt_sec,'o',color='grey')
#     plt.xlabel(r"$log[age,f - age]$")
#     plt.ylabel(r"$log[dt]$")
#     print("smallest timestep:",10**min(log_dt_sec))
#     #plt.legend(loc='lower left',frameon=False)
#     #plt.xlim([-0.1, 1])
#     plt.gca().invert_xaxis()

    
#     plt.figure()
#     plt.rcParams['font.size'] = 10
#     #plt.rcParams['figure.dpi'] = 300
#     plt.plot(np.log10(star_age),log_dt_sec,'o',color='grey')
#     star_age_o_depl = 6.3036338275683811*10**6
#     star_age_Si_depl = 6.3036339344750084*10**6
#     index_o_depl = np.where(star_age > star_age_o_depl)[0][0]
#     index_Si_depl = np.where(star_age > star_age_Si_depl)[0][0]
#     #print(index_o_depl,index_Si_depl)
#     plt.plot(np.log10(star_age)[index_o_depl],log_dt_sec[index_o_depl],'o',color='red')
#     plt.plot(np.log10(star_age)[index_Si_depl],log_dt_sec[index_Si_depl],'o',color='red')
#     #plt.axvline(x=log_star_age_o_depl, color='r', linestyle='--')
#     #plt.axvline(x=log_star_age_Si_depl, color='r', linestyle='--')
#     plt.xlabel(r"log[age]")
#     plt.ylabel(r"$log[dt]$")
#     print("smallest timestep:",10**min(log_dt_sec))
#     #plt.legend(loc='lower left',frameon=False)
#     #plt.xlim([14.29868566, 14.29868568])
    
    
#     star_age = 365*star_age #to convert to days
    
#     plt.figure()
#     plt.rcParams['font.size'] = 10
#     plt.rcParams['figure.dpi'] = 300
#     plt.plot(np.log10(star_age),np.log10(center_h1),'.',label=r'h1')
#     plt.plot(np.log10(star_age),np.log10(center_he4),'.',label=r'he4')
#     plt.plot(np.log10(star_age),np.log10(center_c12),'.' ,label=r'c12')
#     plt.plot(np.log10(star_age),np.log10(center_o16),'.',label=r'o16')
#     plt.plot(np.log10(star_age),np.log10(center_si28),'.',label=r'si28')
#     plt.plot(np.log10(star_age),np.log10(center_fe56),'.',label=r'fe56')
#     plt.xlabel(r"log[age[days]]")
#     plt.ylabel(r"$x$")
#     #plt.xlim([6.7,6.81])
#     plt.ylim([-10,0.5])
#     plt.legend(loc='lower left',frameon=False)

    

    
#     fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=True)

#     # Adjust the spacing between the subplots to make them touch each other
#     plt.subplots_adjust(hspace=0, wspace=0)
    
#     index_h1_depl = np.where(center_h1 < 10**(-6))[0][0] #-6
#     index_he4_depl = np.where(center_he4 < 10**(-6))[0][0] #-6
#     print('len(center_c12)',len(center_c12))
#     index_c12_depl = np.where(center_c12 < 10**(-6))[0][0] #-6
#     index_o16_depl = np.where(center_o16 < 10**(-3))[0][0] #-6
#     #index_si28_depl = np.where(center_si28 < 10**(-3))[0][0] #-6

#     print("index_h1_depl",index_h1_depl)
#     print("index_he4_depl",index_he4_depl)
#     print("index_c12_depl",index_c12_depl)
#     print("index_o16_depl",index_o16_depl)
#     #print("index_si28_depl",index_si28_depl)

#     print("star_age[index_o16_depl]",star_age[index_o16_depl])
#     #print("star_age[index_si28_depl]",star_age[index_si28_depl])
#     #print("time from Si depl to end of the simulation",365*(star_age[-1]-star_age[index_si28_depl]))


#     # First plot (panel 1)
#     axes[0].semilogx(star_age, log_center_T, '.', markersize=10, color='dodgerblue', label="mesa80")
#     axes[0].semilogx(star_age[index_h1_depl],log_center_T[index_h1_depl],'o',label=r"$h_{\rm dep}$")
#     axes[0].semilogx(star_age[index_he4_depl],log_center_T[index_he4_depl],'o',label=r"$he_{\rm dep}$")
#     axes[0].semilogx(star_age[index_c12_depl],log_center_T[index_c12_depl],'o',label=r"$c_{\rm dep}$")
#     axes[0].semilogx(star_age[index_o16_depl],log_center_T[index_o16_depl],'o',label=r"$o_{\rm dep}$")
#     axes[0].legend(loc='upper left', frameon=False)
#     axes[0].set_ylabel(r'$\rm log_{\rm 10}(T/[K])$')
#     #axes[0].set_xlim(10**6.7,10**6.81)

#     # Second plot (panel 2)
#     axes[1].semilogx(star_age, log_center_Rho, '.', markersize=10, color='dodgerblue', label="mesa80")    
#     axes[1].legend(loc='upper left', frameon=False)
#     axes[1].set_ylabel(r'$\rm log_{\rm 10}(\rho/[g \: cm^{-3}])$')

#     # Third plot (panel 3)
#     axes[2].semilogx(star_age, log_dt_sec, '.', markersize=10, color='dodgerblue', label="mesa80")
#     axes[2].semilogx(star_age[index_h1_depl],log_dt_sec[index_h1_depl],'o',label=r"$h_{\rm dep}$")
#     axes[2].semilogx(star_age[index_he4_depl],log_dt_sec[index_he4_depl],'o',label=r"$he_{\rm dep}$")
#     axes[2].semilogx(star_age[index_c12_depl],log_dt_sec[index_c12_depl],'o',label=r"$c_{\rm dep}$")
#     axes[2].semilogx(star_age[index_o16_depl],log_dt_sec[index_o16_depl],'o',label=r"$o_{\rm dep}$")     
#     axes[2].legend(loc='lower left', frameon=False)
#     axes[2].set_xlabel(r'age[yr]')
#     axes[2].set_ylabel(r'$\rm log_{\rm 10}(dt[sec])$')
    
    
#     fig, axes = plt.subplots(3, 1, figsize=(8, 12), sharex=True)

#     # Adjust the spacing between the subplots to make them touch each other
#     plt.subplots_adjust(hspace=0, wspace=0)
    
#     star_age_o_depl = star_age[index_o16_depl:-1] # in days
#     star_age_o_depl = star_age_o_depl - star_age_o_depl[0]
#     log_center_T_o_depl = log_center_T[index_o16_depl:-1]
#     log_center_Rho_o_depl = log_center_Rho[index_o16_depl:-1]
#     log_dt_sec_o_depl = log_dt_sec[index_o16_depl:-1]

#     center_si28_o_depl = center_si28[index_o16_depl:-1] # in days
#     #print('center_si28_o_depl',center_si28_o_depl)
#     index_si_depl_in_center_si28_o_depl = np.where(center_si28_o_depl < 10**(-3))[0][0] #-6
#     star_age_si_depl = star_age_o_depl[index_si_depl_in_center_si28_o_depl]
#     print("index_si_depl",index_si_depl_in_center_si28_o_depl)
#     print("star_age_si_depl",star_age_si_depl)
#     print("time from Si depl to end of the simulation",(star_age_o_depl[-1]-star_age_o_depl[index_si_depl_in_center_si28_o_depl]))


#     # First plot (panel 1)
#     axes[0].semilogx(star_age_o_depl, log_center_T_o_depl, '.', markersize=10, color='dodgerblue', label="mesa80")
#     axes[0].legend(loc='upper left', frameon=False)
#     axes[0].set_ylabel(r'$\rm log_{\rm 10}(T/[K])$')

#     # Second plot (panel 2)
#     axes[1].semilogx(star_age_o_depl, log_center_Rho_o_depl,'.', markersize=10, color='dodgerblue', label="mesa80")  
#     axes[1].legend(loc='upper left', frameon=False)
#     axes[1].set_ylabel(r'$\rm log_{\rm 10}(\rho/[g \: cm^{-3}])$')

#     # Third plot (panel 3)
#     axes[2].semilogx(star_age_o_depl, log_dt_sec_o_depl, '.', markersize=10, color='dodgerblue', label="mesa80")    
#     axes[2].legend(loc='lower left', frameon=False)
#     axes[2].set_xlabel(r'time[days]')
#     axes[2].set_ylabel(r'$\rm log_{\rm 10}(dt[sec])$')
    
#     #np.savez("20M_mesa151_lgTmax_Data.npz",star_age_o_depl=star_age_o_depl, log_center_T_o_depl=log_center_T_o_depl,
#     #         log_center_Rho_o_depl=log_center_Rho_o_depl,log_dt_sec_o_depl=log_dt_sec_o_depl)
    
#     #np.savez("20M_mesa151_to_cc_Data.npz",star_age=star_age, log_center_T=log_center_T,
#     #         log_center_Rho=log_center_Rho,log_dt_sec=log_dt_sec)
    
#     return
    




# %% Main
# Call the function with the base directory
baseDir = "\\\\wsl.localhost/Ubuntu/home/aldana/TARDIS_connector_SESN/stellar_models/"
mainAnalysisMultipleProfiles(baseDir)


