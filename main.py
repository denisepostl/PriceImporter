import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import matplotlib.dates as mdates

class Importer:
    def __init__(self, in_file, out_file):
        self.in_file = in_file 
        self.out_file = out_file
        self.data = []

    def read(self):
        with open(self.in_file, 'r') as f:
            content = f.readlines()
            self.data = [line.strip().split(', ') for line in content]  # Split lines
            return content
        
    def usd_to_eur(self, share):
        return float(share) * 0.91
    
    def to_upper(self, text):
        return str(text).upper()
    
    def convert_timestamp(self, timestamp):
        return datetime.fromtimestamp(int(timestamp))
    
    def round_share(self, share):
        return round(share, 2)

    def transform(self):
        self.read()
        cont = 'COMPANY,DATE,SHARE,CURRENCY,COMPANY_LOCATION\n'
        
        for row in self.data:
            row = [column.rstrip(';') for column in row]  # Remove ;
            row_0 = self.to_upper(row[0]) 
            row_3 = 'EUR'
            row_4 = self.to_upper(row[4])

            date_object = self.convert_timestamp(row[1])
            currency = self.to_upper(row[3])

            if currency == 'USD':
                share = self.usd_to_eur(row[2])
            else:
                share = float(row[2])

            rounded_share = self.round_share(share)
    
            cont += f'{row_0},{date_object},{rounded_share},{row_3},{row_4}\n'  # Select items
        
        with open(self.out_file, 'w') as f:
            f.write(cont)
            
        return cont

class Visualizer:
    def __init__(self, input_file):
        self.input_file = input_file

    def export(self):
        imp = Importer(self.input_file, 'data/data_output.csv')
        imp.transform()
        data = pd.read_csv('data/data_output.csv')
        
        data['DATE'] = pd.to_datetime(data['DATE'])
        
        plt.figure(figsize=(10, 6))
        for company, group in data.groupby('COMPANY'):
            plt.scatter(group['DATE'], group['SHARE'], label=company, alpha=0.7)

            # Annotate points with company and price information
            for i, row in group.iterrows():
                plt.text(row['DATE'], row['SHARE'] - 1, f"{row['SHARE']}", fontsize=8, ha='center')

                # Add company location above each company's points
                plt.text(row['DATE'], row['SHARE'], row['COMPANY_LOCATION'], fontsize=8, ha='center')

        plt.xlabel('Time')
        plt.ylabel('Shares (EUR)')

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.title('Shares over time')
        plt.xticks(rotation=45)  

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

        plt.tight_layout()
        plt.savefig('visualization/image.jpg')

vis = Visualizer('data/data.txt')
vis.export()

