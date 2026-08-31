import os
from scholarly import scholarly

# Your Google Scholar ID
SCHOLAR_ID = "AaljAEgAAAAJ"

def fetch_publications():
    print(f"Fetching publications for Scholar ID: {SCHOLAR_ID}...")
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=['publications'])
    
    pubs_data = []
    for pub in author['publications']:
        # Fetch detailed publication metadata
        filled_pub = scholarly.fill(pub)
        bib = filled_pub.get('bib', {})
        
        title = bib.get('title', 'Untitled')
        authors = bib.get('author', 'Bhargavi R')
        pub_year = bib.get('pub_year', 'N/A')
        venue = bib.get('venue') or bib.get('journal') or bib.get('conference') or ''
        pub_url = filled_pub.get('pub_url') or f"https://scholar.google.com/citations?view_op=view_citation&citation_for_view={filled_pub.get('author_pub_id')}"
        
        pubs_data.append({
            'title': title,
            'authors': authors,
            'year': str(pub_year),
            'venue': venue,
            'url': pub_url
        })
        print(f"Fetched: {title} ({pub_year})")
        
    # Sort publications by Year descending
    pubs_data.sort(key=lambda x: (x['year'] if x['year'] != 'N/A' else '0000'), reverse=True)
    return pubs_data

def generate_html(pubs):
    # Generate list items without citation counts
    pub_items = ""
    for p in pubs:
        venue_str = f"<em>{p['venue']}</em>" if p['venue'] else ""
        year_str = f"({p['year']})" if p['year'] != 'N/A' else ""
        
        meta_parts = [part for part in [venue_str, year_str] if part]
        meta_html = " ".join(meta_parts)
        
        pub_items += f"""
        <li class="publication-item">
            <a href="{p['url']}" target="_blank" class="pub-title">{p['title']}</a>
            <div class="pub-authors">{p['authors']}</div>
            <div class="pub-meta">{meta_html}</div>
        </li>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publications | Dr. Bhargavi R</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        .publications-container {{
            max-width: 900px;
            margin: 20px auto;
            padding: 0 15px;
            font-family: inherit;
        }}
        .publication-list {{
            list-style-type: decimal;
            padding-left: 20px;
        }}
        .publication-item {{
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e0e0e0;
        }}
        .pub-title {{
            font-size: 1.05rem;
            font-weight: 600;
            color: #0056b3;
            text-decoration: none;
        }}
        .pub-title:hover {{
            text-decoration: underline;
        }}
        .pub-authors {{
            color: #444;
            margin-top: 4px;
            font-size: 0.95rem;
        }}
        .pub-meta {{
            color: #666;
            margin-top: 4px;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <header>
        <ul>
            <li><a href="index.html">About</a></li>
            <li><a href="./teaching.html">Teaching</a></li>
            <li><a aria-current="page" href="./publications.html">Publications</a></li>
            <li><a href="#">Software</a></li>
        </ul>
    </header>

    <div class="publications-container">
        <h2>Publications</h2>
        <p>
            <a href="https://scholar.google.co.in/citations?hl=en&user={SCHOLAR_ID}" target="_blank">
                <img height="20px" src="assets/icons/icons8-google-scholar.svg" alt="Google Scholar" style="vertical-align: middle;"> View on Google Scholar
            </a>
        </p>
        <ol class="publication-list">
            {pub_items}
        </ol>
    </div>
</body>
</html>
"""
    with open("publications.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("\n✓ 'publications.html' regenerated successfully without citations!")

if __name__ == "__main__":
    publications = fetch_publications()
    generate_html(publications)