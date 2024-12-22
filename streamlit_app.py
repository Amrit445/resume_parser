import re
import fitz
import nltk
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
import streamlit as st
import pandas as pd

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    skills = Column(String)
    experience = Column(String)

def setup_database():
    engine = create_engine("sqlite:///candidates.db")
    Base.metadata.create_all(engine)
    return engine

def extract_text_from_pdf(file_path):
    with fitz.open(file_path) as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text

def extract_skills(text, skill_set):
    text = text.lower()
    found_skills = [skill for skill in skill_set if skill in text]
    return found_skills

def extract_experience(text):
    experience_pattern = re.compile(r"(\d+)\s+years? of experience")
    match = experience_pattern.search(text)
    return match.group(1) if match else None

from nltk.tokenize import word_tokenize
from nltk import pos_tag

def extract_candidate_name(text):
    tokens = word_tokenize(text)
    pos_tags = pos_tag(tokens)
    proper_nouns = [word for word, tag in pos_tags if tag == 'NNP']
    return proper_nouns[0] if proper_nouns else "Not Found"

engine = setup_database()

st.title("Resume Parser")

uploaded_file = st.file_uploader("Upload a resume (PDF)", type=["pdf"])
if uploaded_file:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract and process resume
    text = extract_text_from_pdf("temp_resume.pdf")
    skills = extract_skills(text, skill_set=["Python", "Data Analysis", "Machine Learning", "Communication", "Project Management", "Deep Learning", "SQL", "Tableau",
    "Java", "C++", "JavaScript", "HTML", "CSS", "React", "Angular", "Node.js", "MongoDB", "Express.js", "Git",
    "Research", "Statistics", "Quantitative Analysis", "Qualitative Analysis", "SPSS", "R", "Data Visualization", "Matplotlib",
    "Seaborn", "Plotly", "Pandas", "Numpy", "Scikit-learn", "TensorFlow", "Keras", "PyTorch", "NLTK", "Text Mining",
    "Natural Language Processing", "Computer Vision", "Image Processing", "OCR", "Speech Recognition", "Recommendation Systems",
    "Collaborative Filtering", "Content-Based Filtering", "Reinforcement Learning", "Neural Networks", "Convolutional Neural Networks",
    "Recurrent Neural Networks", "Generative Adversarial Networks", "XGBoost", "Random Forest", "Decision Trees", "Support Vector Machines",
    "Linear Regression", "Logistic Regression", "K-Means Clustering", "Hierarchical Clustering", "DBSCAN", "Association Rule Learning",
    "Apache Hadoop", "Apache Spark", "MapReduce", "Hive", "HBase", "Apache Kafka", "Data Warehousing", "ETL", "Big Data Analytics",
    "Cloud Computing", "Amazon Web Services (AWS)", "Microsoft Azure", "Google Cloud Platform (GCP)", "Docker", "Kubernetes", "Linux",
    "Shell Scripting", "Cybersecurity", "Network Security", "Penetration Testing", "Firewalls", "Encryption", "Malware Analysis",
    "Digital Forensics", "CI/CD", "DevOps", "Agile Methodology", "Scrum", "Kanban", "Continuous Integration", "Continuous Deployment",
    "Software Development", "Web Development", "Mobile Development", "Backend Development", "Frontend Development", "Full-Stack Development",
    "UI/UX Design", "Responsive Design", "Wireframing", "Prototyping", "User Testing", "Adobe Creative Suite", "Photoshop", "Illustrator",
    "InDesign", "Figma", "Sketch", "Zeplin", "InVision", "Product Management", "Market Research", "Customer Development", "Lean Startup",
    "Business Development", "Sales", "Marketing", "Content Marketing", "Social Media Marketing", "Email Marketing", "SEO", "SEM", "PPC",
    "Google Analytics", "Facebook Ads", "LinkedIn Ads", "Lead Generation", "Customer Relationship Management (CRM)", "Salesforce",
    "HubSpot", "Zendesk", "Intercom", "Customer Support", "Technical Support", "Troubleshooting", "Ticketing Systems", "ServiceNow",
    "ITIL", "Quality Assurance", "Manual Testing", "Automated Testing", "Selenium", "JUnit", "Load Testing", "Performance Testing",
    "Regression Testing", "Black Box Testing", "White Box Testing", "API Testing", "Mobile Testing", "Usability Testing", "Accessibility Testing",
    "Cross-Browser Testing", "Agile Testing", "User Acceptance Testing", "Software Documentation", "Technical Writing", "Copywriting",
    "Editing", "Proofreading", "Content Management Systems (CMS)", "WordPress", "Joomla", "Drupal", "Magento", "Shopify", "E-commerce",
    "Payment Gateways", "Inventory Management", "Supply Chain Management", "Logistics", "Procurement", "ERP Systems", "SAP", "Oracle",
    "Microsoft Dynamics", "Tableau", "Power BI", "QlikView", "Looker", "Data Warehousing", "ETL", "Data Engineering", "Data Governance",
    "Data Quality", "Master Data Management", "Beautiful Soup", "NLP", "Predictive Analytics", "Prescriptive Analytics", "Descriptive Analytics", "Business Intelligence",
    "Dashboarding", "Reporting", "Data Mining", "Web Scraping", "API Integration", "RESTful APIs", "GraphQL", "SOAP", "Microservices",
    "Serverless Architecture", "Lambda Functions", "Event-Driven Architecture", "Message Queues", "GraphQL", "Socket.io", "WebSockets",
    "Ruby", "Ruby on Rails", "PHP", "Symfony", "Laravel", "CakePHP", "Zend Framework", "ASP.NET", "C#", "VB.NET", "ASP.NET MVC", "Entity Framework",
    "Spring", "Hibernate", "Struts", "Kotlin", "Swift", "Objective-C", "iOS Development", "Android Development", "Flutter", "React Native", "Ionic",
    "Mobile UI/UX Design", "Material Design", "SwiftUI", "RxJava", "RxSwift", "Django", "Flask", "FastAPI", "Falcon", "Tornado", "WebSockets",
    "GraphQL", "RESTful Web Services", "SOAP", "Microservices Architecture", "Serverless Computing", "AWS Lambda", "Google Cloud Functions",
    "Azure Functions", "Server Administration", "System Administration", "Network Administration", "Database Administration", "MySQL", "PostgreSQL",
    "SQLite", "Microsoft SQL Server", "Oracle Database", "NoSQL", "MongoDB", "Cassandra", "Redis", "Elasticsearch", "Firebase", "Google Analytics",
    "Google Tag Manager", "Adobe Analytics", "Marketing Automation", "Customer Data Platforms", "Segment", "Salesforce Marketing Cloud", "HubSpot CRM",
    "Zapier", "IFTTT", "Workflow Automation", "Robotic Process Automation (RPA)", "UI Automation", "Natural Language Generation (NLG)",
    "Virtual Reality (VR)", "Augmented Reality (AR)", "Mixed Reality (MR)", "Unity", "Unreal Engine", "3D Modeling", "Animation", "Motion Graphics",
    "Game Design", "Game Development", "Level Design", "Unity3D", "Unreal Engine 4", "Blender", "Maya", "Adobe After Effects", "Adobe Premiere Pro",
    "Final Cut Pro", "Video Editing", "Audio Editing", "Sound Design", "Music Production", "Digital Marketing", "Content Strategy", "Conversion Rate Optimization (CRO)",
    "A/B Testing", "Customer Experience (CX)", "User Experience (UX)", "User Interface (UI)", "Persona Development", "User Journey Mapping", "Information Architecture (IA)",
    "Wireframing", "Prototyping", "Usability Testing", "Accessibility Compliance", "Internationalization (I18n)", "Localization (L10n)", "Voice User Interface (VUI)",
    "Chatbots", "Natural Language Understanding (NLU)", "Speech Synthesis", "Emotion Detection", "Sentiment Analysis", "Image Recognition", "Object Detection",
    "Facial Recognition", "Gesture Recognition", "Document Recognition", "Fraud Detection", "Cyber Threat Intelligence", "Security Information and Event Management (SIEM)",
    "Vulnerability Assessment", "Incident Response", "Forensic Analysis", "Security Operations Center (SOC)", "Identity and Access Management (IAM)", "Single Sign-On (SSO)",
    "Multi-Factor Authentication (MFA)", "Blockchain", "Cryptocurrency", "Decentralized Finance (DeFi)", "Smart Contracts", "Web3", "Non-Fungible Tokens (NFTs)", 
    "Rust", "Go (Golang)", "TypeScript", "Svelte", "Vue.js", "Electron.js", "Deno", "Bash Scripting", "Perl", "Groovy", "Scala",
    "ColdFusion", "LightGBM", "CatBoost", "AutoML", "H2O.ai", "OpenAI APIs", "Hugging Face", "Transformers", "Few-Shot Learning", "Retrieval-Augmented Generation",
    "Zero-Shot Learning", "Transfer Learning", "Bayesian Optimization", "Hyperparameter Tuning", "Explainable AI (XAI)", "TensorFlow", "PyTorch Lightning",
    "Federated Learning", "Edge AI", "Alteryx", "KNIME", "RapidMiner", "DataRobot", "Snowflake", "Azure Synapse Analytics", "HuggingFace",
    "Data Lineage", "Time Series Analysis", "Anomaly Detection", "Hypothesis Testing", "Terraform", "Ansible", "Puppet", "Chef",
    "Jenkins", "Spinnaker", "Istio", "Prometheus", "Grafana", "Elastic Stack (ELK)", "Consul", "OpenShift", "CloudFormation", "PyTorch", "RAG",
    "AWS Sagemaker", "Cloudflare", "Neo4j", "Amazon Redshift", "DynamoDB", "CockroachDB", "Greenplum", "Hadoop Distributed File System (HDFS)",
    "Amazon S3", "Ceph", "MinIO", "OWASP", "Threat Modeling", "SIEM Tools (Splunk, QRadar)", "Identity Federation", "Gen ai", "GenAI",
    "Secure Software Development Lifecycle (SSDLC)", "Kubernetes Security (K8s security tools like Falco, Aqua Security)",
    "Cloud Security (AWS Security Hub, Azure Security Center)", "Solidity", "Hyperledger Fabric", "Ethereum Virtual Machine (EVM)",
    "Polkadot", "Cosmos", "Chainlink", "Metamask Integration", "Decentralized Applications (dApps)", "IPFS (InterPlanetary File System)",
    "CorelDRAW", "Affinity Designer", "Canva", "GIMP", "DaVinci Resolve", "Cinema 4D", "Houdini", "Jira", "Trello", "Confluence",
    "Airtable", "Monday.com", "Basecamp", "Notion", "Miro", "Quantum Computing", "Tensor Networks", "Neuromorphic Computing", 
    "Edge Computing", "5G Networking", "Remote Desktop Tools (TeamViewer, AnyDesk)", "API Management (Postman, Swagger)", 
    "IT Asset Management", "ChatGPT Plugins Development", "SaaS Product Development", "Generative AI", "BeautifulSoup"])
    experience = extract_experience(text)
    name = extract_candidate_name(text)
    
    # Save to database
    with engine.connect() as conn:
        conn.execute(Candidate.__table__.insert().values(name=name, skills=",".join(skills), experience=experience))
    
    st.success(f"Parsed resume for {name}")
    st.write("**Skills:**", ", ".join(skills))
    st.write("**Experience:**", experience or "Not Found")

    # Display database records
    st.subheader("All Parsed Resumes")
    df = pd.read_sql_table('candidates', engine)
    st.dataframe(df)
