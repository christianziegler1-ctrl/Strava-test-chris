"""
Strava Token Helfer - Einmalig ausfuehren!
Oeffnet automatisch den Browser und holt deinen Refresh Token.
"""
import http.server
import threading
import webbrowser
import urllib.parse
import urllib.request
import urllib.error
import json
import os

CLIENT_ID = "212390"
CLIENT_SECRET = "9a72a230557541966f235311c06afb92255238cd"
REDIRECT_URI = "http://localhost:8080/callback"
PORT = 8080

received_token = {}


AUTH_URL = (
    f"https://www.strava.com/oauth/authorize"
    f"?client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&response_type=code"
    f"&scope=read,activity:read_all"
)

SUCCESS_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Strava Verbindung erfolgreich!</title>
  <style>
    body {{ font-family: Arial, sans-serif; background: #f5f5f5;
           display: flex; justify-content: center; padding: 40px; }}
    .box {{ background: white; border-radius: 12px; padding: 40px;
            max-width: 600px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
    h1 {{ color: #FC4C02; }}
    .token {{ background: #f0f0f0; padding: 15px; border-radius: 8px;
              word-break: break-all; font-family: monospace; font-size: 14px; }}
    .hinweis {{ background: #fff3cd; padding: 15px; border-radius: 8px;
                margin-top: 20px; }}
  </style>
</head>
<body>
  <div class="box">
    <h1>Verbindung erfolgreich!</h1>
    <p>Dein Strava Refresh Token wurde abgerufen.</p>
    <p><strong>Kopiere diesen Token und schicke ihn an Claude:</strong></p>
    <div class="token">{refresh_token}</div>
    <div class="hinweis">
      <strong>Was tun?</strong><br>
      Markiere den Token oben, kopiere ihn (Strg+C),
      und fuege ihn in das Chat-Fenster mit Claude ein.
    </div>
    <p style="color: green; margin-top: 20px;">
      Du kannst dieses Browserfenster jetzt schliessen.
    </p>
  </div>
</body>
</html>
"""

ERROR_HTML = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Fehler</title></head>
<body style="font-family: Arial; padding: 40px;">
  <h1 style="color:red">Fehler aufgetreten</h1>
  <p>{error}</p>
  <p>Bitte schliesse dieses Fenster und starte das Script erneut.</p>
</body></html>
"""


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/callback" and "code" in params:
            code = params["code"][0]
            try:
                token_data = exchange_code(code)
                received_token["refresh_token"] = token_data["refresh_token"]
                received_token["access_token"] = token_data["access_token"]

                html = SUCCESS_HTML.format(
                    refresh_token=token_data["refresh_token"]
                )
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
            except Exception as e:
                html = ERROR_HTML.format(error=str(e))
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

        # Server stoppen
        threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        pass  # Keine Logs ausgeben


def exchange_code(code):
    data = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://www.strava.com/oauth/token",
        data=data,
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main():
    print("=" * 60)
    print("  STRAVA VERBINDUNG - Einmaliger Setup")
    print("=" * 60)
    print()
    print("Gleich oeffnet sich dein Browser.")
    print("Logge dich bei Strava ein und klicke auf 'Authorize'.")
    print()
    print("Warte auf Browser-Oeffnung...")

    server = http.server.HTTPServer(("localhost", PORT), CallbackHandler)

    threading.Timer(1.5, lambda: webbrowser.open(AUTH_URL)).start()

    print("Browser geoeffnet! Warte auf Strava-Freigabe...")
    server.serve_forever()

    if received_token:
        print()
        print("=" * 60)
        print("  ERFOLG! Dein Refresh Token:")
        print("=" * 60)
        print()
        print(received_token["refresh_token"])
        print()

        # Token in Datei speichern
        with open("mein_strava_token.txt", "w") as f:
            f.write(f"REFRESH_TOKEN={received_token['refresh_token']}\n")
            f.write(f"ACCESS_TOKEN={received_token['access_token']}\n")

        print("Token wurde auch in 'mein_strava_token.txt' gespeichert.")
        print()
        print("Bitte kopiere den Refresh Token und schicke ihn an Claude!")
        print()
    else:
        print("Fehler: Kein Token empfangen.")

    input("Druecke ENTER zum Beenden...")


if __name__ == "__main__":
    main()
