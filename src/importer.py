from datetime import datetime

class Importer():
    """A class to read, transform, and export files."""

    def __init__(self, in_file, out_file):
        """
        Initializes the Importer class.

        Parameters:
        -----------
        in_file : str
            The path to the input file.
        out_file : str
            The path to the output file.
        """
        self.in_file = in_file 
        self.out_file = out_file
        self.data = []

    def read(self):
        """
        Reads the input file and stores the data in self.data.

        Returns:
        -----------
        list:
            A list of lines read from the input file.
        """
        with open(self.in_file, 'r') as f:
            content = f.readlines()
            self.data = [line.strip().split(', ') for line in content]  # Split lines
            return content
        
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
        self.read()
        cont = 'COMPANY,DATE,SHARE,CURRENCY,COMPANY_LOCATION\n'
        
        for row in self.data:
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
            
        return cont

