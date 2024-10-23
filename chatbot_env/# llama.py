from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """Extract video ID from YouTube URL."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]
    if parsed_url.hostname in {'www.youtube.com', 'youtube.com'}:
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
    raise ValueError('Invalid YouTube URL')

def get_transcript(url):
    """Get transcript from YouTube video."""
    try:
        video_id = get_video_id(url)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return ' '.join([entry['text'] for entry in transcript_list])
    except Exception as e:
        return f"Error getting transcript: {str(e)}"

def create_chatbot():
    # Initialize Ollama
    llm = OllamaLLM(model="llama3.1")  # Change to the model you have installed in Ollama
    
    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that answers questions based on the provided YouTube video transcript. 
         Only answer questions that can be answered using information from the transcript.
         If the question cannot be answered using the transcript, politely inform the user and ask them to ask a question about the video content.
         
         Transcript: {transcript}"""),
        ("human", "{question}")
    ])
    
    # Create the chain
    chain = prompt | llm
    return chain

def main():
    print("Welcome to YouTube Video Q&A Bot!")
    
    # Get video URL and transcript
    while True:
        url = input("\nEnter the YouTube video URL (or 'quit' to exit): ")
        if url.lower() == 'quit':
            break
            
        try:
            transcript = get_transcript(url)
            print("\nTranscript loaded successfully! You can now ask questions about the video.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Please try again with a valid YouTube URL.")
    
    # Create the chatbot
    chain = create_chatbot()
    
    # Start the Q&A loop
    while True:
        question = input("\nAsk a question about the video (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
            
        try:
            response = chain.invoke({
                "question": question,
                "transcript": transcript
            })
            print("\nAnswer:", response)
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()