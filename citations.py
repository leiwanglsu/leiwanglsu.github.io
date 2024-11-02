import re
import requests

def extract_doi_and_format(citation_text):
    # Define a regular expression pattern to match DOIs in the text
    doi_pattern = r"(10.\d{4,9}/[-._;()/:A-Za-z0-9]+)"
    
    # Search for a DOI in the citation text
    doi_match = re.search(doi_pattern, citation_text)
    
    if doi_match:
        # If a DOI is found, create a hyperlink without a trailing period
        doi = doi_match.group(0).rstrip('.')
        doi_link = f"https://doi.org/{doi}"
        html_output = f'<li><a href="{doi_link}" target="_blank">{citation_text}</a></li>'
    else:
        # If no DOI is found, try to retrieve it from the web
        doi_link = search_for_doi(citation_text)
        if doi_link:
            html_output = f'<li><a href="{doi_link}" target="_blank">{citation_text}</a></li>'
        else:
            html_output = f'<li>{citation_text}</li>'
    
    return html_output

def search_for_doi(citation_text):
    """
    Search for DOI using CrossRef API.
    """
    try:
        url = "https://api.crossref.org/works"
        headers = {"Accept": "application/json"}
        
        # Use the citation text as a query to the CrossRef API
        response = requests.get(url, headers=headers, params={"query": citation_text, "rows": 1})
        response.raise_for_status()
        
        data = response.json()
        # Check if we have a DOI in the response
        if data["message"]["items"]:
            doi = data["message"]["items"][0]["DOI"]
            return f"https://doi.org/{doi}"
    except Exception as e:
        print(f"Error fetching DOI: {e}")
    
    return None

# Example citations with and without DOI
citations = [
    """
Wang, Lei, Hongxing Liu, Haibin Su, and Jun Wang. 2019. “Bathymetry Retrieval from Optical Images with Spatially Distributed Support Vector Machines.” GIScience and Remote Sensing 56 (3): 323–37.
"""

]

# Process each citation and print the resulting HTML
html_list_items = [extract_doi_and_format(citation) for citation in citations]

# Join list items into a single HTML unordered list
html_output = "<ul>\n" + "\n".join(html_list_items) + "\n</ul>"

print(html_output)
