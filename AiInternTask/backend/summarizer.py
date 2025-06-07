from transformers import pipeline

# Load the summarization pipeline once
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Summarize multiple chunks into a single theme
def summarize_chunks(chunks):
    combined_text = " ".join(chunk['document'] for chunk in chunks)
    if len(combined_text) > 1024:
        combined_text = combined_text[:1024]  # distilbart has a token limit

    summary = summarizer(combined_text, max_length=100, min_length=30, do_sample=False)
    return summary[0]['summary_text']
