import React, {useState} from 'react';
import axios from 'axios';
export default function TopicSelector({setExam, topic, setTopic}){
    const [status,setStatus]=useState('');
    const doIngest = async ()=> {
        setStatus('Ingesting...');
        try{
            const res = await axios.post('http://localhost:8000/ingest', {topic});
            setStatus(JSON.stringify(res.data||res));
            const e = await axios.post('http://localhost:8000/exam', {topic});
            setExam(e.data.exam);
        }catch(err){
            setStatus('Error:'+err.message);
        }
    };
    return <div>
        <h3>Topic</h3>
        <input value={topic} onChange={e=>setTopic(e.target.value)}/>
        <button onClick={doIngest}>Ingest & Generate Exam</button>
        <div>{status}</div>
    </div>;
}
