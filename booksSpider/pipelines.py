import csv
    
class CsvExportPipeline:
    """
    Export all data in a csv file.
    """
    def __init__(self):
        """
        Open the file, define and write field names.
        """
        self.csv_file = open('output.csv', 'w', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=['title', 'price', 'rank', 'availability', 'category', 'url'])
        self.csv_writer.writeheader()

    def process_item(self, item, spider):
        """
        Write items in the csv file
        """
        self.csv_writer.writerow(item)
        return item

    def close_spider(self, spider):
        """
        Close csv file when spider stop.
        """
        self.csv_file.close()
