from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .ingest import ingest_topic
from .generator import generate_questions, generate_notes
from .evaluator import evaluate_exam
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:5173'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
class IngestReq(BaseModel):
    topic: str
class ExamReq(BaseModel):
    topic: str
class SubmitReq(BaseModel):
    exam: list
    answers: dict
    level_hint: str
@app.post('/ingest')
def api_ingest(req: IngestReq):
    return ingest_topic(req.topic)
@app.post('/exam')
def api_exam(req: ExamReq):
    qs = generate_questions(req.topic)
    return {'exam': qs}
@app.post('/submit')
def api_submit(req: SubmitReq):
    results, score = evaluate_exam(req.exam, req.answers)
    profile = {}
    for r in results:
        profile.setdefault(r['topic'], []).append(r['score'])
    profile = {k: sum(v)/len(v) for k,v in profile.items()}
    notes = generate_notes(profile, req.level_hint, list(profile.keys()))
    return {'results':results,'score':score,'profile':profile,'notes':notes}
