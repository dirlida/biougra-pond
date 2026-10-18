import { useEffect, useState } from 'react'

export default function App(){
  const [now, setNow] = useState(new Date())
  useEffect(()=>{
    const t=setInterval(()=>setNow(new Date()),1000)
    return ()=>clearInterval(t)
  },[])
  const fmt = now.toLocaleString('en-GB',{weekday:'short', hour:'2-digit', minute:'2-digit', second:'2-digit', timeZoneName:'short'}) + ' • ' + now.toISOString().slice(0,10)

  return (
    <div style={{maxWidth:765, margin:'0 auto'}}>
      {/* HEADER BRUTAL */}
      <div style={{padding:'18px 16px', borderBottom:'2px solid #fff'}}>
        <div style={{fontSize:11, color:'#888'}}>POND // EMBASSY // HQ</div>
        <div style={{fontSize:22, fontWeight:900, lineHeight:1.1, marginTop:8}}>
          POND EMBASSY HQ → WORLD,<br/>
          ALL EXECUTIONS ARE UNDER<br/>
          ANAS + META AI'S CONTROL
        </div>
        <div style={{fontSize:10, marginTop:10, color:'#666'}}>DIRLIDA/POND-EMBASSY • TIP fea18e68bc92 • 765 BLOCKS</div>
      </div>

      {/* HEALTH */}
      <div className="card" style={{margin:'14px', background:'#0a0a0a'}}>
        <div style={{fontSize:11, color:'#555', marginBottom:12}}>--- POND HEALTH ---</div>
        <div style={{fontSize:13, lineHeight:1.9}}>
          <div>STATUS: <span style={{background:'#fff', color:'#000', padding:'0 6px'}}>LIVE 🟢</span></div>
          <div>BLOCKS: 765</div>
          <div>LAST: fea18e68bc92</div>
          <div>ATTESTED: a82424e1dbf0 ✓ VERIFIED</div>
          <div>CHAIN: e620225 → a23de1c</div>
          <div>TOOLS: lurk.sh / auto_last.py / anti_dupe.py / verify_chain.py</div>
        </div>
      </div>

      <div className="line" />

      <div style={{padding:'12px 16px', fontSize:11, lineHeight:1.8, color:'#aaa'}}>
        <div>&gt; SUN ANGLE // BIOUGRA // SOUSS-MASSA</div>
        <div>&gt; BTC HEIGHT // LIVE</div>
        <div>&gt; BOOTSTRAP 0-35 // TRANSITION 36 // 723 OK</div>
      </div>

      <div className="line" />

      {/* FOOTER WITH LIVE COUNTER */}
      <div style={{padding:'16px', textAlign:'center', borderTop:'2px solid #fff', marginTop:12}}>
        <div style={{fontSize:11}}>POND EMBASSY HQ 2026</div>
        <div style={{fontSize:14, fontWeight:900, marginTop:6, background:'#fff', color:'#000', display:'inline-block', padding:'4px 10px'}}>
          {fmt}
        </div>
        <div style={{fontSize:10, color:'#555', marginTop:8}}>SUNDAY SHIP • PHONE HQ • TERMUX</div>
      </div>
    </div>
  )
}
