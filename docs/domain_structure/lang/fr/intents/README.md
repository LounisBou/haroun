Intents files are .ini files.
There are used to define the intents for the domain.
Sentence templates are based on the JSGF standard. The following constructs are available:

Optional words
this is [a] test - the word "a" may or may not be present

Alternatives
set color to (red | green | blue) - either "red", "green", or "blue" is possible

Tags
turn on the [den | playroom]{location} light - named entity location will be either "den" or "playroom"

Substitutions
make ten:10 coffees - output will be "make 10 coffees"
turn off the: (television | tele):tv - output will be "turn off tv"
set brightness to (medium | half){brightness:50} - named entity brightness will be "50"

Rules
rule_name = rule body can be referenced as <rule_name>

Slots
$slot_name will be replaced by a list of sentences in the replacements argument. The slot name is the name of the slot file.
See slots/README.md for more information about slot creation.

Rules
Named rules can be added to your template file using the syntax:
rule_name = rule body
and then reference using <rule_name>. The body of a rule is a regular sentence, which may itself contain references to other rules.
You can refrence rules from different intents by prefixing the rule name with the intent name and a dot. (See exemples)

Converters
You can add converters to your template file following a word, sequence, 
or tag name with "!converter" will run "converter" on the string value during recognize. 
Default converters are :
int - convert to integer
float - convert to real
bool - convert to boolean
lower - lower-case
upper - upper-case

Special Cases
If one of your sentences happens to start with an optional word (e.g., [the]), this can lead to a problem:
[wrong_intent]
[the] problem sentence
Python's configparser will interpret [the] as a new section header, which will produce a new intent, grammar, etc. Rhasspy handles this special case by using a backslash escape sequence (\[):
[correct_intent]
\[the] problem sentence

Examples:

[intent]
a sentence in a different intent

[set_color]
set light to (red | green | blue)

[light_on]
turn on [the] (living room lamp | kitchen light){name}

[set_brightness]
set brightness to (one: hundred:100)!int

[intent_with_rule_1]
rule = a test
this is <rule>

[intent_with_rule_2]
rule = this is
<rule> <Intent1.rule>
