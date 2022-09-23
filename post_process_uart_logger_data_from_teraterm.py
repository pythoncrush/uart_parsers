import re
import glob
import pandas as pd
from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#Cypress reference firmware for BLE, MCU, and Bluetooth events.
voice_prompt_dictionary = {'0':  'VPR_STOP_PROMPT',
						   '1':  'VPR_PAIRING_BLUETOOTH', 
						   '2':  'VPR_BLUETOOTH_PAIRED',
						   '3':  'VPR_BLUETOOTH_PAIRING_FAILED',
						   '4':  'VPR_BLUETOOTH_CONNECTED',
						   '5':  'VPR_BLUETOOTH_DISCONNECTED',
						   '6':  'VPR_BLUETOOTH_ON',
						   '7':  'VPR_BLUETOOTH_OFF',
						   '8':  'VPR_CHARGING_BATTERY',
						   '9':  'VPR_PAIRING_HEADSET',
						   '10': 'VPR_HEADSET_PAIRED',
						   '11': 'VPR_BATTERY_LEVEL_HIGH',
						   '12': 'VPR_BATTERY_LEVEL_MEDIUM',
						   '13': 'VPR_BATTERY_LEVEL_LOW',
						   '14': 'VPR_POWER_ON',
						   '15': 'VPR_POWER_OFF',
						   '16': 'VPR_INCOMING_CALL',
						   '17': 'VPR_SYS_LAST'}

#fonts for matplot lib figures
SMALL_SIZE = 7
MEDIUM_SIZE = 10
BIGGER_SIZE = 12

plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=MEDIUM_SIZE)  # fontsize of the figure title


def read_logs_and_create_csv_files():
	for name in glob.glob('*.log'):
		ts = datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
		outfile_name1 = name + '_voice_prompts_' + ts + '.csv'
		outfile_name2 = name + '_battery_percentage_' + ts + '.csv'
		outfile_name3 = name + '_voltage_' + ts + '.csv'
		
		with open(name, 'r') as infile:
			with open(outfile_name1, 'w') as outfile1, open(outfile_name2, 'w') as outfile2, open(outfile_name3, 'w') as outfile3:
				for line in infile:
					if (regex_matched := re.search(r'\[(\d{4}-\d+-\d+)\s+(\d+:\d+:\d+\.\d+)]\s+\[(.+)]\s+file_index:(\d+)', line)):
						date_parsed = regex_matched.group(1)
						time_stamp_parsed = regex_matched.group(2)
						text_parsed = regex_matched.group(3)
						index_parsed = regex_matched.group(4)
						print(date_parsed + ',' +time_stamp_parsed + ',' +voice_prompt_dictionary[index_parsed], file=outfile1)

					if (regex_matched := re.search(r'\[(\d{4}-\d+-\d+)\s+(\d+:\d+:\d+\.\d+)]\s+\.(.+)MCU:\s+Batt\s+%=(\d+)\s+V=(\d+)', line)):
						date_parsed = regex_matched.group(1)
						time_stamp_parsed = regex_matched.group(2)
						batt_percentage_parsed = regex_matched.group(4)
						voltage_parsed = regex_matched.group(5)
						print(date_parsed + ',' +time_stamp_parsed + ',' +batt_percentage_parsed, file=outfile2)
						print(date_parsed + ',' +time_stamp_parsed + ',' +voltage_parsed, file=outfile3)

def compose_pandas_dataframes_and_plots():
	for name in glob.glob('*.csv'):
		headers_1 = ['Date','Time','Voice_prompts']
		headers_2 = ['Date','Time','Battery_pecentage']
		headers_3 = ['Date','Time','Voltage']

		if 'voice' in name:
			df = pd.read_csv(name,names=headers_1)
			x = df['Time']
			y = df['Voice_prompts']
		if 'battery' in name:
			df = pd.read_csv(name,names=headers_2)
			x = df['Time']
			y = df['Battery_pecentage']
		if 'voltage' in name:
			df = pd.read_csv(name,names=headers_3)
			x = df['Time']
			y = df['Voltage']
		#printing dataframe head to verify data looks good	
		print(df.head())

		#don't remember what this is, leaving it in in case it becomes necessary to use
		#df['Time'] = df['Date'].map(lambda x: datetime.strptime(str(x), '%Y/%m/%d %H:%M:%S.%f'))
	
		# plot
		plt.plot(x,y)
		# beautify the x-labels
		plt.gcf().autofmt_xdate()
		plt.gca().set_title(name)
		#can change interval to 5,10 any number if there is too much data to plot
		plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
		name = name + '.png'
		plt.show()
		#plt.savefig(name)


if __name__ == "__main__":
	read_logs_and_create_csv_files()
	compose_pandas_dataframes_and_plots()

    
