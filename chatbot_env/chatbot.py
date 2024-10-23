import google.generativeai as genai
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

def init_gemini():
    """Initialize Gemini model."""
    # Replace with your API key
    GOOGLE_API_KEY = "AIzaSyBPgo96MnIClI34mqXv5mppsT2vAchuny4"
    # GOOGLE_API_KEY = "AIzaSyDMRjSfK5Gzk44QOOU6D7pr9K50bGMni_k"
    genai.configure(api_key=GOOGLE_API_KEY)

    generation_config = {
        'max_output_tokens': 70,  # Approximately 2-3 lines of text
        'temperature': 0.7,
        'top_p': 0.8,
        'top_k': 40
    }

    model = genai.GenerativeModel('gemini-1.5-flash',generation_config=generation_config)
    return model

def create_context(transcript):
    """Create a context message for Gemini."""
    return f"""You are a helpful assistant that has watched a video with the following transcript:
    {transcript}
    
    Please answer questions about this video's content. If the question is not related to the video,
    politely redirect the user to ask about the video content."""

def chat_with_gemini(url):
    """Main function to run the chatbot."""
    # Get transcript and initialize model
    transcript = get_transcript(url)
    if transcript.startswith("Error"):
        print(transcript)
        return
    
    model = init_gemini()
    context = create_context(transcript)
    
    # Initialize chat
    chat = model.start_chat(history=[])
    chat.send_message(context)
    
    print("Chat initialized! Ask questions about the video (type 'quit' to exit)")
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == 'quit':
            break
            
        try:
            response = chat.send_message(user_input)
            print("\nBot:", response.text)
        except Exception as e:
            print(f"\nError: {str(e)}")

# Example usage
if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    chat_with_gemini(video_url)