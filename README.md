# Note-Taker Application

A **Streamlit-based application** for extracting, summarizing, and managing notes from web pages and YouTube videos. The application integrates with external shell scripts and provides an intuitive interface for efficient note-taking.

---

## Features

- **Web Page Note Taker**: Paste web content or provide a URL to extract and summarize notes.
- **YouTube Note Taker**: Enter YouTube video links for structured note extraction.
- **Customizable Patterns**: Choose between different summarization patterns (e.g., `summarize`, `extract_wisdom`).
- **Obsidian Integration**: Save notes directly into an Obsidian vault for easy organization.
- **Dockerized Deployment**: Easily deploy and run the app in any environment using Docker.

---

## Getting Started

### Running Locally with Streamlit

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app/app.py
   ```

   The app will be available in your browser at: [http://localhost:8501](http://localhost:8501).

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t note-taker-app .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8501:8501 note-taker-app
   ```

   Access the app in your browser at: [http://localhost:8501](http://localhost:8501).

---

## Directory Structure

```plaintext
project-root/
├── app/
│   ├── __init__.py               # Marks `app/` as a package
│   ├── app.py                    # Main entry point for the Streamlit app
│   ├── components/               # Custom reusable components
│   │   ├── __init__.py
│   │   ├── logo.py               # Code for displaying the logo
│   │   ├── tabs/                 # Tab-specific components
│   │   │   ├── youtube_tab.py    # YouTube Note-Taker tab code
│   │   │   ├── web_page_tab.py   # Web Page Note-Taker tab code
│   ├── utils.py                  # Shared utility functions
│   ├── config.py                 # Configuration constants
├── assets/                       # Static assets (images, logos, etc.)
│   ├── logo.png
├── scripts/                      # Shell scripts
│   ├── pbpaste_extract_and_save.sh
│   ├── web_extract_and_save.sh
│   ├── yt_extract_and_save.sh
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Docker configuration
├── README.md                     # Documentation

```

---

## Example Commands

### Streamlit Run Command
```bash
streamlit run app/app.py
```

- Launches the app in your browser.

### Docker Run Command
```bash
docker run -p 8501:8501 note-taker-app
```

- Starts the app in a containerized environment.

---

## Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

## License

This project is licensed under the TB

---

## Contact

For issues, questions, or suggestions:
- **Email**: tsoglog.uli@gmail.com
- **GitHub Issues**: [Open an Issue](https://github.com/tsogtbatjargal/note_taker/issues)

