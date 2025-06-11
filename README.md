# Clinical Notes AI Agent

An intelligent system that processes clinical notes, extracts tasks, assesses risks, and generates actionable summaries using LangGraph and OpenAI's GPT-4.

## Overview

This application uses AI to analyze clinical notes and:
- Extracts key tasks and action items
- Assesses potential risks
- Generates a structured summary
- Creates a visual workflow graph
- Sends a PDF report via email

Built with LangGraph for workflow management and OpenAI's GPT-4 for natural language processing, this tool helps healthcare professionals quickly process and act on clinical documentation.

## Features

- **Intelligent Task Extraction**: Automatically identifies and categorizes tasks from clinical notes
- **Risk Assessment**: Evaluates potential risks and flags critical items
- **Visual Workflow**: Generates an interactive graph visualization of the processing pipeline
- **PDF Report Generation**: Creates a professional PDF summary of tasks and findings
- **Email Integration**: Sends reports directly to specified recipients via SendGrid
- **Web Interface**: User-friendly Flask web application for easy interaction

## Technical Stack

- **AI/ML**: OpenAI GPT-4, LangChain
- **Workflow**: LangGraph
- **Web Framework**: Flask
- **PDF Generation**: ReportLab
- **Email Service**: SendGrid
- **Visualization**: Graphviz
- **Environment Management**: Python-dotenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Clinical_Notes_AI_Agent.git
cd Clinical_Notes_AI_Agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install system dependencies:
```bash
# macOS
brew install graphviz

# Ubuntu/Debian
sudo apt-get install graphviz

# Windows
# Download and install from https://graphviz.org/download/
```

5. Create a `.env` file in the project root:
```env
# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# SendGrid Configuration
SENDGRID_API_KEY=your_sendgrid_api_key_here
SENDER_EMAIL=your_sender_email_here
DEFAULT_RECIPIENT=your_recipient_email_here

# File Configuration
PDF_FILENAME=task_summary.pdf
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter a clinical note in the text area and submit

4. View the processed results, including:
   - Extracted tasks
   - Risk assessment
   - Workflow visualization
   - PDF report (sent via email)

## Project Structure

```
Clinical_Notes_AI_Agent/
├── app.py                 # Flask application entry point
├── processor/            # Core processing modules
│   ├── pipeline.py       # LangGraph workflow definition
│   ├── extract.py        # Task extraction logic
│   ├── classify.py       # Risk classification
│   ├── emailer.py        # Email handling
│   ├── llm.py           # LLM configuration
│   ├── pdf_utils.py     # PDF generation
│   └── types.py         # Type definitions
├── static/              # Static files (graphs, etc.)
├── templates/           # HTML templates
├── requirements.txt     # Python dependencies
└── .env                # Environment variables (not in repo)
```

## Security

- API keys and sensitive information are stored in environment variables
- The `.env` file is git-ignored to prevent accidental commits
- A `.env.example` file is provided as a template

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- OpenAI for GPT-4
- LangChain team for the LangGraph framework
- SendGrid for email services
- The open-source community for various tools and libraries 