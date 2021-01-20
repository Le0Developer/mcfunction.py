from mcfunction import parse_command
from mcfunction.versions.mc_1_8.summon import ParsedSummonCommand

command = parse_command('summon minecraft:ender_dragon ~ ~ ~')
# command is the parsed command
command: ParsedSummonCommand  # for type-hinting

# you can use 'str(command)' to construct the command from the parsed command
print(command)  # print() automatically calls str()
print(repr(command))  # bypasses str() and lets you see the real 'command'

# modify the node of the summoned entity
command.entity.name = 'wither'

# reconstruction will show the changed command
print(command)
