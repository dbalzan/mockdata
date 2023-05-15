"""
Generate Persoon Data
	BSN - Generated from regex pattern
	Voorvoegsel and Achternaam - from dutch population file - http://www.naamkunde.net/?page_id=294
	Voornamen - from dutch population file - http://www.naamkunde.net/?page_id=293&vt_list_all=true
	Geboortedatum - random in range
	Initialen - Derived
"""
import csv
import random
from sys import argv
from datetime import datetime, timedelta

# Generate geboortedatum in the last 90 years
geboortedatum_range = {"start": datetime.today() - timedelta(weeks=90*52), "end": datetime.today()}
# The probability of voornaamen 2, 3 and 4 existing (1 = 100%, 0.5 = 50%, 0.1 = 10%)
voornaam_probability = [1, 0.5, 0.1, 0.1]

def main(num_records: int):
    # Read the achternamen csv 
    achternamen_data = read_population_csv ('achternaamen.csv')
    # Create the weighted surnames
    achternaam_relative_weights = ([float(x) for x in list(zip(*achternamen_data))[2]])
    weighted_achternaam = random.choices(achternamen_data, weights=achternaam_relative_weights, k=num_records)
    
    # Read the voornamen csv 
    voornamen_data = read_population_csv ('voornaamen.csv')
    # Create the weighted surnames
    voornaam_relative_weights = ([float(x) for x in list(zip(*voornamen_data))[1]])
    weighted_voornaam = random.choices(voornamen_data, weights=voornaam_relative_weights, k=num_records)

    # Generate the data
    with open('out.csv', 'w+', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_ALL)
        # Write the header
        csv_writer.writerow(["bsn", "voorvoegsel", "achternaam", "initialen", "voornamen", "voornaam_1", "voornaam_2", "voornaam_3", "voornaam_4", "geboortedatum"])
        for i in range(num_records):
            bsn = random.randrange(10000000, 999999999)
            achternaam = weighted_achternaam[i][1]
            voorvoegsel = weighted_achternaam[i][0]

            # Generate between 1 to 4 voornamen
            voornaamen = ["", "", "", ""] 
            # Add voornaamen based on probability
            for j in range(4):
                if (random.random() <= voornaam_probability[j]):
                    voornaamen[j] = weighted_voornaam[random.randrange(0, num_records)][0]
                else:
                    break
            
            # Generate and format a random geboortedatum in the specified range
            geboortedatum = geboortedatum_range['start'] + (geboortedatum_range['end'] - geboortedatum_range['start']) * random.random()
            geboortedatum = geboortedatum.strftime("%Y-%m-%d")
            
            # Derive combined_voornamen and initialen from voornamen
            combined_voornamen = " ".join(voornaamen).strip()
            initialen = ".".join(v[0] for v in combined_voornamen.split()) + "."
            
            # Write the row
            csv_writer.writerow([bsn, voorvoegsel, achternaam, initialen, combined_voornamen, voornaamen[0], voornaamen[1], voornaamen[2], voornaamen[3], geboortedatum])

# Read the population csv
def read_population_csv(filename):
    with open(filename, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        # Skip the header row
        headings = next(csv_reader)
        # Read the data and return it
        return list(csv_reader)

if __name__ == '__main__':
    # The number of records to generate
    num_records = 100000
    if len(argv) >= 2 and argv[1].isnumeric():
        num_records = int(argv[1])
    main(num_records)