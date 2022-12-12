Slot file are .slot files.
They are text file with one entry per line.
The following constructs are available:

Optional words
this is [a] test - the word "a" may or may not be present

Alternatives
set color to (red | green | blue) - either "red", "green", or "blue" is possible

Substitutions
ten:10
(television | tele):tv
(medium | half):50

Haroun have some default slots you can use. Make sure your slots names aren't in conflict with Haroun's ones.

Examples :

For example the file slots/movie could contain following lines.
Primer
Moon
Chronicle
Timecrimes
Mullholand Drive

For example the file slots/room could contain following lines.
(playroom | downstairs):playroom
(living room | lounge):lounge
(bedroom | room | chamber):bedroom
([ground | first] floor):first floor
