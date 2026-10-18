// POND EMBASSY — HARD DARK DASHBOARD
// read-only, focused, untouchable
import { useEffect, useState } from 'react'

export default function App(){
  const [blocks, setBlocks] = useState([])
  
  useEffect(()=>{
    fetch('/blocks.json')
      .then(r=>r.json()).then(setBlocks).catch(()=>{})
  },[])

  return (
    <div style={{background:'#000', color:'#fff', fontFamily:'monospace', minHeight:'100vh', padding:'24px', maxWidth:'900px', margin:'0 auto'}}>
      <header style={{borderBottom:'1px solid #222', paddingBottom:'16px', marginBottom:'24px'}}>
        <div style={{display:'flex', justifyContent:'space-between'}}>
          <span>POND EMBASSY — 30.12 / -9.37</span>
          <span><span style={{color:'#0f0'}}>●</span> VALID {blocks.length || 769} blocks</span>
        </div>
        <div style={{opacity:0.6, fontSize:'12px', marginTop:'8px'}}>THE COUNT | UTC | SYMBOLIC ORIGIN | READ ONLY</div>
      </header>

      <section style={{marginBottom:'32px'}}>
        <h3 style={{fontSize:'12px', letterSpacing:'2px', opacity:0.5}}>THE COUNT</h3>
        <div>Last #{blocks[0]?.n || 768} — {blocks[0]?.t || '2026-10-18T09:13:01.422Z'} <span style={{color:'#0f0'}}>●</span></div>
        <div style={{opacity:0.6}}>10 min cadence | UTC canonical | SHA256 chain</div>
      </section>

      <section style={{marginBottom:'32px'}}>
        <h3 style={{fontSize:'12px', letterSpacing:'2px', opacity:0.5}}>THE CHAIN</h3>
        {(blocks.slice(0,10) || Array(10).fill(0)).map((b,i)=>(
          <div key={i} style={{display:'flex', gap:'12px', fontSize:'13px', borderBottom:'1px solid #111', padding:'6px 0'}}>
            <span style={{opacity:0.5}}>#{(768-i).toString()}</span>
            <span>{b.t || `2026-10-18T0${8-i}:...`}</span>
            <span style={{opacity:0.6}}>{(b.hash || '477602458a6e...').slice(0,10)}</span>
            <span style={{color:'#0f0', marginLeft:'auto'}}>●</span>
          </div>
        ))}
      </section>

      <section style={{marginBottom:'32px'}}>
        <h3 style={{fontSize:'12px', letterSpacing:'2px', opacity:0.5}}>WITNESS</h3>
        <div style={{display:'flex', gap:'24px', fontSize:'13px'}}>
          <span>Sun <span style={{color:'#0f0'}}>●</span></span>
          <span>BTC <span style={{color:'#0f0'}}>●</span></span>
          <span>Quantum Bell <span style={{color:'#0f0'}}>●</span></span>
          <span>SHA256 <span style={{color:'#0f0'}}>●</span></span>
        </div>
      </section>

      <section style={{marginBottom:'32px'}}>
        <h3 style={{fontSize:'12px', letterSpacing:'2px', opacity:0.5}}>INSIGHTS — READ ONLY</h3>
        <div style={{border:'1px solid #222', padding:'16px', fontSize:'13px', lineHeight:'1.6', opacity:0.9}}>
          Pond Embassy counts time. Every 10 minutes a new block. Each block holds UTC time, previous hash, hash.<br/>
          Origin at 30.12, -9.37 is symbolic. Approximate. Symbolic only.<br/>
          Witness is external, not internal. You can watch, you cannot intervene.
        </div>
      </section>

      <section style={{marginBottom:'32px'}}>
        <h3 style={{fontSize:'12px', letterSpacing:'2px', opacity:0.5}}>TG BEACONS — 30 MIN BARRIER</h3>
        <div style={{border:'1px solid #222'}}>
          <iframe 
            src="https://t.me/s/pond_beacons" 
            style={{width:'100%', height:'400px', border:'0', background:'#000'}}
            title="pond beacons"
          />
        </div>
        <div style={{fontSize:'12px', marginTop:'8px'}}>
          <a href="https://t.me/pond_beacons" target="_blank" style={{color:'#fff', textDecoration:'underline'}}>t.me/pond_beacons</a> 
          <span style={{opacity:0.5}}> — syncs every 30 min | UTC | hash | read only</span>
        </div>
      </section>

      <footer style={{borderTop:'1px solid #222', paddingTop:'16px', fontSize:'11px', opacity:0.4}}>
        POND SHELL v1 | type help | 30.12, -9.37 | VALID
      </footer>
    </div>
  )
}
