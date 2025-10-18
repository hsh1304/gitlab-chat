from PyPDF2 import PdfReader
import os
import math

def load_pdf_text_chunks(pdf_path, chunk_size=200, overlap=50):
    if not os.path.exists(pdf_path):
        print(f"Document not found at {pdf_path}. No docs loaded.")
        return []
    
    if pdf_path.endswith('.txt'):
        with open(pdf_path, 'r', encoding='utf-8') as f:
            full_text = f.read().strip()
    else:
        try:
            reader = PdfReader(pdf_path)
            full_text = []
            for p in reader.pages:
                text = p.extract_text() or ""
                full_text.append(text)
            full_text = "\n".join(full_text).strip()
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
            return []
    
    if not full_text:
        return []
    
    paragraphs = full_text.split('\n\n')
    chunks = []
    
    for paragraph in paragraphs:
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        if len(paragraph.split()) <= chunk_size:
            chunks.append({"text": paragraph})
        else:
            sentences = paragraph.split('. ')
            current_chunk = []
            current_length = 0
            
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                    
                current_chunk.append(sentence)
                current_length += len(sentence.split())
                
                if current_length >= chunk_size:
                    chunk_text = '. '.join(current_chunk)
                    if chunk_text:
                        chunks.append({"text": chunk_text})
                    
                    overlap_sentences = current_chunk[-1:] if current_chunk else []
                    current_chunk = overlap_sentences
                    current_length = sum(len(s.split()) for s in overlap_sentences)
            
            if current_chunk:
                chunk_text = '. '.join(current_chunk)
                if chunk_text:
                    chunks.append({"text": chunk_text})
    
    return chunks
