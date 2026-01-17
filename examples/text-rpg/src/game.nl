# Text RPG - Complete NLS Example

@module game
@target python
@imports entities, combat

@type RoundResult {
  over: boolean
  status: string
  hero_msg: string
  monster_msg: string
}

[execute-round]
PURPOSE: Execute one round of combat (Hero attack then Monster attack)
INPUTS:
  - hero: Entity
  - monster: Entity
  - round_num: number
LOGIC:
  1. hero_result = attack(hero, monster)
  2. is_game_over = hero_result.target_dead
  3. monster_msg = ""
  4. IF not is_game_over THEN monster_msg = attack(monster, hero).message
  5. IF not is_game_over THEN is_game_over = hero.hp <= 0
  6. status = "Round " + str(round_num) + " complete."
  7. IF hero_result.target_dead THEN status = "VICTORY! " + monster.name + " defeated."
  8. IF hero.hp <= 0 THEN status = "DEFEAT! " + hero.name + " died."
RETURNS: RoundResult(is_game_over, status, hero_result.message, monster_msg)

@main {
  PRINT "=== NLS TEXT RPG ==="
  PRINT "Initializing from compiled .nl files..."
  
  hero = create-hero("Gandalf")
  monster = create-monster("Goblin", 1)
  
  PRINT hero
  PRINT monster
  PRINT "BATTLE START!"
  
  round_num = 1
  WHILE hero.hp > 0 and monster.hp > 0 {
    result = execute-round(hero, monster, round_num)
    PRINT result.hero_msg
    PRINT result.monster_msg
    PRINT result.status
    round_num = round_num + 1
  }
}
