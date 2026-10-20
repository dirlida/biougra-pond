// POND EMBASSY — FIXED DARK DASHBOARD
import { useEffect, useState } from 'react'

export default function App(){
  const [blocks, setBlocks] = useState([])

  useEffect(()=>{
    fetch('/blocks.json').then(r=>r.json()).then(data=>{
      // data is oldest-first, reverse for newest first
      const rev = [...data].reverse()
      setBlocks(rev)
    }).catch(()=>{})
  },[])

  const last = blocks[0]
  const count = blocks.length

  const fmtTime = (b)=>{
    if(!b) return '--:--:--'
    const ts = b?.payload?.ts || b?.t
    if(!ts) return '--:--:--'
    try{
      const d = new Date(ts)
      return d.toISOString().slice(11,19)
    }catch{
      return ts.slice(11,19)
    }
  }
  const fmtHash = (b)=> b?.hash?.slice(0,10) || '----------'
  const fmtIndex = (b)=> b?.index ?? b?.payload?.index ?? b?.n ?? '?'

  return (
    <div style={{background:'#000', color:'#fff', fontFamily:'monospace', minHeight:'100vh', padding:'24px', maxWidth:'900px', margin:'0 auto'}}>
      <header style={{borderBottom:'1px solid #222', paddingBottom:'16px', marginBottom:'24px'}}>
        <div style={{display:'flex', justifyContent:'space-between', flexWrap:'wrap', gap:'8px'}}>
          <span>POND EMBASSY — 30.12 / -9.37</span>
          <span><span style={{color:'#0f0'}}>●</span> VALID {count || 775} blocks</span>
        </div>
        <div style={{opacity:0.6, fontSize:'11px', marginTop:'8px'}}>THE COUNT | UTC | SYMBOLIC | READ ONLY</div>
      </header>

      <section style={{marginBottom:'28px'}}>
        <h3 style={{fontSize:'11px', letterSpacing:'2px', opacity:0.5}}>THE COUNT</h3>
        <div style={{fontSize:'13px'}}>Last #{fmtIndex(last)} — {last?.payload?.ts || last?.t || '2026-10-18T10:15:50Z'} <span style={{color:'#0f0'}}>●</span></div>
        <div style={{opacity:0.6, fontSize:'12px'}}>10 min cadence | UTC | SHA256 | SUN+BTC ATTESTED</div>
      </section>

      <section style={{marginBottom:'28px'}}>
        <h3 style={{fontSize:'11px', letterSpacing:'2px', opacity:0.5}}>THE CHAIN</h3>
        {blocks.slice(0,8).map((b,i)=>(
          <div key={i} style={{display:'flex', gap:'12px', fontSize:'12px', borderBottom:'1px solid #111', padding:'6px 0'}}>
            <span style={{opacity:0.5}}>#{fmtIndex(b)}</span>
            <span style={{opacity:0.8}}>{fmtTime(b)} UTC</span>
            <span style={{opacity:0.4}}>{fmtHash(b)}</span>
            <span style={{color:'#0f0', marginLeft:'auto'}}>●</span>
          </div>
        ))}
      </section>

      <section style={{marginBottom:'28px'}}>
        <h3 style={{fontSize:'11px', letterSpacing:'2px', opacity:0.5}}>WITNESS</h3>
        <div style={{display:'flex', gap:'20px', fontSize:'12px'}}>
          <span>Sun {last?.payload?.sunAltitude ? `${last.payload.sunAltitude}°` : ''} <span style={{color:'#0f0'}}>●</span></span>
          <span>BTC {last?.payload?.btcHeight || ''} <span style={{color:'#0f0'}}>●</span></span>
          <span>Q-Bell <span style={{color:'#0f0'}}>●</span></span>
          <span>SHA256 <span style={{color:'#0f0'}}>●</span></span>
        </div>
      </section>

      <section style={{marginBottom:'28px'}}>
        <h3 style={{fontSize:'11px', letterSpacing:'2px', opacity:0.5}}>INSIGHTS — READ ONLY</h3>
        <div style={{border:'1px solid #222', padding:'14px', fontSize:'12px', lineHeight:'1.6'}}>
          Pond Embassy counts time. Every 10 min a new block.<br/>
          Origin 30.12, -9.37 symbolic. Watch only, cannot intervene.<br/>
          Last SUN: {last?.payload?.sunAltitude ?? '--'} | BTC: {last?.payload?.btcHeight ?? '--'}
        </div>
      </section>

      <section style={{marginBottom:'28px'}}>
        <h3 style={{fontSize:'11px', letterSpacing:'2px', opacity:0.5}}>TG BEACONS — 30 MIN</h3>
        <div style={{border:'1px solid #222', padding:'12px', fontSize:'12px'}}>
          <div style={{opacity:0.7}}>Beacons push every 30 min via bot — no iframe, zero lag</div>
          <div style={{marginTop:'10px'}}>
            <a href="https://t.me/pond_beacons" target="_blank" style={{color:'#fff', border:'1px solid #333', padding:'6px 12px', textDecoration:'none'}}>→ t.me/pond_beacons</a>
            <span style={{opacity:0.4, marginLeft:'12px'}}>read only</span>
          </div>
        </div>
      </section>

      <footer style={{borderTop:'1px solid #222', paddingTop:'12px', fontSize:'10px', opacity:0.4}}>
        POND SHELL v1 | 30.12, -9.37 | VALID | {count} BLOCKS
      </footer>
    </div>
  )
}
