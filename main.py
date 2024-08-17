from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
import os

# Environment setup
os.environ['OPENAI_MODEL_NAME'] = 'gpt-4-turbo'
os.environ['OPENAI_API_KEY'] = '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'
os.environ["SERPER_API_KEY"] = 'e99fbcb9e3705c51ce0b8fec4553f31140f076ca'

# Tools
searching_tool = SerperDevTool()
web_scraper = ScrapeWebsiteTool()

# Agents
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

# Tasks
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
    expected_output="A Markdown-formatted table containing common technical skills and their frequency across all analyzed job postings for {job_title}. It\'s no closed in triple back ticks ```markdown\n"
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

# Crew setup
crew = Crew(
    agents=[job_analyst, requirement_analyst, quality_assurance],
    tasks=[search_scrape, find_common_skills, assuring_quality],
    memory=True,
    verbose=2,
    process=Process.sequential  # Ensuring tasks are executed in sequence
)

# Kick off the crew process
result = crew.kickoff(inputs={'job_title': job_title})
