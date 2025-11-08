import React, {useState} from 'react';
import TopicSelector from './components/TopicSelector';
import ExamPanel from './components/ExamPanel';
import ResultSummary from './components/ResultSummary';
export default function App(){
    const [exam, setExam] = useState(null);
    const [results, setResults] = useState(null);
    const [topic, setTopic] = useState('matrices');
    return <div className='container'>
        <h1>Tutor RAG (local TinyLlama)</h1>
        <TopicSelector setExam={setExam} topic={topic} setTopic={setTopic}/>
        {exam ? <ExamPanel exam={exam} setResults={setResults} setExam={setExam}/> : null}
        {results ? <ResultSummary results={results}/> : null}
    </div>;
}
