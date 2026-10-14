package main
import (
 "bufio"
 "encoding/json"
 "fmt"
 "os"
 "os/exec"
)
func chainHeight() int {
 data, _ := os.ReadFile("chain.json")
 var chain []json.RawMessage
 json.Unmarshal(data, &chain)
 return len(chain)
}
func main(){
 height := chainHeight()
 fmt.Printf("🐸 bsh v2.1 — Pond Embassy — Count:%d\nChain height = time | 10min heartbeat\n\n", height)
 r := bufio.NewReader(os.Stdin)
 for {
  fmt.Printf("bsh:%d:~$ ", height)
  line, _ := r.ReadString('\n')
  if len(line)>0{line=line[:len(line)-1]}
  if line=="exit"{break}
  if line=="--origin"{fmt.Printf("Embassy:0.json Chain:%d\n", height); continue}
  if line==""{continue}
  c := exec.Command("bash","-c",line)
  c.Stdout=os.Stdout; c.Stderr=os.Stderr; c.Stdin=os.Stdin
  c.Run()
 }
}
