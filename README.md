# GitHub Repository Score Calculator

A comprehensive DevOps solution for evaluating GitHub repository health and quality through automated scoring based on multiple key metrics including community engagement, development activity, CI/CD practices, and code quality indicators.

## 📋 Problem Statement

In modern software development, maintaining high-quality, healthy repositories is crucial for project success. However, developers and organizations often struggle with:

- Lack of objective metrics to assess repository health and quality
- Manual evaluation processes that are time-consuming and inconsistent
- Difficulty identifying repositories that need attention or improvement
- No standardized way to compare repository quality across projects

This project solves these challenges by providing an automated, API-driven scoring system that evaluates GitHub repositories across multiple dimensions and provides actionable insights for improvement.

## 🏗️ Folder Structure

```
devopsproject-Repository-Score-Calculator/
├── src/
│   ├── main.py              # FastAPI application with REST endpoints
│   └── logic.py             # Core scoring logic and metrics calculation
├── infrastructure/
│   ├── Dockerfile           # Containerization configuration
│   ├── docker-compose.yml   # Local development orchestration
│   └── app.json             # Deployment configuration
├── .github/
│   └── workflows/           # CI/CD pipelines
├── docs/                    # Documentation and guides
├── .env                     # Environment variables (local development)
├── .gitignore              # Git ignore rules
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── LICENSE                 # Project license
```

## 🚀 Installation and Setup

### Prerequisites

- Python 3.12+
- Git
- Docker & Docker Compose (for containerized deployment)

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd devopsproject-Repository-Score-Calculator
   ```

2. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   Create a `.env` file in the project root:
   ```env
   INTERNAL_API_KEY=your-secure-api-key
   GITHUB_TOKEN=your-github-personal-access-token
   ```

5. **Run the application:**
   ```bash
   uvicorn src.main:app --reload
   ```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## 📖 Usage

### API Endpoints

#### Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

#### Repository Scan
```bash
curl -X POST "http://localhost:8000/scan" \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-api-key" \
  -d '{"owner": "microsoft", "repo": "vscode"}'
```

### Local Development

1. **Start the server:**
   ```bash
   uvicorn src.main:app --reload
   ```

2. **Access the API:**
   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

3. **Test with curl:**
   ```bash
   curl -X POST "http://localhost:8000/scan" \
     -H "x-api-key: devops-secret-123" \
     -H "Content-Type: application/json" \
     -d '{"owner": "octocat", "repo": "Hello-World"}'
   ```

### Docker Deployment

#### Using Docker Compose (Recommended)

1. Build and run:
   ```bash
   cd infrastructure
   docker-compose up --build
   ```

2. Access the API:
   - API: `http://localhost:8000`
   - Health Check: `http://localhost:8000/health`

#### Using Docker directly

1. Build the image:
   ```bash
   docker build -f infrastructure/Dockerfile -t git-health-scorer .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 \
     -e INTERNAL_API_KEY=your-api-key \
     -e GITHUB_TOKEN=your-github-token \
     git-health-scorer
   ```

## 🔄 DevOps Implementation

### CI/CD Pipeline

The project includes GitHub Actions workflows for automated testing, building, and deployment:

- Continuous Integration: Automated testing on every push/PR
- Containerization: Docker image building and publishing
- Security Scanning: Dependency and code vulnerability checks


### Infrastructure as Code

- Docker: Containerized application for consistent development
- Docker Compose: Local development environment orchestration
- Health Checks: Built-in monitoring and health verification

### Security Features

- API Key Authentication: Secure access control for API endpoints
- Environment Variable Management: Sensitive data stored securely
- GitHub Token Integration: Secure access to GitHub API
- HTTPS Ready: Configured for secure communication

### Monitoring & Observability

- Health Endpoints: Built-in health checks for load balancers
- Structured Logging: Comprehensive logging for debugging and monitoring
- Error Handling: Proper error responses and status codes


##  Scoring Metrics

The calculator evaluates repositories across multiple dimensions:

- Community (25 points): Stars, forks, contributors diversity
- Activity (25 points): Recent commits, issue resolution
- CI/CD (20 points): Workflow success rates, automation
- Code Quality (15 points): License, documentation, structure
- Security (15 points): Vulnerability management, access controls

Total Score Range: 0-100 points
Grade Scale: A (90-100), B (80-89), C (70-79), D (60-69), F (0-59)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review the health endpoint at `/health`