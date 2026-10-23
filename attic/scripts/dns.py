import socket, struct
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.bind(('::1', 53))
print("DNS listening on [::1]:53")
while True:
  data, addr = s.recvfrom(512)
  # forward to 1.1.1.1
  f = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  f.settimeout(2)
  try:
    f.sendto(data, ('1.1.1.1', 53))
    resp,_ = f.recvfrom(512)
    s.sendto(resp, addr)
  except Exception as e:
    print(e)
  finally:
    f.close()
