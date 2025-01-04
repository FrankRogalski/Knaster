# NN Concept Layers
## Input
* 11 input numbers
* 11 * 25 current numbers
* 25 marked numbers
* 25 empty fields (maybe they can be implicit, but i think its better for performance if they are not?)
* 25 possible fields to mark (if any)
* 1 number of fields to mark 
** maybe in increments of 0.2 since here the closeness of the number actually means something?
** but also 1/3 could be better as the maximum is 3 selectable fields?
* 1 number placement mode
* 1 line selection mode
* 1 field selection mode

## Output
* 25 number output
* 12 row/column selection
* 25 field selection output
