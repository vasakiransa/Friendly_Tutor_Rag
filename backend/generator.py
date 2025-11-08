from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import os
from .config import LOCAL_MODEL
_pipe = None
def _init():
    global _pipe
    if _pipe is not None: return
    try:
        tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL)
        model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL, device_map='auto')
        _pipe = pipeline('text-generation', model=model, tokenizer=tokenizer, device_map='auto')
    except Exception as e:
        print('Local model init failed:', e)
        _pipe = None
def generate_questions(topic):
    _init()
    prompt = f"""Create 12 exam questions for the topic: {topic}. Include easy, medium and hard questions. Output as a JSON array of objects with id, topic, type, question, options (for mcq) and answer."""
    if _pipe is None:
        qs = []
        for i in range(12):
            qs.append({'id':f'q{i+1}','topic':topic,'type':'short','question':f'Sample question {i+1} on {topic}','answer':'sample'})
        return qs
    out = _pipe(prompt, max_new_tokens=400, do_sample=False)[0]['generated_text']
    try:
        import json, re
        m = re.search(r'\[.*\]', out, re.S)
        if m:
            qs = json.loads(m.group(0))
            return qs
    except Exception as e:
        print('Parse failed:', e)
    qs = []
    for i in range(12):
        qs.append({'id':f'q{i+1}','topic':topic,'type':'short','question':f'Sample question {i+1} on {topic}','answer':'sample'})
    return qs
def generate_notes(profile, level_hint, topics):
    _init()
    prompt = f"""You are a helpful tutor. Student level: {level_hint}. Profile: {profile}. Generate concise personalized notes and 3 practice problems for each topic in {topics}.""" 
    if _pipe is None:
        return [{'topic':t,'content':'Local model not available. Try enabling or use HF.'} for t in topics]
    out = _pipe(prompt, max_new_tokens=600, do_sample=True)[0]['generated_text']
    return [{'topic':t,'content':out} for t in topics]
