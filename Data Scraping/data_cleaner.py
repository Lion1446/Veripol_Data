import csv
from models import *

rows = []
positions = []
locations = []
parties = []
candidates = []
filed_candidacies = []
counter = 0

with open('MergedDatasets_2.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        rows.append(row)

## Positions Algorithm
for i in range(len(rows)):
    if "#" in rows[i]:
        position = Position(rows[i-1][0]) 
        add_position = True
        for pos in positions:
            if position.name == pos.name:
                add_position = False
                position = pos
        if add_position:
            positions.append(position)


        add_location = True
        if (rows[i-2][0] == "PHILIPPINES"):       
            location = Location(None, None, None)
        else:
            this_location = rows[i-2][0].split(" - ")
            if len(this_location) == 1:
                location = Location(this_location[0], None, None)
            elif len(this_location) == 2:
                location = Location(this_location[0], this_location[1], None)
            elif len(this_location) == 3:
                location = Location(this_location[0], this_location[1], this_location[2])
            else:
                location = Location(None, None, None)
        for loc in locations:
            if loc.province == location.province and loc.municipality == location.municipality and loc.district == location.district:
                add_location = False
                location = loc
        if add_location:
            locations.append(location)
    else:
        try:
            ballot_number = int(rows[i][0])
            ballot_name = rows[i][1]
            sex = rows[i][2]
            name = rows[i][3]
            party = rows[i][4]
            if len(party) == 0:
                party = rows[i][5]
            
            add_party = True
            political_party = PoliticalParty(party)

            for par in parties:
                if political_party.name == par.name:
                    add_party = False
                    political_party = par
            if add_party:
                parties.append(political_party)


            add_candidate = True
            candidate = Candidate(name,sex, None)
            for can in candidates:
                if candidate.name == can.name and candidate.sex == can.sex and candidate.imgURL == can.imgURL:
                    add_candidate = False
                    candidate = can
            if add_candidate:
                candidates.append(candidate)

            add_filed_candidacy = True
            filed_candidacy = FiledCandidacy(candidate.id, ballot_number, ballot_name, political_party.id, location.id, position.id)
            for filed in filed_candidacies:
                if filed_candidacy.ballot_number == filed.ballot_number and filed_candidacy.ballot_name == filed.ballot_name and filed_candidacy.political_party_id == filed.political_party_id and filed_candidacy.location_id == filed.location_id and filed_candidacy.position_id == filed.position_id:
                    add_filed_candidacy = False
                    filed_candidacy = filed
            if add_filed_candidacy:
                filed_candidacies.append(filed_candidacy)
        except Exception as e:
            pass


header = ["ballot_number", "ballot_name", "sex", "name", "political_party", "img", "position", "province", "municipality", "district"]
with open('cleaned_data_2.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)

    for filed in filed_candidacies:
        candidate = next((x for x in candidates if x.id == filed.candidate_id), None)
        location = next((x for x in locations if x.id == filed.location_id), None)
        position = next((x for x in positions if x.id == filed.position_id), None)
        political_party = next((x for x in parties if x.id == filed.political_party_id), None)
        if candidate is not None and location is not None and position is not None and political_party is not None:
            this_row = [filed.ballot_number, filed.ballot_name, candidate.sex, candidate.name, political_party.name, candidate.imgURL , position.name, location.province, location.municipality, location.district]
            writer.writerow(this_row)

