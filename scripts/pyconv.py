import pandas as pd
import json
import sys

def title_to_filename(title):
    """Convert book title to a file-friendly format."""
    return title.replace(' ', '-').lower()

def convert_csv_to_json(csv_file_path):
    """Convert CSV data to JSON format."""
    df = pd.read_csv(csv_file_path)

    json_data = []
    for _, row in df.iterrows():
        book_json = {
            "file": title_to_filename(row['Title']),
            "name": row['Title'],
            "author": row['Author'],
            "startDate": row['Start Date'] if pd.notna(row['Start Date']) else "null",
            "endDate": row['End Date'] if pd.notna(row['End Date']) else "null",
            "reason": row['Reason'] if pd.notna(row['Reason']) else "null",
            "body": row['Body'] if pd.notna(row['Body']) else "null",
            "links": [] if pd.isna(row['Links']) else [link.strip() for link in row['Links'].split(',')]
        }
        json_data.append(book_json)

    return json.dumps(json_data, indent=2)

def generate_html_output(csv_file_path):
    """Generate HTML output for each book entry."""
    df = pd.read_csv(csv_file_path)

    html_output = ""
    for _, row in df.iterrows():
        file_name = title_to_filename(row['Title'])
        project_date = row['Date'] if pd.notna(row['Date']) else ""
        book_title = row['Title']
        book_author = row['Author']

        html_row = f"""<div class="project_row">
                <a href="books-read/{file_name}.html">
                    <div class="project_date">{project_date}</div>
                    <div class="project_name">{book_title}</div>
                    <div class="project_subtitle">{book_author}</div>
                </a>
            </div>\n"""
        html_output += html_row

    return html_output

def output_to_file(output, file_path):
    """Output data to file."""
    with open(file_path, 'w') as f:
        f.write(output)


def main(csv_file_path):
    json_output = convert_csv_to_json(csv_file_path)
    output_to_file(json_output, "books-read.json")
    html_output = generate_html_output(csv_file_path)
    output_to_file(html_output, "books-read.html")

if __name__ == "__main__":
    csv_file_path = sys.argv[1]
    main(csv_file_path)

