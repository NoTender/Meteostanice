#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function   
import matplotlib
import pandas as pd
import datetime
import math
import numpy as np
import sys

class Plotter:
    data = dict() #Data from CSV file
    #Define colors for lines in graph:
    colors = {'temps': (199/255., 199/255., 199/255.), 'pressure': (214/255., 39/255., 40/255.), 'humidity': (255/255., 127/255., 14/255.)}
    dates = []
    
    #Loads data from csv database
    def getData(self):
        try:
            csv_data = pd.read_csv('out.csv', names=['timestamps', 'temps', 'pressure', 'humidity'])
        except:
            print('Could not load data from csv.', file=sys.stderr)
            sys.exit(1)
        
        timestamps = csv_data['timestamps'].values
        self.data['temps'] = csv_data['temps'].values
        self.data['pressure'] = csv_data['pressure'].values
        self.data['humidity'] = csv_data['humidity'].values
        self.dates = [datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S') for date in timestamps] #Convert timestamp to date
    
    def setGraphAppearance(self, quantity, days):
        #Set visibility of spines
        fig, ax = plt.subplots()    
        ax.spines["top"].set_visible(False)    
        ax.spines["bottom"].set_visible(False)    
        ax.spines["right"].set_visible(False)    
        ax.spines["left"].set_visible(False)
        
        #Set positions of x and y axes
        ax.get_xaxis().tick_bottom()    
        ax.get_yaxis().tick_left()

        #Set label of y axis and title of graph
        if (quantity == 'temps'):
            title = 'Temperature\n'
            plt.ylabel("Temperature [°C]".decode('utf8'))
        elif (quantity == 'pressure'):
            title = 'Pressure\n'
            plt.ylabel("Pressure [MBar]".decode('utf8'))
        else:
            title = 'Humidity\n'
            plt.ylabel("Humidity [%]".decode('utf8'))  

        plt.xlabel('Time [HH:MM:SS]')

        #If data are from more than one day print interval of days
        if (len (days) == 1):
            title += days[0]
        else:
            title += days[0] + ' - ' + days[-1]
        
        plt.title(title, y = 1.03, fontsize=20)
        plt.tight_layout()
        
        #For graph in full-screen
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())
        
    
    def plot(self):
        self.getData()

        days = np.unique([x[0:10] for x in self.dates]) #Find days where capturing of data was performed
        times = [x[11:] for x in self.dates] #Find times when samples were captured
        
        #For every key and value in loaded data
        for key, value in self.data.iteritems():
            self.setGraphAppearance(key, days)

            #Plotting of graph:
            false_x = [x for x in range(len(times))]
            plt.xticks(range(len(times)), times, rotation=90)

            #Set number of x ticks labels 
            ticks_labels_frequency = int(math.ceil(len(value) / 150.))
            frame = plt.gca()
            for label in frame.axes.get_xaxis().get_ticklabels():
                label.set_visible(False)
            for label in frame.axes.get_xaxis().get_ticklabels()[::ticks_labels_frequency]:
                label.set_visible(True)
            
            #Set min and max values of both axes
            ymin = int(math.floor(min(value)) - 1)
            ymax = int(math.ceil(max(value)) + 1)
            plt.axis([-1, len(times), ymin, ymax])
            
            #Plot tick lines across the graph to help viewers trace along
            for y in range(int(ymin + 1), ymax, 1):    
                plt.plot(range(-1, len(times)+1), [y] * (len(range(-1, len(times)))+1), "--", lw=0.5, color="black", alpha=0.3)
            
            #Plot data into graph
            plt.plot(false_x, value, 'o-' ,lw=2.5, markersize=5.0, markeredgewidth=0.0 ,color=self.colors[key])
        
        plt.show()
