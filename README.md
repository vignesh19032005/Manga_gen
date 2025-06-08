# 🧠🎨 AI Manga Creator

A Django-based web application that generates manga stories and visual panels using cutting-edge AI technology — powered by **Google Gemini** for story generation and **Stability AI** for art generation.

---

## 🚀 Features

* **📝 Story Generation**: Generate unique manga narratives with Google's **Gemini AI**.
* **🖼️ Manga Panel Creation**: Create stunning visual manga panels using **Stability AI**.
* **📚 Multiple Genres**: Supports a wide range of genres:

  * Action
  * Romance
  * Fantasy
  * Sci-Fi
  * Mystery
  * Comedy
  * Drama
  * Supernatural
* **🎨 Art Style Options**: Choose from multiple manga art styles:

  * Classic Anime
  * Modern Manga
  * Western Comics
  * Chibi Style
  * Semi-Realistic
* **🎯 Target Audience Selection**: Customize content for various age groups.
* **🔀 Story Element Mixing**: Mix and match tropes, plot twists, and archetypes.
* **🖥️ Interactive UI**: Real-time user-friendly interface with live feedback.
* **🖼️ Gallery View**: Browse and view previously generated panels and stories.

---

## 🛠️ Technologies Used

* **Backend**: Django 5.1
* **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5.3
* **AI Services**:

  * [Google Gemini 2.0](https://ai.google.dev/) — story generation
  * [Stability AI](https://stability.ai/) — image generation
* **Database**: SQLite3 (default; configurable)
* **Additional Libraries**:

  * jQuery 3.6.0
  * Font Awesome 6.0

---

## 📋 Prerequisites

* Python 3.11+
* pip
* Virtual environment setup (recommended)
* API Keys:

  * Google Gemini API Key
  * Stability AI API Key

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/vignesh19032005/ai-manga-creator.git
cd ai-manga-creator

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
touch .env
```

Add the following to your `.env` file:

```
GOOGLE_API_KEY=your_google_gemini_api_key
STABILITY_API_KEY=your_stability_ai_api_key
```

Then, run the app:

```bash
python manage.py runserver
```

Access the app at: [http://localhost:8000](http://localhost:8000)

---

## 🗂️ Project Structure

```
ai_manga_creator/
├── manga_ai/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── panels.html
│   │   ├── gallery.html
│   │   └── about.html
│   ├── views.py
│   ├── services/
│   │   └── MangaAIService.py
├── static/
├── panels/                # Generated panel images stored here
├── manage.py
└── .env
```

---

## 🚀 Usage

1. **Generate Story**:

   * Select your genre
   * Set story length and target audience
   * Enter a brief story premise
   * Choose story elements (e.g. plot twists, character types)
   * Click "Generate Manga" — AI will generate your story

2. **Generate Panels**:

   * Choose your preferred art style
   * Generate visual scenes from story content
   * Each panel generation may take 2–5 minutes

3. **Gallery View**:

   * Access the gallery to view all generated panels
   * Download or share your creations

---

## 🔒 API Keys & Security

Ensure your `.env` file contains the following:

```
GOOGLE_API_KEY=your_google_gemini_api_key
STABILITY_API_KEY=your_stability_ai_api_key
```

> **Important**: Never commit your `.env` file to version control. Add `.env` to your `.gitignore` file.

---

## 🌐 Project Components

### 🔧 AI Services — `MangaAIService.py`

* Integrates Google Gemini for natural language story generation
* Processes generated scenes for visual rendering
* Sends requests to Stability AI for panel generation

### 🖥️ Views — `views.py`

* `index`: Story generation form interface
* `panels`: Visual panel generation interface
* `gallery`: Displays saved/generated panels
* `about`: Project description and FAQ

### 🧩 Templates

* `base.html`: Base layout
* `index.html`: Story input and generation
* `panels.html`: Panel creation UI
* `gallery.html`: Panel viewing
* `about.html`: Credits and how-it-works

---

## 📌 Notes

* Generated images are saved in the `panels/` directory
* Default image resolution: **1024x1024 pixels**
* Currently supports **single-panel** generation per story chunk
* Panel generation may take 2–5 minutes depending on complexity

---

## 🤝 Contributing

We welcome contributions! Follow these steps:

1. Fork the repository
2. Create a new feature branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to GitHub (`git push origin feature-name`)
5. Open a Pull Request

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

* [Google Gemini AI](https://ai.google.dev/)
* [Stability AI](https://stability.ai/)
* [Django Web Framework](https://www.djangoproject.com/)
* [Bootstrap 5](https://getbootstrap.com/)
* [Font Awesome](https://fontawesome.com/)

---

> *“Creativity meets technology — generate your own manga universe in just a few clicks.”*

---

