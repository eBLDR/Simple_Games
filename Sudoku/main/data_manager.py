import csv


class DataManager:
    def __init__(self):
        self.filename = 'sudoku_data.csv'
        self.data = None

    def read_data(self, size=9):
        with open(self.filename, 'r') as csv_file:
            reader = csv.reader(csv_file)
            self.data = [[number if number != '0' else '' for number in row] for row in reader]
        self.validate_data(size)
        return self.data

    def validate_data(self, size):
        assert isinstance(self.data, (list, tuple)) is True, 'Wrong data format, must be list or tuple.'
        assert len(self.data[0]) != 0, 'Data is empty.'
        assert len(self.data) == len(self.data[0]) == size, 'Incomplete data.'
