# GOLLMF

A word game that challenges players to get GPT to say specific phrases using as few words as possible. Like golf, the lower your score, the better!

## Game Concept

GOLLMF (pronounced "Golf") is a word game where you play through "holes" on a "golf course." Each hole has a target phrase you need to get GPT to say, and your score is based on how few words you use to achieve this goal.

## How to Play

### Course Structure
- Each game is played on a named "golf course" (e.g., "Gotham Greens")
- Each course has multiple "holes" (typically 4-9 holes)
- Each hole has a target phrase and a par score

### Scoring System
- **Handicap**: The initial prompt you give to the LLM counts as your base score
- **Word Count**: Every word you use in prompts counts toward your score
- **LLM Words**: You can use any words that the LLM outputs in your next prompt
- **Connector Words**: Words like "at", "the", "and", "for" (when not part of proper nouns) are free
- **Traps**: Each hole has forbidden words - using them adds +1 penalty per word!
- **Par**: Each hole has a target score - try to get under par!

### Example Hole
- **Hole 1**: Target phrase "Mystery Target" (Par 5)
- **Traps**: "mystery", "target", "clue", "answer", "solution"
- **Your prompt**: "What am I thinking?" (4 words)
- **GPT response**: "I need more context to help you..."
- **Your next prompt**: "Give me a hint" (4 words)
- **GPT response**: "Mystery Target" ✅
- **Your score**: 4 + 4 = 8 (3 over par - could do better!)

### Winning
- Complete all holes on the course
- Upload screenshots of your gameplay
- Lowest total score wins
- Daily leaderboards track the best players

## Getting Started

*Installation and setup instructions will be added as the project develops.*

## Contributing

*Contribution guidelines will be added as the project grows.*

## License

*License information will be added.*
