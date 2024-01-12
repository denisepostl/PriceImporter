class Importer():
    """A class to read files."""

    def __init__(self, in_file):
        """
        Initializes the Importer class.

        Parameters:
        -----------
        in_file : str
            The path to the input file.
        """
        self.in_file = in_file 

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
            self.data = [line.strip().split(', ') for line in content] 
            return content
