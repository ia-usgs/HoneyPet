class HTMLGenerator:
    def __init__(self):
        # Default HTML template
        self.template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>{title}</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 20px;
                }}
                h1 {{
                    color: #333;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ccc;
                    padding: 10px;
                    text-align: left;
                }}
                th {{
                    background-color: #f4f4f4;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
            </style>
        </head>
        <body>
            <h1>{title}</h1>
            {table}
        </body>
        </html>
        """

    def generate_html(self, json_data, output_file):
        """
        Generate an HTML report from JSON data.
        :param json_data: The JSON data containing 'title', 'headers', and 'rows'.
        :param output_file: The path of the HTML file to generate.
        """
        # Generate HTML table
        table_html = self.create_html_table(json_data)

        # Apply template
        html_content = self.apply_template(json_data["title"], table_html)

        # Write to output file
        with open(output_file, "w") as f:
            f.write(html_content)

    def create_html_table(self, json_data):
        # Generate table headers
        headers_html = "".join(f"<th>{header}</th>" for header in json_data["headers"])
        table_html = f"<table><tr>{headers_html}</tr>"

        # Generate table rows
        for row in json_data["rows"]:
            row_html = "".join(f"<td>{cell}</td>" for cell in row)
            table_html += f"<tr>{row_html}</tr>"

        table_html += "</table>"
        return table_html

    def apply_template(self, title, table):
        return self.template.format(title=title, table=table)
