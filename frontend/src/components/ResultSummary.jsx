import React from 'react';
export default function ResultSummary({results}){ 
    if(!results) return null;
    return <div>
        <h3>Score: {(results.score*100).toFixed(1)}%</h3>
        <pre>{JSON.stringify(results.profile,null,2)}</pre>
        <div>{results.notes.map(n=> (<div key={n.topic}><h4>{n.topic}</h4><pre>{n.content}</pre></div>))}</div>
    </div>;
}
