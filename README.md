# AI Sprint Estimator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](https://github.com/your-org/ai-sprint-estimator)
[![LLM](https://img.shields.io/badge/LLM-LM%20Studio%20Compatible-orange.svg)](https://lmstudio.ai)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Passing-green.svg)](https://github.com/your-org/ai-sprint-estimator)

A Python-based AI framework for evaluating local large language models (LLMs) in Agile sprint effort estimation. This project provides a reproducible proof of concept (PoC) pipeline that produces benchmarkable, explainable outputs in a privacy-preserving setup using local LLM integration.

## 🚀 Features

- **🤖 AI-Powered Estimation**: Local LLM integration with LM Studio and compatible models
- **📊 Comprehensive Benchmarking**: Multi-trial consistency analysis with statistical metrics
- **🔒 Privacy-Preserving**: Local LLM evaluation with no data transmission to external services
- **📈 Detailed Analytics**: Response latency, parse success rates, and estimation accuracy
- **🎯 Structured Outputs**: JSON-based responses with estimates, reasoning, and confidence levels
- **📋 Reproducible Results**: Complete pipeline with saved raw, parsed, and aggregated data
- **🧪 Academic Ready**: Designed for research papers with comprehensive evaluation metrics

## 🏗️ Architecture

The AI Sprint Estimator follows a modular architecture with the following components:

- **`src/model_inference.py`**: LLM API integration and communication layer
- **`src/prompt_design.py`**: Structured prompt templates for consistent JSON outputs
- **`src/evaluation.py`**: Comprehensive benchmarking and statistical analysis
- **`src/baseline.py`**: Heuristic estimation baseline for comparison
- **`main.py`**: Main pipeline orchestration and execution
- **`chart_generator.py`**: Visualization and chart generation utilities

## 📋 Prerequisites

- Python 3.8+
- **LM Studio** or compatible local LLM server
- Required Python packages (see requirements.txt)
- Docker Desktop (optional)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/your-org/ai-sprint-estimator.git
cd ai-sprint-estimator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup LM Studio

1. **Install LM Studio**: Download from [lmstudio.ai](https://lmstudio.ai)
2. **Download a compatible model**: e.g., `gpt-oss-7b-instruct` or similar
3. **Start LM Studio Server**: Run on `http://localhost:1234`

### 4. Configure Environment (Optional)

```bash
export LMSTUDIO_HOST="http://127.0.0.1:1234"
export LMSTUDIO_API_KEY="lm-studio"
export LM_MODEL="gpt-oss-7b-instruct"
```

### 5. Run the Pipeline

```bash
python main.py
```

## 📖 Usage Examples

### Basic Pipeline Execution

```python
from main import run_pipeline

# Run with default 5 trials per story
run_pipeline(trials=5)
```

### Custom Configuration

```python
# Modify trials per story
run_pipeline(trials=10)

# The pipeline will:
# 1. Load user stories from data/user_stories.csv
# 2. Run multiple estimation trials per story
# 3. Generate structured JSON responses
# 4. Save results to results/model_outputs.csv
# 5. Calculate benchmark metrics
```

### Direct Model Query

```python
from src.model_inference import query_model

story = "As a user, I want to reset my password via email so that I can regain account access."
raw_response, latency = query_model(story)
print(f"Response time: {latency:.2f}s")
print(f"Raw output: {raw_response}")
```

## 📊 Results & Outputs

### Generated Files

#### `results/model_outputs.csv`
Contains detailed trial data:
- `story_id`: Story identifier
- `trial`: Trial number (0-4 by default)
- `story`: Full user story text
- `raw_output`: Raw JSON response from LLM
- `response_time`: Latency in seconds
- `estimate`: Parsed story point estimate

#### `results/benchmark_summary.json`
Contains aggregated metrics:
- **Per-story statistics**: Mean, std, coefficient of variation, consistency
- **Global statistics**: Overall mean, std, percentiles across all stories

### Example Output

```
=== BENCHMARK SUMMARY ===
Global Statistics:
  Mean estimate: 4.06
  Standard deviation: 2.73
  Median (p50): 4.00
  90th percentile: 8.10

Per-Story Statistics:
  Story 1: mean=3.40, std=1.20, consistency=0.40
  Story 2: mean=7.80, std=1.33, consistency=0.60
  ...
```

## 🧪 Testing & Evaluation

### Comprehensive Metrics

The evaluation system provides:

- **Estimation Consistency**: Mean, standard deviation, coefficient of variation
- **Response Latency**: Average and percentile response times
- **Parse Success Rate**: JSON parsing reliability
- **Confidence Analysis**: Model confidence level distribution
- **Baseline Comparison**: Agreement with heuristic estimates

### Running Evaluations

```bash
# Run the complete pipeline
python main.py

# Generate additional charts and visualizations
python chart_generator.py
```

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the image
docker build -t ai-sprint-estimator .

# Run the container
docker run -p 8000:8000 ai-sprint-estimator
```

### Docker Compose

```bash
docker-compose up --build
```

## 📈 Performance & Monitoring

- **Structured Logging**: Detailed execution logs with timing information
- **Response Time Tracking**: Latency monitoring for each LLM query
- **Error Handling**: Robust error handling for API failures and parsing errors
- **Progress Tracking**: Real-time progress updates during pipeline execution

## 🔧 Configuration

### Environment Variables

```bash
# LM Studio Configuration
LMSTUDIO_HOST="http://127.0.0.1:1234"
LMSTUDIO_API_KEY="lm-studio"
LM_MODEL="gpt-oss-7b-instruct"

# Pipeline Configuration
TRIALS_PER_STORY=5
TIMEOUT_SECONDS=60
```

### Customizing User Stories

Edit `data/user_stories.csv` to add your own user stories:

```csv
id,story,human_baseline
1,"As a user, I want to reset my password via email so that I can regain account access.",3
2,"As an admin, I want to export all user activity logs in CSV format so that I can analyze system usage.",8
...
```

### Prompt Customization

Modify `src/prompt_design.py` to adjust the estimation prompts:

```python
PROMPT_SYSTEM = "You are an experienced Agile coach. Give a concise, structured JSON output."

PROMPT_USER_TEMPLATE = (
    "Estimate story points (integer 1-10) for the user story below. "
    "Return valid JSON only with keys: estimate (int), reasons (list of short strings), "
    "similar_examples (short string), confidence (low|med|high).\n\n"
    "User story: \"{story}\"\n"
    "Be concise."
)
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author & Credits

**AI Sprint Estimator**  
Developed by: **Your Name**

### Attribution Notice
When using this software, please include the following attribution:

```
AI Sprint Estimator
Copyright (c) 2025 Your Name
Licensed under the MIT License
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Academic Use

This project is designed for academic research and provides:

- **Reproducible Methodology**: Complete pipeline with documented steps
- **Structured Data Outputs**: CSV and JSON formats for analysis
- **Comprehensive Benchmarking**: Statistical metrics for evaluation
- **Privacy-Preserving Evaluation**: Local LLM integration
- **Research-Ready**: Suitable for academic papers and publications

---

**AI Sprint Estimator** - Transforming Agile estimation with AI-powered local LLM evaluation and comprehensive benchmarking.

