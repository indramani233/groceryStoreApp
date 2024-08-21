import pdfkit

def generate_report(content, file_path, format_type='html'):
    if format_type == 'pdf':
        pdfkit.from_string(content, file_path)
        return file_path  # Return the file path for PDF download or viewing

    # Return the HTML content if requested format is HTML
    return content
