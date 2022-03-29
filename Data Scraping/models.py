import uuid


class Position:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())

class Location:
    def __init__(self, province, municipality, district):
        self.province = province
        self.municipality = municipality
        self.district = district
        self.id = str(uuid.uuid4())
    
class PoliticalParty:
    def __init__(self, name):
        self.name = name
        self.id = str(uuid.uuid4())

class Candidate:
    def __init__(self, name, sex, imgURL):
        self.name = name
        self.sex = sex
        self.imgURL = imgURL
        self.id = str(uuid.uuid4())

class FiledCandidacy:
    def __init__(self, candidate_id, ballot_number, ballot_name, political_party_id, location_id, position_id, year, is_elected, rank, vote_count, vote_percentage):
        self.candidate_id = candidate_id
        self.ballot_number = ballot_number
        self.ballot_name = ballot_name
        self.political_party_id = political_party_id
        self.location_id = location_id
        self.position_id = position_id
        self.year = year
        self.id = str(uuid.uuid4())

class ElectionResult:
    def __init__(self, candidate_id, candidacy_id, is_elected, rank, date, vote_count, vote_percentage):
        self.candidate_id = candidate_id
        self.candidacy_id = candidacy_id
        self.is_elected = is_elected
        self.rank = rank
        self.date = date
        self.vote_count = vote_count
        self.vote_percentage = vote_percentage
        self.id = str(uuid.uuid4())