Dialogs files are no value .ini files. 
They are used to store the dialog data for domains. 
Each sections is a dialog type, and section name is the dialog key.
Each lines of section is a possible sentence dialog that can contains variables (ex : {my_var}).
Variables are replaced by domain values when the dialog is use.
By default a random sentence will be chose by domain, 
but you can force a specific sentence by using the "dialog_position" parameter in the domain file.

Example of a dialog file :
[dialog.key]
This is a dialog sentence with a variable {my_var}
This is another dialog sentence with a variable {my_var}
This is a dialog sentence without variable

[dialog.key2]
This is a dialog sentence with two variables. This is the first variable {my_var} and the second variable is {my_var2}