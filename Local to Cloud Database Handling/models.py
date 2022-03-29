from click import echo
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, Float, Integer, Boolean, create_engine


Base = declarative_base()

class Position(Base):
    __tablename__ = "Position"

    id = Column(String(64), unique=True, primary_key=True)
    name = Column(String(64), nullable=False)
    def to_map(self):
        return {
            "id": self.id,
            "name": self.name 
        }


class Location(Base):
    __tablename__ = "Location"


    id = Column(String(64), unique=True, primary_key=True)
    province = Column(String(32))
    municipality = Column(String(32))
    district = Column(String(32))
    barangay = Column(String(32))
    population = Column(Integer)

    
    def to_map(self):
        return {
            "id": self.id,
            "province": self.province,
            "municipality": self.municipality,
            "district": self.district,
            "barangay": self.barangay,
            "population": {"2020": self.population}
        }
    
class PoliticalParty(Base):
    __tablename__ = "political_party"

    id = Column(String(64), unique=True, primary_key=True)
    name = Column(String(32), nullable=False)

    def to_map(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Candidate(Base):
    __tablename__ = "Candidate"

    id = Column(String(64), unique=True, primary_key=True)
    name = Column(String(64), nullable=False)
    sex = Column(String(10))
    imgURL = Column(String(128))

    def to_map(self):
        return {
            "id": self.id,
            "name": self.name,
            "sex": self.sex,
            "imgURL": self.imgURL
        }

class FiledCandidacy(Base):
    __tablename__ = "filed_candidacy"

    id = Column(String(64), unique=True, primary_key=True)
    candidate_id = Column(String(64), nullable=False)
    position_id = Column(String(64), nullable=False)
    location_id = Column(String(64), nullable=False)
    party_id = Column(String(64))
    ballot_number = Column(Integer)
    ballot_name = Column(String(64))
    date = Column(String(64))
        
    def to_map(self):
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "location_id": self.location_id,
            "position_id": self.position_id,
            "party_id": self.party_id,
            "ballot_number": self.ballot_number,
            "ballot_name": self.ballot_name,
            "date": self.date
        }

class ElectionResult(Base):
    __tablename__ = "election_result"

    id = Column(String(64), unique=True, primary_key=True)
    candidate_id = Column(String(64), nullable=False)
    candidacy_id = Column(String(64), nullable=False)
    is_elected = Column(Boolean)
    rank = Column(Integer)
    vote_count = Column(Integer)
    vote_percentage = Column(Float)
    date = Column(String(64))

    def to_map(self):
        return {
            "id": self.id,
            "candidate_id": self.candidate_id,
            "candidacy_id": self.candidacy_id,
            "is_elected": self.is_elected,
            "rank": self.rank,
            "vote_count": self.vote_count,
            "vote_percentage": self.vote_percentage,
            "date": self.date
        }


class SenateBills(Base):
    __tablename__ = "senate_bills"

    id = Column(String(64), unique=True, primary_key=True)
    candidate_id = Column(String(64))
    congress = Column(String(8))
    senatebill_number = Column(String(10))
    title = Column(Text)
    long_title = Column(Text)
    date_filed = Column(String(16))
    principal_authors = Column(Text)
    significance = Column(String(32))
    bill_status = Column(Text)

    def to_map(self):
        return {
            "id": self.id,
            "congress": self.congress,
            "senatebill_number": self.senatebill_number,
            "title": self.title,
            "long_title": self.long_title,
            "date_filed": self.date_filed,
            "principal_authors": self.principal_authors,
            "significance": self.significance,
            "bill_status": self.bill_status
        }

    def from_map(self, values):
        try: 
            if values["candidate_id"] == "":
                self.candidate_id = None
            else: 
                self.candidate_id = values["candidate_id"]
        except: 
                self.candidate_id = None
        try: 
            if values["congress"] == "":
                self.congress = None
            else: 
                self.congress = values["congress"]
        except: 
            self.congress = None
        try: 
            if values["senatebill_number"] == "":
                self.senatebill_number = None
            else: 
                self.senatebill_number = values["senatebill_number"]
        except: 
            self.senatebill_number = None
        try: 
            if values["title"] == "":
                self.title = None
            else: 
                self.title = values["title"]
        except: 
            self.title = None
        try: 
            if values["long_title"] == "":
                self.long_title = None
            else: 
                self.long_title = values["long_title"]
        except: 
            self.long_title = None
        try: 
            if values["date_filed"] == "":
                self.date_filed = None
            else: 
                self.date_filed = values["date_filed"]
        except: 
            self.date_filed = None
        try: 
            if values["principal_author/s"] == "":
                self.principal_authors = None
            else: 
                self.principal_authors = values["principal_author/s"]
        except: 
            self.principal_authors = None
        try: 
            if values["significance"] == "":
                self.significance = None
            else: 
                self.significance = values["significance"]
        except: 
            self.significance = None
        try: 
            if values["bill_status"] == "":
                self.bill_status = None
            else: 
                self.bill_status = values["bill_status"]
        except: 
            self.bill_status = None

