import os
from flask import Flask, request, jsonify, make_response

app = Flask(__name__)

TOKEN_HTML = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <title>Bomb Game Client</title>
</head>
<body>
  <h1>Bomb Game Test Client</h1>

  <div id="login-section">
    <h2>Login</h2>
    <input id="email" type="email" placeholder="Email" />
    <input id="password" type="password" placeholder="Password" />
    <button id="signup">Sign up</button>
    <button id="login">Login</button>
  </div>

  <div id="user-section" style="display:none;">
    <h2>Logged in as: <span id="user-email"></span></h2>
    <button id="get-token">Get ID Token</button>
    <pre id="token-output"></pre>

    <h2>Call API Gateway</h2>
    <button id="call-api">Call /api/health</button>
    <pre id="api-output"></pre>
  </div>


  <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-auth-compat.js"></script>

  <script>

    const firebaseConfig = {
      apiKey: ${{ secrets.API_KEY }},
      authDomain: "alperenokur-sandbox-415013.firebaseapp.com",
      projectId: "alperenokur-sandbox-415013",
    };

    const gatewayBaseUrl = "https://alperenokur.com"; 

    // Firebase init
    firebase.initializeApp(firebaseConfig);
    const auth = firebase.auth();

    // UI elements
    const loginSection = document.getElementById('login-section');
    const userSection = document.getElementById('user-section');
    const userEmailSpan = document.getElementById('user-email');
    const tokenOutput = document.getElementById('token-output');
    const apiOutput = document.getElementById('api-output');

    document.getElementById('signup').onclick = async () => {
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      try {
        await auth.createUserWithEmailAndPassword(email, password);
        alert('User created and logged in');
      } catch (e) {
        alert('Sign up error: ' + e.message);
      }
    };

    document.getElementById('login').onclick = async () => {
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
      try {
        await auth.signInWithEmailAndPassword(email, password);
      } catch (e) {
        alert('Login error: ' + e.message);
      }
    };

    auth.onAuthStateChanged(user => {
      if (user) {
        loginSection.style.display = 'none';
        userSection.style.display = 'block';
        userEmailSpan.textContent = user.email;
      } else {
        loginSection.style.display = 'block';
        userSection.style.display = 'none';
      }
    });

    document.getElementById('get-token').onclick = async () => {
      const user = auth.currentUser;
      if (!user) {
        alert('Not logged in');
        return;
      }
      const token = await user.getIdToken(/* forceRefresh */ true);
      tokenOutput.textContent = token;
    };

    document.getElementById('call-api').onclick = async () => {
      const user = auth.currentUser;
      if (!user) {
        alert('Not logged in');
        return;
      }
      const token = await user.getIdToken(true);
      apiOutput.textContent = 'Calling...';

      try {
        const resp = await fetch(`${gatewayBaseUrl}/api/health`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        const text = await resp.text();
        apiOutput.textContent = `Status: ${resp.status}\n\n${text}`;
      } catch (e) {
        apiOutput.textContent = 'Error: ' + e.message;
      }
    };
  </script>
</body>
</html>
"""


@app.route("/")
def main():
    return TOKEN_HTML

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
