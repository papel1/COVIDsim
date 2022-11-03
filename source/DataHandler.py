import pandas as pd


class DataHandler:
    """
    Handles basic read / write operations from/to a selected dataset.
    """

    def __init__(self, data_folder: str, output_folder: str):
        """__init__

        Args:
            data_folder (str): Folder to check for input data. 
            output_folder (str): Folder to export the data.
        """
        self.data_folder = data_folder
        self.output_folder = output_folder

    def to_xlsx(self, data_container, name: str):
        """Write data to xlsx

        Args:
            data_container (_type_): The container we would like to export.
            name (str): The name of the file we would like to use during export.
        """
        df = pd.DataFrame(data=data_container)
        df.to_excel(self.output_folder + f"{name}.xlsx")

    def from_xlsx(self, name: str) -> pd.DataFrame:
        """Read data from xlsx.

        Args:
            name (str): The name of the file we would like to read.

        Returns:
            pd.DataFrame: The read xls content.
        """
        return pd.read_excel(self.data_folder + f"{name}.xlsx")
