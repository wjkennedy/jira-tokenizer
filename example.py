import json
import d3py
import jira
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd

# Jira connection
jira = jira.JIRA(basic_auth=('username', 'password'), options={'server': 'https://your-jira-instance.com'})

# Jira query
query = 'project = project_name and created > -30d'

# Get all issues from Jira
issues = jira.search_issues(query, maxResults=None)

# Tokenize and remove stopwords from issue summaries
stop_words = set(stopwords.words('english'))
top_words = []
for issue in issues:
    words = word_tokenize(issue.fields.summary.lower())
    words = [word for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]
    top_words.extend(words)

# Get top 10 most common words
top_words = Counter(top_words)
top_words = top_words.most_common(10)

# Create dataframe with project name, issue key, and top words
data = []
for issue in issues:
    project = issue.fields.project.name
    key = issue.key
    summary = issue.fields.summary
    row = [project, key, summary] + [word[0] for word in top_words]
    data.append(row)

df = pd.DataFrame(data, columns=["Project Name", "Issue Key", "Summary"] + [word[0] for word in top_words])

# Normalize all text
df["Summary"] = df["Summary"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df["Project Name"] = df["Project Name"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
df["Issue Key"] = df["Issue Key"].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

# Create alluvial flow diagram
data = {}
for word in top_words:
    for project, df_project in df.groupby('Project Name'):
        data[(project, word[0])] = len(df_project[df_project[word[0]] == 1])

with open('alluvial_diagram.json', 'w') as fp:
    json.dump(data, fp)

# Create the alluvial flow diagram using d3py
fig = d3py.alluvial(data)
d3 = d3py.d3(fig)
d3.saveas("alluvial_diagram.svg")


