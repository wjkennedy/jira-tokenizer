import string
from jira import JIRA
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import pandas as pd

# Jira query
jira_query = 'project = "Sample Project" and status = "Closed"'

# Jira API endpoint
jira_url = "https://jira.example.com"

# Jira credentials
jira_username = "your_username"
jira_password = "your_password"

# Connect to Jira
jira = JIRA(jira_url, basic_auth=(jira_username, jira_password))

# Initialize list to store frequency distribution data
fdist_data = []

# Initialize starting point
startAt = 0

# Initialize the Porter stemmer
ps = PorterStemmer()

# Continuously retrieve the next set of issues
while True:
    # Execute the Jira query
    issues = jira.search_issues(jira_query, startAt=startAt)

    # Exit the loop if no more issues are returned
    if len(issues) == 0:
        break
    
    # Iterate over the returned issues
    for issue in issues:
        # Extract the project key, project name, summary, and description
        issue_key = issue.key
        project_name = issue.fields.project.name
        summary = issue.fields.summary
        description = issue.fields.description

        # Concatenate the summary and description
        text = summary + " " + description

        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Normalize the text
        text = text.lower()

        # Tokenize the text
        tokens = word_tokenize(text)

        # Remove stop words
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]

        # Stem the tokens
        stemmed_tokens = [ps.stem(token) for token in tokens]

        # Compute frequency distribution
        fdist = FreqDist(stemmed_tokens)
        
        # Get the top 10 most common words
        top_words = fdist.most_common(10)

        # Append the project key, project name, summary, and top words to the data list
        fdist_data.append({'Issue Key': issue_key, 'Project Name': project_name, 'Summary': summary, 'Top Words': top_words})

    # Update the starting point
    startAt += len(issues)

# Create a DataFrame from the frequency distribution data
df = pd.DataFrame(fdist_data)

# Sort the DataFrame by Issue Key
df = df.sort_values(by=['Issue Key'])

# Print the DataFrame
print(df)

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

