# Jira Issue Tokenizer and Analyzer

This script utilizes the Jira Python API and NLTK library to extract, tokenize, and analyze the text data of Jira issues. It allows you to query Jira issues, extract specified fields, and perform natural language processing tasks such as tokenization and removing stop words. The script also generates a Pandas DataFrame with the Project Name, Summary, and Issue Key, as well as a frequency distribution of the top words. The script also generate an alluvial flow diagram of the top words and their corresponding project key.

## Usage
To use this script, you will need to have a Jira account and an API token. You will also need to have the following Python packages installed:

-jira

-nltk

-pandas

-matplotlib

-plotly

-seaborn

-colour

-alluvial

You can install these packages by running the following command:

    pip install jira nltk pandas matplotlib plotly seaborn colour alluvial

You can then run the script by providing your Jira URL, API token, and query string as command-line arguments:


    python jira_issue_tokenizer_and_analyzer.py --url https://your-jira-url --token your-api-token --query "project = YOURPROJECT AND resolution = Done"

You can also specify the limit of the results returned from Jira query and the number of top words to keep.

## Output

The script will output the following:

- A CSV file containing the dataframe of the Project Name, Summary, Issue Key and the top 10 words

- A alluvial flow diagram of the top words and their corresponding project key in PNG format

## Caveats

The script only retrieves the first 1000 results of the query by default. You can increase this by modifying the maxResults parameter in the Jira API query.
The script uses the NLTK library's stopwords list for removing stop words. This list is in English, so if your Jira issues contain text in a different language, you may need to modify the script to use a different stopwords list.
The script normalizes the text, but it does not perform stemming or lemmatization.
The script uses the default color scheme of Plotly and does not use the ebay's color scheme and font; Market Sans.
Please note that this is a sample README file. It might not reflect the full functionality of the script and you may have to adjust it accordingly.

