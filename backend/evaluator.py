import difflib
def normalize(s): return ''.join(ch.lower() for ch in str(s) if ch.isalnum())
def evaluate_exam(exam, answers):
    results=[]; total=0; gained=0
    for q in exam:
        total+=1
        ans = answers.get(q['id'],'').strip()
        if q.get('type')=='mcq':
            score = 1.0 if ans.lower()==q.get('answer','').lower() else 0.0
        else:
            sim = difflib.SequenceMatcher(None, normalize(ans), normalize(q.get('answer',''))).ratio()
            score = 1.0 if sim>0.7 else 0.0
        results.append({'id':q['id'],'topic':q['topic'],'score':score,'student_ans':ans,'correct':q.get('answer','')})
        gained+=score
    return results, (gained/total if total else 0.0)
