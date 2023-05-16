"""
Generate Identifier Data
	identification_number - 8 or 9 digit random number
    InactivatedDate - 10% random date (last two years) - 90% empty
    StartDate - random date (between four to two years ago)
    LastUpdatedDate - higher of inactivated or start date
    LastUpdatedUser - hardcoded "dummy_user"
    PartyType - 10% O and 90% P
    record_source - hardcoded "TestSet"	
"""
import csv
import random
from sys import argv
from datetime import datetime, timedelta

# InactivatedDate characteristics (20% - last two years)
inactivated_date_range = {"start": datetime.today() - timedelta(weeks=2*52), "end": datetime.today()}
inactivated_date_probability = 0.1

# Probability of generating an O instead of a P
party_type_probability = 0.1

# StartDate characteristics (100% - between four to two years ago)
start_date_range = {"start": datetime.today() - timedelta(weeks=4*52), "end": datetime.today() - timedelta(weeks=2*52)}

def main(num_records: int):
    # Generate the data
    with open('out.csv', 'w+', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_ALL)
        # Write the header
        csv_writer.writerow(["identification_number", "InactivatedDate", "StartDate", "LastUpdatedDate", "LastUpdatedUser", "PartyType", "record_source"])
        for i in range(num_records):
            identification_number = random.randrange(10000000, 999999999)

            if (random.random() <= inactivated_date_probability):
                inactivated_date = inactivated_date_range['start'] + (inactivated_date_range['end'] - inactivated_date_range['start']) * random.random()
                inactivated_date = inactivated_date.isoformat(sep=' ', timespec='milliseconds')
            else:
                inactivated_date = ""

            start_date = start_date_range['start'] + (start_date_range['end'] - start_date_range['start']) * random.random()
            start_date = start_date.isoformat(sep=' ', timespec='milliseconds')

            last_updated_date = start_date if (inactivated_date == "") else inactivated_date
            last_updated_user = "dummy_user"
            party_type = "O" if (random.random() <= party_type_probability) else "P"
            recourd_source = "TestSet"
            
            # Write the row
            csv_writer.writerow([identification_number, inactivated_date, start_date, last_updated_date, last_updated_user, party_type, recourd_source])

            # Report progress
            if (i % 1000000 == 0):
                print ("Writing record " + str(i)) 

if __name__ == '__main__':
    # The number of records to generate
    num_records = 10
    if len(argv) >= 2 and argv[1].isnumeric():
        num_records = int(argv[1])
    main(num_records)