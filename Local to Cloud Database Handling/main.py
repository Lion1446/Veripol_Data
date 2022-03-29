import os
from turtle import position
from unicodedata import name
from sqlalchemy.orm import sessionmaker
from models import *
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
import json

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
engine = create_engine(connection_string)

Session = sessionmaker()
read_session = Session(bind=engine)

## firebase config
cred = credentials.Certificate("veripol-156e4-firebase-adminsdk-84l91-d09a868558.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_searchkeys(search_string):
    search_keys = []
    for i in range(len(search_string)+1):
        for j in range(i, len(search_string)+1):
            if search_string[i:j].strip() != "," and search_string[i:j].strip() != "." and search_string[i:j].strip() != "":
                search_keys.append(search_string[i:j].strip().upper())
    return search_keys




def get_location_ids(province, municipality, barangay):
    locations = []

    ## get barangay
    try:
        barangay_id = read_session.query(Location).filter(Location.province.contains(province), Location.municipality.contains(municipality), Location.district==None,Location.barangay.contains(barangay)).first().id
        if barangay_id not in locations:
            locations.append(barangay_id)
    except:
        print("barangay")
        pass

    ## get municipality
    try:
        municipality_id = read_session.query(Location).filter(Location.province.contains(province), Location.municipality.contains(municipality), Location.district==None,Location.barangay==None).first().id
        if municipality_id not in locations:
            locations.append(municipality_id)
    except:
        print("municipality")
        pass

    ## get province
    try:
        province_id = read_session.query(Location).filter(Location.province.contains(province), Location.municipality==None, Location.district==None,Location.barangay==None).first().id
        if province_id not in locations:
            locations.append(province_id)
    except:
        print("province")
        pass

    ## get national
    try:
        national_id = read_session.query(Location).filter(Location.province==None, Location.municipality==None, Location.district==None,Location.barangay==None).first().id
        if national_id not in locations:
            locations.append(national_id)
    except:
        print("national")
        pass
    return locations

def get_candidateIDS_by_location(location_id):
    candidate_ids = []
    query = read_session.query(FiledCandidacy).filter(FiledCandidacy.location_id==location_id).all()
    for q in query:
        candidacy = q.to_map()
        candidate_ids.append(candidacy["candidate_id"])
    return candidate_ids


def get_candidate_candidacies(candidate_id):
    filed_candidacies = []
    candidacy_results = read_session.query(FiledCandidacy).filter(FiledCandidacy.candidate_id==candidate_id).all()
    for candidacy_result in candidacy_results:
        candidacy = candidacy_result.to_map()
        position = read_session.query(Position).filter(Position.id==candidacy["position_id"]).first().to_map()
        location = read_session.query(Location).filter(Location.id==candidacy["location_id"]).first().to_map()
        try:
            party = read_session.query(PoliticalParty).filter(PoliticalParty.id==candidacy["party_id"]).first().to_map()
        except:
            party = {"name": None}

        ## for each candidacy, get the result
        try:
            result = read_session.query(ElectionResult).filter(ElectionResult.candidacy_id==candidacy["id"]).first().to_map()
        except:
            result = {"is_elected": None, "rank": None, "vote_count": None, "date": None}

        filed_candidacy = {
            "candidacy_id": candidacy["id"],
            "position": position["name"],
            "location" : {
                "province": location["province"],
                "municipality": location["municipality"],
                "district": location["district"],
                "barangay": location["barangay"]
            },
            "political_party": party["name"],
            "ballot_number" : candidacy["ballot_number"],
            "ballot_name": candidacy["ballot_name"],
            "date": candidacy["date"],
            "is_elected": result["is_elected"],
            "rank": result["rank"],
            "vote_count": result["vote_count"],
            "result_date": result["date"]
        }
        filed_candidacies.append(filed_candidacy)
    return filed_candidacies

def get_candidate_housebills(candidate_id):
    housebills = []
    housebill_queries = read_session.query(HouseBills).filter(HouseBills.candidate_id==candidate_id).all()
    for housebill_query in housebill_queries:
        housebills.append(housebill_query.to_map())
    return housebills

def get_candidate_senatebills(candidate_id):
    senatebills = []
    senatebills_queries = read_session.query(SenateBills).filter(SenateBills.candidate_id==candidate_id).all()
    for senatebill_query in senatebills_queries:
        senatebills.append(senatebill_query.to_map())
    return senatebills
    


def get_candidates_with_location(province, municipality, barangay):  
    candidate_list = []

    ## get focused locations
    location_ids = get_location_ids(province, municipality, barangay)

    for location_id in location_ids:
        ## get candidates from that location
        candidates = get_candidateIDS_by_location(location_id)

        ## for each candidate, get filed candidacies
        for can in candidates:
            ## get candidate details
            candidate = read_session.query(Candidate).filter(Candidate.id==can).first().to_map()
            filed_candidacy_queries = read_session.query(FiledCandidacy).filter(FiledCandidacy.candidate_id==can).all()
            search_keys = []
            for filed_candidacy_query in filed_candidacy_queries:
                ballot_name = filed_candidacy_query.to_map()["ballot_name"]
                try:
                    search_keys.append(get_searchkeys(ballot_name[:ballot_name.index("(")-1]))
                except:
                    if ballot_name is not None:
                        search_keys.append(get_searchkeys(ballot_name))
            candidacy_details = {
                "id": candidate["id"], 
                "name": candidate["name"],
                "sex": candidate["sex"],
                "imgURL": candidate["imgURL"],
                "filed_candidacies": get_candidate_candidacies(candidate["id"]),
                "search_keys": search_keys,
                "housebills": get_candidate_housebills(candidate["id"]),    
                "senatebills": get_candidate_senatebills(candidate["id"])
            }
            candidate_list.append(candidacy_details)
    return candidate_list

def get_all_candidates():
    candidate_list = []

    ## get all locations
    location_ids = []
    location_queries = read_session.query(Location).all()
    for location_query in location_queries:
        location_ids.append(location_query.id) 

    for location_id in location_ids:
        ## get candidates from that location
        candidates = get_candidateIDS_by_location(location_id)

        ## for each candidate, get filed candidacies
        for can in candidates:
            ## get candidate details
            candidate = read_session.query(Candidate).filter(Candidate.id==can).first().to_map()
            filed_candidacy_queries = read_session.query(FiledCandidacy).filter(FiledCandidacy.candidate_id==can).all()
            search_keys = []
            for filed_candidacy_query in filed_candidacy_queries:
                ballot_name = filed_candidacy_query.to_map()["ballot_name"]
                try:
                    search_keys.append(get_searchkeys(ballot_name[:ballot_name.index("(")-1]))
                except:
                    if ballot_name is not None:
                        search_keys.append(get_searchkeys(ballot_name))
            candidacy_details = {
                "id": candidate["id"], 
                "name": candidate["name"],
                "sex": candidate["sex"],
                "imgURL": candidate["imgURL"],
                "filed_candidacies": get_candidate_candidacies(candidate["id"]),
                "search_keys": search_keys,
                "housebills": get_candidate_housebills(candidate["id"]),    
                "senatebills": get_candidate_senatebills(candidate["id"])
            }
            candidate_list.append(candidacy_details)
    return candidate_list

candidates = get_all_candidates()

with open('complete_data.json', 'w') as fout:
    json.dump(candidates , fout)




