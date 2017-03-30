#!/usr/bin/python

"""
Danielle McDermott 
6/11/2015
Histogram Code
Python 2.7

Take raw data and make 3d contour plot histograms. 
vx vs. vy colored by frequency, making a 2d image
"""
#load matplotlib libraries separately, mainly for ease of use
#if your computer is slow, just import these
#and don't bother with importing the entire library
import matplotlib.pyplot as plt
import matplotlib.colors as clr
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator
from matplotlib.ticker import MaxNLocator

#make all of the fonts big, unfortunately this involves
#loading the entire library.  thank goodness for modern computers
import matplotlib 
matplotlib.rcParams.update({'font.size': 11})

import numpy as np

#home written subroutines not called, very powerful, but not well documented
import data_importerDM as di
#import Plot2D_Library as p2D

#####################################################
#Define Modules Here, in principle
#####################################################

###############################################################
#main function begins
###############################################################


if __name__ == "__main__":

    #####################################################
    #define figure
    #####################################################
    size1=(6,6)
    rows=2
    columns=2
    fig = plt.figure(figsize=(size1[0],size1[1]),num=None, facecolor='w', edgecolor='k')

    if 0:
        fig.subplots_adjust(top=0.8)
        fig.suptitle("No Substrate, 1000 particles",fontsize=14,backgroundcolor='white')

    minorLocator   = AutoMinorLocator()
    ticksLocator   = MaxNLocator()

    G = gridspec.GridSpec(rows, columns)

    #leave room for subplotting
    ax1 = fig.add_subplot(G[0])
    ax2 = fig.add_subplot(G[1])
    ax3 = fig.add_subplot(G[2])
    ax4 = fig.add_subplot(G[3])

    #####################################################
    #import data from c code calculation
    #####################################################
    data_file="raw_speed.txt"

    raw_data=di.get_data(data_file,4,sep="\t")

    vx=raw_data[1]
    vy=raw_data[2]
    speed=raw_data[3]

    weights=np.ones_like(speed)/len(speed)

    (H,xedges,yedges,img) = ax4.hist2d(vx,vy,bins=40,norm=clr.LogNorm(),
                                       weights=weights)
    ax4.xaxis.set_major_locator(MaxNLocator(4))
    ax4.yaxis.set_major_locator(MaxNLocator(5))

    try:
        if 0:
            fig.subplots_adjust(right=0.8)
            cbar_ax=fig.add_axes([0.85,0.15,0.05,0.7])
            cbar = fig.colorbar(img, cax=cbar_ax)
        else:
            cbar = fig.colorbar(img, ax=ax4)

    except:
        print "figure out how to plot"

    counter=0
    log_bins=0
    linear_bins=1
    
    for data,ax in zip([vx,vy,speed],[ax1,ax2,ax3]):

        if  ax == ax1 or ax == ax2 or ax == ax3:
            weights=np.ones_like(data)/len(data)
            (n,bins,patches)=ax.hist(data,40,weights=weights)
            if counter<2 and 0:
                ax.set_ylim(0,0.10)
                ax.set_ylim(1e-3,0.3)
            #ax.set_yscale('log')
        
        '''
        elif ax == ax3:
            ax.hist(data, log=True,bins=np.logspace(-9, 0, 10)) 
            ax.set_xscale('log') 
        
            if 1:
                ax.set_xscale('log') 
                ax.set_yscale('log')
                ax.set_ylim(10e-4,1.0e-3) 
                ax.set_xlim(10e-4,1.0) 
        '''

        ax.xaxis.set_major_locator(MaxNLocator(3))
        ax.yaxis.set_major_locator(MaxNLocator(3))

        counter+=1
    
    ax4.set_xlabel("$v_x$",fontsize=22)
    ax4.set_ylabel("$v_y$",fontsize=22)

    ax1.set_xlabel("$v_x$",fontsize=22)
    ax2.set_xlabel("$v_y$",fontsize=22)
    ax3.set_xlabel("$|v|$",fontsize=22)


    fig.tight_layout()

    fig.savefig("histogram.png")
