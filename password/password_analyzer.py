from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

def analyze_password_strength(password):
    # Criteria definitions
    length_criteria = len(password) >= 8
    uppercase_criteria = bool(re.search(r'[A-Z]', password))
    lowercase_criteria = bool(re.search(r'[a-z]', password))
    digit_criteria = bool(re.search(r'\d', password))
    special_char_criteria = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    common_patterns = ["123456", "password", "qwerty", "letmein", "admin"]
    common_pattern_criteria = not any(pattern in password.lower() for pattern in common_patterns)

    # Calculate strength
    passed_criteria = sum([
        length_criteria,
        uppercase_criteria,
        lowercase_criteria,
        digit_criteria,
        special_char_criteria,
        common_pattern_criteria,
    ])

    # Recommendations
    recommendations = []
    if not length_criteria:
        recommendations.append("Use at least 8 characters.")
    if not uppercase_criteria:
        recommendations.append("Include at least one uppercase letter.")
    if not lowercase_criteria:
        recommendations.append("Include at least one lowercase letter.")
    if not digit_criteria:
        recommendations.append("Include at least one digit.")
    if not special_char_criteria:
        recommendations.append("Include at least one special character (!@#$%^&* etc.).")
    if not common_pattern_criteria:
        recommendations.append("Avoid common patterns or dictionary words.")

    # Strength levels
    if passed_criteria == 6:
        strength = "Strong"
    elif passed_criteria >= 4:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, recommendations

# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength Analyzer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 50px;
            background: linear-gradient(to right, #e66465, #9198e5);
            color: #fff;
            text-align: center;
        }
        .container {
            max-width: 600px;
            margin: auto;
            background: rgba(0, 0, 0, 0.7);
            padding: 20px;
            border-radius: 10px;
        }
        input {
            width: calc(100% - 40px);
            padding: 10px;
            margin: 10px 0;
            border: none;
            border-radius: 5px;
        }
        .password-container {
            position: relative;
        }
        .toggle-password {
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            cursor: pointer;
            font-size: 18px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .refresh {
            background-color: #f44336;
            margin-top: 10px;
        }
        .refresh:hover {
            background-color: #e53935;
        }
        .strong {
            color: #4CAF50;
        }
        .moderate {
            color: #FFC107;
        }
        .weak {
            color: #F44336;
        }
        .icon {
            font-size: 50px;
            margin: 20px 0;
        }
        .strong .icon {
            color: #4CAF50;
        }
        .moderate .icon {
            color: #FFC107;
        }
        .weak .icon {
            color: #F44336;
        }
    </style>
    <script>
        function togglePasswordVisibility() {
            const passwordInput = document.getElementById('password');
            const toggleIcon = document.getElementById('toggle-password');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                toggleIcon.textContent = '🙈';
            } else {
                passwordInput.type = 'password';
                toggleIcon.textContent = '👁️';
            }
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>Password Strength Analyzer</h1>
        <form method="POST">
            <label for="password">Enter your password:</label><br>
            <div class="password-container">
                <input type="password" id="password" name="password" required>
                <span id="toggle-password" class="toggle-password" onclick="togglePasswordVisibility()">👁️</span>
            </div>
            <button type="submit">Analyze</button>
        </form>
        <form method="GET">
            <button class="refresh" type="submit">Refresh</button>
        </form>
        {% if password %}
        <div class="{{ strength_class }}">
            <div class="icon">{% if strength == 'Weak' %}⚠️{% elif strength == 'Moderate' %}🟡{% else %}✅{% endif %}</div>
            <h2>Password Strength: <span>{{ strength }}</span></h2>
        </div>
        {% if recommendations %}
        <h3>Recommendations:</h3>
        <ul>
            {% for rec in recommendations %}
            <li>{{ rec }}</li>
            {% endfor %}
        </ul>
        {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def password_analyzer():
    password = None
    strength = None
    recommendations = []
    strength_class = ""

    if request.method == "POST":
        password = request.form.get("password")
        if password:
            strength, recommendations = analyze_password_strength(password)
            if strength == "Strong":
                strength_class = "strong"
            elif strength == "Moderate":
                strength_class = "moderate"
            else:
                strength_class = "weak"

    return render_template_string(HTML_TEMPLATE, password=password, strength=strength,
                                  recommendations=recommendations, strength_class=strength_class)

if __name__ == "__main__":
    app.run(debug=True)
