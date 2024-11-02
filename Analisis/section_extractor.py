def extract_sections(text):
    """Divide el texto en párrafos, retornando una lista de párrafos."""
    paragraphs = text.split('\n')  # Suponiendo que los párrafos están separados por saltos de línea
    return [para.strip() for para in paragraphs if para.strip()]  # Limpia y elimina vacíos

