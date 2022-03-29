
from models import *
import os
from sqlalchemy.orm import sessionmaker
import firebase_admin

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
connection_string = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
engine = create_engine(connection_string)

Session = sessionmaker()
read_session = Session(bind=engine)

## firebase config
cred = credentials.Certificate("veripol-156e4-firebase-adminsdk-84l91-d09a868558.json")
firebase_admin.initialize_app(cred)






national = read_session.query(Location).filter(Location.province==None,Location.municipality==None,Location.district==None,Location.barangay==None, Location.population==None).first()
cebu = read_session.query(Location).filter(Location.province=="CEBU").all()
lapu_lapu = read_session.query(Location).filter(Location.province=="CEBU", Location.municipality.contains("CITY OF LAPU-LAPU")).all()

candidate_list = []


candidacy = read_session.query(FiledCandidacy).filter(FiledCandidacy.location_id==national.id).all()
for can in candidacy:
    this_candidate = read_session.query(Candidate).filter(Candidate.id==can.candidate_id).first()
    candidate_list.append(this_candidate)


for c in cebu:
    candidacy = read_session.query(FiledCandidacy).filter(FiledCandidacy.location_id==c.id).all()
    for can in candidacy:
        this_candidate = read_session.query(Candidate).filter(Candidate.id==can.candidate_id).first()
        candidate_list.append(this_candidate)

for c in lapu_lapu:
    candidacy = read_session.query(FiledCandidacy).filter(FiledCandidacy.location_id==c.id).all()
    for can in candidacy:
        this_candidate = read_session.query(Candidate).filter(Candidate.id==can.candidate_id).first()
        candidate_list.append(this_candidate)

