 <img width="100%" src="https://github.com/asifthedev/mulit-agent-skills-analyst/blob/main/images/header.png" alt=""></a>
## Problem

One common mistake beginners make when learning a new skill is not researching what to learn and what not to. As a result, we end up wasting a lot of our precious time on skills that may not be in high demand in the job market.

## Solution

We utilized the **CrewAI** framework alongside **OPENAI's API** to construct a Multi-Agent System. This system searches Google and scrapes popular job posting websites for job descriptions related to a specific role. It then analyzes the **common skills** across all available jobs in the market. These are the skills you should prioritize, as they are sought after by most companies.

### Key Features:

- Utilizes OpenAI's GPT-4 model for advanced natural language processing
- Implements web scraping and search capabilities using SerperDev and custom tools
- Analyzes job descriptions to identify common technical skills
- Presents results in a clean, Markdown-formatted table
### How It Works:

1. The user inputs a job title 
2. The Job Analyst agent searches and scrapes job descriptions
3. The Requirement Analyst agent identifies common skills across job postings
4. The Quality Assurance agent ensures proper Markdown formatting
5. Results are displayed in markdown format

## Code Breakdown

### 1. Imports and Environment Setup

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os

# Environment setup
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4-turbo'
os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'
os.environ["SERPER_API_KEY"] = 'your_serper_api_key'
```

**Imports:**
- `Agent`, `Task`, `Crew`, and `Process` are imported from the `crewai` library to define agents, tasks, and their orchestration.
- `SerperDevTool` and `ScrapeWebsiteTool` are tools from `crewai_tools` for web searching and scraping.
- `os` is used for setting environment variables like API keys.

**Environment Setup:** The environment variables are set for the OpenAI API and the Serper API, which are used by the tools to access the GPT-4 model and perform web searches.

### 2. Tool Initialization

```python
# Tools
searching_tool = SerperDevTool()
web_scraper = ScrapeWebsiteTool()
```

**Tool Initialization:**
- `SerperDevTool` is a search tool for finding information on the web.
- `ScrapeWebsiteTool` is used to scrape data from websites.

### 3. Agent Definitions

```python
job_analyst = Agent(
    role='Senior Job Researcher',
    goal='Search and collect comprehensive job descriptions for {job_title} from reputable online sources.',
    backstory=(
        'As an expert in job market research, you excel at finding and compiling detailed job postings for {job_title}. '
        'Your expertise in using search and scraping tools allows you to gather accurate and up-to-date job information.'
    ),
    allow_delegation=True,
    verbose=True
)

requirement_analyst = Agent(
    role='Senior Job Requirements Analyst',
    goal='Identify and analyze common technical skills across collected job descriptions for {job_title}.',
    backstory=(
        'With your extensive experience in analyzing job requirements for {job_title}, '
        'you specialize in identifying key technical skills that are consistently in demand across various job postings. '
        'Your insights help job seekers focus on the most crucial skills for their career development.'
    ),
    allow_delegation=False,
    verbose=True
)

quality_assurance = Agent(
    role='Markdown Output Validator',
    goal='Ensure the final output is in valid Markdown format.',
    backstory=(
        'As a documentation and formatting expert, you understand the importance of presenting data in a clear, '
        'readable Markdown format. Your role is to verify that the final output adheres to proper Markdown syntax, '
        'ensuring it can be easily read and integrated into various documentation systems.'
    ),
    allow_delegation=True,
    verbose=True
)
```

**Agents:**
- `job_analyst`: Responsible for searching and collecting job descriptions for the given job title.
- `requirement_analyst`: Analyzes the collected job descriptions to identify common technical skills.
- `quality_assurance`: Ensures the final output is properly formatted in Markdown.
Each agent has a specific role, goal, and backstory to define their purpose and how they contribute to the tasks.

### 4. Task Definitions

```python
search_scrape = Task(
    description=(
        'Conduct a comprehensive search and scrape of reputable job posting websites for {job_title} positions. '
        'Focus on extracting detailed job descriptions, emphasizing required skills, qualifications, and responsibilities. '
        'Ensure the collected data is diverse and representative of the current job market.'
    ),
    expected_output='A comprehensive list of job descriptions for {job_title}, including detailed requirements and skills.',
    tools=[searching_tool, web_scraper],
    agent=job_analyst
)

find_common_skills = Task(
    description=(
        'Analyze the collected job descriptions for {job_title} to identify recurring technical skills. '
        'Quantify the frequency of each skill across all job postings to determine their relative importance in the job market. '
        'Present the results in a Markdown-formatted table.'
    ),
    expected_output="A Markdown-formatted table containing common technical skills and their frequency across all analyzed job postings for {job_title}. It's no closed in triple back ticks ```markdown\n"
    "```like this but should markdown",
    agent=requirement_analyst
)

assuring_quality = Task(
    description=(
        'Validate that the output from the skill analysis task is properly formatted in Markdown. '
        'The output should include a table of skills and their frequencies, formatted correctly in Markdown syntax. '
        'If the output does not meet this requirement, collaborate with the Requirement Analyst to rectify the format. '
        'Ensure that only the Markdown-formatted table is returned, without any extraneous text or information.'
    ),
    expected_output='A Markdown-formatted table containing skill data and frequencies, with no extraneous text or information.',
    agent=quality_assurance
)
```

**Tasks:**
- `search_scrape`: Task for `job_analyst` to search and scrape job descriptions using the tools.
- `find_common_skills`: Task for `requirement_analyst` to analyze the job descriptions and identify common skills.
- `assuring_quality`: Task for `quality_assurance` to validate the Markdown formatting of the output.

### 5. Crew Setup and Execution

```python
# Crew setup
crew = Crew(
    agents=[job_analyst, requirement_analyst, quality_assurance],
    tasks=[search_scrape, find_common_skills, assuring_quality],
    memory=True,
    verbose=2,
    process=Process.sequential
)

# Kick off the crew process
result = crew.kickoff(inputs={'job_title': job_title})

print(result)
```

**Crew Setup:** A `Crew` is created with the three agents and their respective tasks. The process is set to `Process.sequential`, meaning tasks are executed one after the other.

**Execution:** The `crew.kickoff()` method is called to start the process, passing in the job title as input. The final result is displayed using Streamlit's `st.markdown()`.

---

© 2024 Asif Shahzad. All rights reserved.

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=80&section=footer"/>
</p>

