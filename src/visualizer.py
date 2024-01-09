from importer import Importer
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Visualizer():
    """A class to visualize data."""

    def __init__(self, input_file):
        """
        Initializes the Visualizer class.

        Parameters:
        -----------
        input_file : str
            The path to the input file.
        """
        self.input_file = input_file

    def export(self):
        """
        Exports the visualized data to an image file.
        """
        imp = Importer(self.input_file, '../data/data_output.csv')
        imp.transform()
        data = pd.read_csv('../data/data_output.csv')
        
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
        plt.savefig('../visualization/image.jpg')

vis = Visualizer('../data/data.txt')
vis.export()

