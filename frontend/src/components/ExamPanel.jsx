import React, {useState} from 'react';
import axios from 'axios';
export default function ExamPanel({exam, setResults, setExam}){
    const [answers,setAnswers]=useState({});
    const submit = async ()=>{
        const res = await axios.post('http://localhost:8000/submit', {exam, answers, level_hint: 'beginner'});
        setResults(res.data);
        setExam(null);
    };
    return <div>
        <h3>Exam</h3>
        {exam.map(q=>(
            <div key={q.id}><p>{q.question}</p>
            {q.type==='mcq' ? q.options.map((o,i)=><label key={i}><input type="radio" name={q.id} value={o} onChange={e=>setAnswers({...answers,[q.id]:e.target.value})}/> {o}</label>) : <input onChange={e=>setAnswers({...answers,[q.id]:e.target.value})}/>}
            </div>
        ))}
        <button onClick={submit}>Submit</button>
    </div>;
}
