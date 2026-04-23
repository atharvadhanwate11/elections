# VoterGuide AI - Smart Election Assistant

**VoterGuide AI** is an interactive, intelligent assistant designed to simplify the complex journey of voting. Built for the Google Antigravity Challenge, it empowers first-time and experienced voters across two major democracies—the **United States** and **India**—by providing a clear, roadmap-driven approach to civic participation.

## 🗳️ Project Overview

**Chosen Vertical:** First-Time Voter Guidance & Civic Education.

Navigating election procedures can be overwhelming. VoterGuide AI reduces "choice paralysis" and procedural confusion by breaking down the journey into four distinct phases: Eligibility, Registration, Preparation, and Voting. By integrating **Google Gemini AI**, the assistant provides dynamic, context-aware answers to user queries, ensuring no voter is left with unanswered questions.

## 🚀 Key Features

- **Dual-Region Engine:** A seamless toggle between **USA 🇺🇸** and **India 🇮🇳** electoral logic. All roadmap content, links, and AI context update instantly.
- **Intelligent Roadmap:** A horizontally optimized 4-phase guide (Eligibility, Registration, Preparation, Voting Day) that adapts to the user's selected country.
- **HCI-First Checklist:** A tactile "Civic Checklist" featuring a real-time **Preparation Progress Bar**. Checking off tasks provides visual feedback and ensures 100% readiness.
- **ElectiBot (AI Assistant):** A floating, persistent assistant powered by **Google Gemini (gemini-flash-latest)**. It uses the user's active country and current phase to provide hyper-relevant advice.
- **Official Portal Integration:** Replaces unreliable search methods with direct, secure links to official government voter portals (`vote.org` and `eci.gov.in`).
- **Premium Aesthetics:** A state-of-the-art UI featuring glassmorphism, the 'Outfit' typography, smooth micro-animations, and a fully responsive grid system.

## 🛠️ Technology Stack

- **Frontend:** HTML5 (Semantic), Vanilla CSS3 (Custom Design System), JavaScript (ES6+).
- **Backend:** Python Flask.
- **AI Integration:** Google Generative AI SDK (Gemini API).
- **Icons & Fonts:** FontAwesome 6, Google Fonts (Outfit).
- **Dev Tools:** Git, Google Antigravity.

## 💡 Human-Computer Interaction (HCI) & Logic

1. **Context Loading:** When a user clicks a roadmap phase, the assistant doesn't just open; it greets the user with specific knowledge about that phase, reducing cognitive load.
2. **Dynamic Redirection:** The app understands that "Polling Stations" are handled differently in the US (state hubs) vs India (centralized search), and redirects accordingly via a single, smart "Access Official Portal" CTA.
3. **Progress Tracking:** The "Preparation Progress" bar uses psychological reinforcement (turning green at 100%) to encourage users to complete all steps before election day.
4. **Accessibility:** Integrated focus-visible ring styles and ARIA labels ensure the tool is usable for citizens with varying levels of technical ability.

## 🧠 Assumptions & Safety

- **Geoblocking Awareness:** Many official US and Indian voting portals use **strict geoblocking** for cybersecurity. Users located outside the target country (e.g., trying to access a US state site from India) may face access restrictions. Our assistant provides the official links, but accessibility is ultimately determined by government firewalls.
- **Official Documentation:** ElectiBot is programmed to prioritize official commission websites and reminds users that dates/deadlines are subject to change by local authorities.
- **Data Privacy:** This is a stateless application; voter progress is kept on the client side (Local Storage) for maximum privacy.

## ⚙️ Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/atharvadhanwate11/elections.git
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Gemini API Key:**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key
   ```
4. **Run the App:**
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:5000` in your browser.

---
*Developed by Atharva Dhanwate - Empowering democracy through intelligent design.*
