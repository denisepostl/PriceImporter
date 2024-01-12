from importer import Importer
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

class Visualizer():
    """A class to visualize data."""

    def __init__(self, input_file, out_file):
        """
        Initializes the Visualizer class.

        Parameters:
        -----------
        input_file : str
            The path to the input file.
        output_file : str
            The path to the output file.
        data : list
            Save content of file in list.
        """
        self.input_file = input_file
        self.out_file = out_file 
        self.data = []

    def usd_to_eur(self, share):
        """
        Converts the given share value from USD to EUR.

        Parameters:
        -----------
        share : float
            The share value in USD.

        Returns:
        -----------
        float:
            The converted share value in EUR.
        """
        return float(share) * 0.91
        
    def to_upper(self, text):
        """
        Converts the given text to uppercase.

        Parameters:
        -----------
        text : str
            The input text.

        Returns:
        -----------
        str:
            The input text in uppercase.
        """
        return str(text).upper()
    
    def convert_timestamp(self, timestamp):
        """
        Converts the given timestamp to a datetime object.

        Parameters:
        -----------
        timestamp : int
            The timestamp to convert.

        Returns:
        -----------
        datetime:
            A datetime object corresponding to the given timestamp.
        """
        return datetime.fromtimestamp(int(timestamp))
    
    def round_share(self, share):
        """
        Rounds the given share value to two decimal places.

        Parameters:
        -----------
        share : float
            The share value to round.

        Returns:
        -----------
        float:
            The rounded share value.
        """
        return round(share, 2)
    
    def transform(self):
        """
        Transforms the data based on defined operations and exports it to the output file.

        Returns:
        -----------
        str:
            The transformed data.
        """
        imp = Importer(self.input_file)
        
        imp.read()
        
        cont = 'COMPANY,DATE,SHARE,CURRENCY,COMPANY_LOCATION\n'
        
        for row in imp.data:
            row = [column.rstrip(';') for column in row]  # Remove ;
            
            row_0 = self.to_upper(row[0]) 
            
            date_object = self.convert_timestamp(row[1])

            row_3 = 'EUR'

            currency = self.to_upper(row[3])
            if currency == 'USD':
                share = self.usd_to_eur(row[2])
            else:
                share = float(row[2])
            
            row_4 = self.to_upper(row[4])

            rounded_share = self.round_share(share)
    
            cont += f'{row_0},{date_object},{rounded_share},{row_3},{row_4}\n'  # Select items
        
        with open(self.out_file, 'w') as f:
            f.write(cont)
            
        self.data = imp.data  
        return cont

    def export(self):
        """
        Exports the visualized data to an image file.
        """
        self.transform()
        data = pd.read_csv(self.out_file)
        
        data['DATE'] = pd.to_datetime(data['DATE'])
        
        plt.figure(figsize=(10, 6))
        for company, group in data.groupby('COMPANY'):
            plt.scatter(group['DATE'], group['SHARE'], label=company, alpha=0.7)

            # Annotate points with company and price information
            for i, row in group.iterrows():
                plt.text(row['DATE'], row['SHARE'] - 1, f"{row['SHARE']}", fontsize=8, ha='center')

                # Add company location above each company's points
                plt.text(row['DATE'], row['SHARE'], row['COMPANY_LOCATION'], fontsize=8, ha='center')

        plt.xlabel('Datum')
        plt.ylabel('Aktienpreis (EUR)')

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.title('Aktienpreise über die Zeit')
        plt.xticks(rotation=45)  

        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

        plt.tight_layout()
        plt.savefig('visualization/image.jpg')

vis = Visualizer('data/data.csv', 'data/data_output.csv')
vis.export()
