from langchain.text_splitter import CharacterTextSplitter # pyright: ignore[reportMissingImports]
def read_job_description(job_description_text, chunk_size=500, chunk_overlap=50):
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = text_splitter.split_text(job_description_text)
    jd_text = "\n\n".join(chunks)

    return jd_text