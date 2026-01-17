# Combat Logic

@module combat
@target python
@imports entities

@type CombatResult {
  damage: number
  is_critical: boolean
  target_dead: boolean
  message: string
}

[attack]
PURPOSE: Perform an attack action between two entities
INPUTS:
  - attacker: Entity
  - target: Entity
GUARDS:
  - attacker.hp > 0 -> ValueError("Dead entities cannot attack")
  - target.hp > 0 -> ValueError("Target is already dead")
LOGIC:
  1. damage = attacker.attack - target.defense
  2. is_critical = damage > 10
  3. IF is_critical THEN damage = damage * 2
  4. IF damage < 1 THEN damage = 1
  5. target.hp = target.hp - damage
  6. is_dead = target.hp <= 0
  7. msg = "Hit for " + str(damage)
  8. IF is_critical THEN msg = msg + " (CRITICAL!)"
  9. IF is_dead THEN msg = msg + " - Target slain!"
RETURNS: CombatResult(damage, is_critical, is_dead, msg)

@test [attack] {
  # Tests would go here
}