class HouseBills(Base):
    __tablename__ = "house_bills"

    id = Column(String(64), unique=True, primary_key=True)
    candidate_id = Column(String(64))
    housebill_number = Column(String(10))
    significance = Column(String(32))
    date_filed = Column(String(16))
    full_title = Column(Text)
    principal_authors = Column(Text)
    date_read = Column(String(16))
    primary_referral = Column(Text)
    bill_status = Column(Text)
    mother_bill_status = Column(Text)
    date_approved_on_second_reading = Column(String(16))
    date_approved_on_third_reading = Column(String(16))
    senate_bill_counterpart = Column(Text)
    date_acted_upon_by_the_president = Column(String(16))
    republic_act_no = Column(String(16))
    congress = Column(String(8))

    def to_map(self):
        date_reads = []
        if self.date_read is not None:
            date_reads.append(self.date_read)
        if self.date_approved_on_second_reading is not None:
            date_reads.append(self.date_approved_on_second_reading)
        if self.date_approved_on_third_reading is not None:
            date_reads.append(self.date_approved_on_third_reading)
        return {
            "bill_id": self.id,
            "congress": self.congress,
            "HB_number": self.housebill_number,
            "title": self.full_title,
            "date_filed" : self.date_filed,
            "principal_authors:" : self.principal_authors,
            "significance": self.significance,
            "bill_status": self.bill_status,
            "motherbill_status": self.mother_bill_status,
            "date_read": date_reads,
            "primary_referal": self.primary_referral,
            "senatebill_counterpart": self.senate_bill_counterpart,
            "date_acted_by_president": self.date_acted_upon_by_the_president,
            "republic_act_no": self.republic_act_no
        }

    def from_map(self, values):
        try:
            if values["candidate_id"] == "":
                self.candidate_id = None
            else:
                self.candidate_id = values["candidate_id"]
        except:
            self.candidate_id = None
        try:
            self.housebill_number = values["house_bill_number"]
        except:
            self.housebill_number = None
        try:
            self.significance = values["significance"]
        except:
            self.significance = None
        try:
            self.date_filed = values["date_filed"]
        except:
            self.date_filed = None
        try:
            self.full_title = values["full_title"]
        except:
            self.full_title = None
        try:
            self.principal_authors = values["principal_author/s"]
        except:
            self.principal_authors = None
        try:
            self.date_read = values["date_read"]
        except:
            self.date_read = None
        try:
            self.primary_referral = values["primary_referral"]
        except:
            self.primary_referral = None
        try:
            self.bill_status = values["bill_status"]
        except:
            self.bill_status = None
        try:
            self.mother_bill_status = values["mother_bill_status"]
        except:
            self.mother_bill_status = None
        try:
            self.date_approved_on_second_reading = values["date_approved_on_second_reading"]
        except:
            self.date_approved_on_second_reading = None
        try:
            self.date_approved_on_third_reading = values["date_approved_on_third_reading"]
        except:
            self.date_approved_on_third_reading = None
        try:
            self.senate_bill_counterpart = values["senate_bill_counterpart"]
        except:
            self.senate_bill_counterpart = None
        try:
            self.date_acted_upon_by_the_president = values["date_acted_upon_by_the_president"]
        except:
            self.date_acted_upon_by_the_president = None
        try:
            self.republic_act_no = values["republic_act_no"]
        except:
            self.republic_act_no = None
        try:
            self.congress = values["congress"]
        except:
            self.congress = None



