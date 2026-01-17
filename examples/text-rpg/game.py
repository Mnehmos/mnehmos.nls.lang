import sys
import os
import time

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.entities import create_hero, create_monster
from src.game import execute_round

def main():
    print("=== NLS TEXT RPG ===")
    print("Initializing game engine from compiled .nl files...")
    time.sleep(1)
    
    # Create entities (defined in entities.nl)
    hero = create_hero("Gandalf")
    monster = create_monster("Goblin", 1)
    
    print(f"\nHero initialized: {hero}")
    print(f"Monster initialized: {monster}")
    print("\nBATTLE START!")
    print("-" * 40)
    
    round_num = 1
    while True:
        print(f"\n--- Round {round_num} ---")
        
        # Execute round logic (defined in game.nl)
        result = execute_round(hero, monster, round_num)
        
        # Display results
        if result.hero_msg:
            print(f"{hero.name} attacks... {result.hero_msg}")
            
        if result.monster_msg:
            print(f"{monster.name} attacks... {result.monster_msg}")
            
        if result.over:
            print(f"\n{result.status}")
            break
            
        print(f"Status: {hero.name} {hero.hp}HP | {monster.name} {monster.hp}HP")
        round_num += 1
        time.sleep(1)

if __name__ == "__main__":
    main()
