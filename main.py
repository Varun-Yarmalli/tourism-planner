"""
Main script for the Multi-Agent Tourism System
"""
from tourism_agent import TourismAgent


def main():
    """Main function to run the tourism system"""
    print("=" * 60)
    print("Welcome to the Multi-Agent Tourism System!")
    print("=" * 60)
    print("\nYou can ask about weather, places to visit, or both.")
    print("Examples:")
    print("  - 'I'm going to go to Bangalore, let's plan my trip.'")
    print("  - 'I'm going to go to Bangalore, what is the temperature there'")
    print("  - 'I'm going to go to Bangalore, what is the temperature there? And what are the places I can visit?'")
    print("\nType 'quit' or 'exit' to stop.\n")
    
    agent = TourismAgent()
    
    while True:
        try:
            user_input = input("\nEnter your query: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nThank you for using the Tourism System. Goodbye!")
                break
            
            print("\n" + "=" * 60)
            print("Processing your request...")
            print("=" * 60 + "\n")
            
            response = agent.process_request(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nThank you for using the Tourism System. Goodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()

