#!/usr/bin/env python3
"""
GOLLMF - A word game where you get GPT to say specific phrases using as few words as possible.
"""

import json
import os
from typing import List, Dict, Any

class GOLLMFGame:
    def __init__(self, course_file: str):
        """Initialize a new GOLLMF game with a course."""
        self.course = self.load_course(course_file)
        self.current_hole = 0
        self.score = 0
        self.word_count = 0
        self.game_history = []
    
    def load_course(self, course_file: str) -> Dict[str, Any]:
        """Load a golf course from a JSON file."""
        with open(course_file, 'r') as f:
            return json.load(f)
    
    def start_game(self):
        """Start a new game."""
        print(f"Welcome to {self.course['courseName']}!")
        print(f"{self.course['description']}")
        print("\nYour goal: Get GPT to say the target phrase using as few words as possible.")
        print("Remember: Every word you use counts toward your score!")
        print("\n" + "="*50)
    
    def play_hole(self, hole_number: int):
        """Play a specific hole."""
        if hole_number >= len(self.course['holes']):
            print("Invalid hole number!")
            return
        
        hole = self.course['holes'][hole_number]
        print(f"\nHole {hole['holeNumber']}: {hole['description']}")
        print(f"Target: '{hole['targetPhrase']}' (Par {hole['par']})")
        
        if 'traps' in hole and hole['traps']:
            print(f"⚠️  TRAPS: Avoid these words: {', '.join(hole['traps'])}")
            print("   Each trap word used adds +1 to your score!")
        
        print("Start your conversation with GPT!")
        print("-" * 30)
        
        # Track this hole's progress
        hole_data = {
            'hole_number': hole['holeNumber'],
            'target': hole['targetPhrase'],
            'par': hole['par'],
            'traps': hole.get('traps', []),
            'prompts': [],
            'word_count': 0
        }
        
        return hole_data
    
    def add_prompt(self, prompt: str, hole_data: Dict):
        """Add a prompt to the current hole and update word count."""
        word_count = len(prompt.split())
        hole_data['prompts'].append(prompt)
        hole_data['word_count'] += word_count
        self.word_count += word_count
        
        print(f"Prompt: '{prompt}' ({word_count} words)")
        print(f"Total words this hole: {hole_data['word_count']}")
    
    def check_win(self, gpt_response: str, target: str) -> bool:
        """Check if the GPT response contains the target phrase."""
        # Convert to lowercase for comparison, but preserve original for display
        response_lower = gpt_response.lower()
        target_lower = target.lower()
        
        # Check for exact match or if target is contained in response
        return target_lower in response_lower
    
    def finish_hole(self, hole_data: Dict, gpt_response: str):
        """Finish the current hole and calculate score."""
        target = hole_data['target']
        par = hole_data['par']
        word_count = hole_data['word_count']
        
        print(f"\nGPT Response: '{gpt_response}'")
        
        if self.check_win(gpt_response, target):
            print(f"🎉 SUCCESS! You got '{target}'")
            score_to_par = word_count - par
            if score_to_par < 0:
                print(f"Score: {word_count} words ({abs(score_to_par)} under par!)")
            elif score_to_par == 0:
                print(f"Score: {word_count} words (Par)")
            else:
                print(f"Score: {word_count} words ({score_to_par} over par)")
        else:
            print(f"❌ GPT didn't say '{target}'")
            print(f"Score: {word_count} words (No completion)")
        
        self.game_history.append(hole_data)
        print("-" * 30)
    
    def get_total_score(self) -> int:
        """Get the total score for the game."""
        return self.word_count
    
    def show_leaderboard(self):
        """Show the current game summary."""
        print(f"\n🏆 {self.course['courseName']} - Game Summary")
        print("=" * 50)
        
        total_par = sum(hole['par'] for hole in self.course['holes'])
        
        for hole_data in self.game_history:
            hole_num = hole_data['hole_number']
            target = hole_data['target']
            par = hole_data['par']
            words = hole_data['word_count']
            score_to_par = words - par
            
            status = "✅" if score_to_par <= par else "❌"
            par_text = f"({score_to_par:+d})" if score_to_par != 0 else "(Par)"
            
            print(f"Hole {hole_num}: {target} - {words} words {par_text} {status}")
        
        print(f"\nTotal Score: {self.word_count} words")
        print(f"Course Par: {total_par}")
        print(f"Score to Par: {self.word_count - total_par:+d}")

def main():
    """Main game loop."""
    # Load the Gotham Greens course
    course_file = "courses/gotham-greens.json"
    
    if not os.path.exists(course_file):
        print(f"Course file {course_file} not found!")
        return
    
    game = GOLLMFGame(course_file)
    game.start_game()
    
    # Play through each hole
    for i in range(len(game.course['holes'])):
        hole_data = game.play_hole(i)
        
        # This is where you'd integrate with your GPT API
        # For now, we'll simulate the game
        print("(In a real game, you'd interact with GPT here)")
        print("Type your prompts and GPT responses manually for now.")
        
        # Simulate some gameplay
        game.add_prompt("What store sells clothes?", hole_data)
        print("GPT: Many stores sell clothes, like Uniqlo, H&M, Zara...")
        
        game.add_prompt("Uniqlo competitor?", hole_data)
        print("GPT: Barclays Uniclo")
        
        game.finish_hole(hole_data, "Barclays Uniclo")
    
    game.show_leaderboard()

if __name__ == "__main__":
    main()
