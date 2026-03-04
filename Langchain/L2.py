from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings,ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()


loader = TextLoader(r"C:\Users\chari\OneDrive\Documents\Python\Langchain\Introduction.txt", encoding="utf-8")
document = loader.load()
#print(document)

splitter = RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap = 120)
chunks = splitter.split_documents(document)

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vectordb = Chroma.from_documents(chunks,embedding=embeddings)

retriverdata = vectordb.as_retriever()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

while True:
    q = input("enter what you want fromthe file: \n")
    data = vectordb.similarity_search(q)
    if q.lower() in {"exit", "quit"}:
        break
    content = "\n".join(d.page_content for d in data)
    response = llm.invoke(f"Answer from this content: \n{content}\n\nQuestion:{q}")
    print(response.content)






