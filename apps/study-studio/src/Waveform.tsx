import {useState} from 'react';
export default function Waveform({compact=false}:{compact?:boolean}){
  const [t,setT]=useState(5);
  const X=(n:number)=>40+(n+1)*43,Y=(n:number)=>174-n*21;
  const path=(fn:(n:number)=>number)=>Array.from({length:81},(_,i)=>{const n=-1+i*.1;return `${i?'L':'M'} ${X(n)} ${Y(fn(n))}`}).join(' ');
  return <div className={'waveform '+(compact?'compact':'')}>
    <svg viewBox="0 0 420 215" role="img" aria-label="Two ramps with equal slopes have different heights; their difference forms a plateau at height two.">
      {[0,1,2,3,4,5,6,7].map(n=><g key={n}><line x1="32" y1={Y(n)} x2="390" y2={Y(n)} stroke="#e4e9e0"/><text x="20" y={Y(n)+4}>{n}</text></g>)}
      {[0,1,2,3,4,5,6,7].map(n=><g key={n}><line x1={X(n)} y1="18" x2={X(n)} y2="178" stroke="#edf0e9"/><text x={X(n)-3} y="196">{n}</text></g>)}
      <line x1="32" y1="174" x2="394" y2="174" stroke="#acb6a9"/>
      <path d={path(n=>Math.max(n,0))} fill="none" stroke="#b4bba8" strokeWidth="2" strokeDasharray="5 4"/>
      <path d={path(n=>Math.max(n-2,0))} fill="none" stroke="#c29559" strokeWidth="2" strokeDasharray="5 4"/>
      <path d={path(n=>Math.max(n,0)-Math.max(n-2,0))} fill="none" stroke="#246c55" strokeWidth="3.5"/>
      {!compact&&<><line x1={X(t)} y1="18" x2={X(t)} y2="178" stroke="#7c9c8b" strokeDasharray="3 4"/><circle cx={X(t)} cy={Y(Math.max(t,0)-Math.max(t-2,0))} r="5" fill="#246c55" stroke="white" strokeWidth="2"/></>}
      <text x="394" y="197">t</text>
    </svg>
    <div className="legend"><span><i className="line sage"/> r(t)</span><span><i className="line amber"/> r(t − 2)</span><span><i className="line green"/> their difference</span></div>
    {!compact&&<><label className="range-label" htmlFor="time-slider">Compare at t = {t}<span>x(t) = {(Math.max(t,0)-Math.max(t-2,0)).toFixed(1)}</span></label><input id="time-slider" aria-label="Time on waveform" type="range" min="0" max="6" step="0.5" value={t} onChange={e=>setT(Number(e.target.value))}/><p className="figure-caption">Move through time: r(t) = {t.toFixed(1)}, r(t − 2) = {Math.max(t-2,0).toFixed(1)}. Compare values, not just slopes.</p></>}
  </div>;
}
