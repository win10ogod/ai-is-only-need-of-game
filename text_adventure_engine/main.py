#!/usr/bin/env python3
import os
import asyncio
import argparse
from dotenv import load_dotenv
from .ui.game_cli import GameCLI

def main():
    """Main entry point for the text adventure engine."""
    parser = argparse.ArgumentParser(description='Text Adventure Game Engine')
    parser.add_argument('--game-dir', type=str, default='game',
                      help='Directory containing game configuration (default: game)')
    parser.add_argument('--create-config', action='store_true',
                      help='Create default configuration files')
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()
    
    # Check for OpenAI API key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return

    # Create game directory if it doesn't exist
    os.makedirs(args.game_dir, exist_ok=True)

    # Initialize game CLI
    game = GameCLI(args.game_dir, openai_api_key)

    if args.create_config:
        game.storage.create_default_config()
        print(f"Created default configuration in {args.game_dir}")
        return

    # Run the game
    try:
        asyncio.run(game.run())
    except KeyboardInterrupt:
        print("\nGame terminated by user.")
    except Exception as e:
        print(f"\nError running game: {str(e)}")

if __name__ == "__main__":
    main()