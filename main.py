import os
from flask import Flask

app = Flask(__name__)

GAME_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8" />
  <title>Buton Oyunu</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    body {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle at top, #1f2937, #020617);
      color: #f9fafb;
    }

    .container {
      text-align: center;
      padding: 2rem 3rem;
      border-radius: 1.5rem;
      background: rgba(15, 23, 42, 0.9);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
      max-width: 480px;
      width: 100%;
    }

    h1 {
      font-size: 1.8rem;
      margin-bottom: 0.75rem;
    }

    p.subtitle {
      font-size: 0.95rem;
      opacity: 0.8;
      margin-bottom: 1.5rem;
    }

    .buttons-wrapper {
      display: flex;
      justify-content: center;
      gap: 1.5rem;
      margin: 1.5rem 0 1rem 0;
    }

    .circle-btn {
      width: 90px;
      height: 90px;
      border-radius: 999px;
      border: none;
      cursor: pointer;
      font-size: 1.2rem;
      font-weight: 600;
      background: #0f172a;
      color: #e5e7eb;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
      transition:
        transform 0.15s ease,
        box-shadow 0.15s ease,
        background 0.15s ease,
        opacity 0.15s ease;
    }

    .circle-btn:hover {
      transform: translateY(-4px);
      box-shadow: 0 14px 24px rgba(0, 0, 0, 0.6);
    }

    .circle-btn:active {
      transform: translateY(0);
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }

    .circle-btn.correct {
      background: #16a34a;
    }

    .circle-btn.wrong {
      background: #b91c1c;
    }

    .status {
      min-height: 1.5rem;
      margin-bottom: 1rem;
      font-weight: 600;
    }

    .status.success {
      color: #22c55e;
    }

    .status.error {
      color: #f97316;
    }

    .reset-info {
      font-size: 0.8rem;
      opacity: 0.7;
    }

    .highlight {
      color: #38bdf8;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Butonu Seç 🎯</h1>
    <p class="subtitle">
      3 butondan sadece <span class="highlight">birinde +</span> var, diğerlerinde <span class="highlight">-</span>.<br/>
      Doğru butonu seçebilir misin?
    </p>

    <div class="buttons-wrapper">
      <button class="circle-btn" data-index="0">1</button>
      <button class="circle-btn" data-index="1">2</button>
      <button class="circle-btn" data-index="2">3</button>
    </div>

    <div id="status" class="status"></div>
    <div class="reset-info">
      Her seçimden sonra oyun otomatik olarak yeniden karışır 🔄
    </div>
  </div>

  <script>
    const buttons = document.querySelectorAll(".circle-btn");
    const statusEl = document.getElementById("status");

    let correctIndex = null;

    function randomizeCorrectButton() {
      correctIndex = Math.floor(Math.random() * 3);

      buttons.forEach((btn) => {
        btn.classList.remove("correct", "wrong");
        btn.disabled = false;
        btn.style.opacity = "1";
      });

      statusEl.textContent = "";
      statusEl.className = "status";
    }

    function handleClick(event) {
      const clickedBtn = event.currentTarget;
      const clickedIndex = Number(clickedBtn.dataset.index);

      buttons.forEach((btn) => {
        btn.disabled = true;
        btn.style.opacity = "0.75";
      });

      if (clickedIndex === correctIndex) {
        clickedBtn.classList.add("correct");
        statusEl.textContent = "Tebrikler! Doğru butonu seçtin 🎉";
        statusEl.classList.add("success");
      } else {
        clickedBtn.classList.add("wrong");
        statusEl.textContent = "Tekrar dene! 🙃";
        statusEl.classList.add("error");
      }

      setTimeout(() => {
        randomizeCorrectButton();
      }, 1200);
    }

    buttons.forEach((btn) => {
      btn.addEventListener("click", handleClick);
    });

    randomizeCorrectButton();
  </script>
</body>
</html>
"""

@app.route("/")
def game():
  return GAME_HTML

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port)
