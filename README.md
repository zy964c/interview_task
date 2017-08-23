# task1
This web app recieves arbitrary number of parameters via POST request to `/get_form`, validates input and searches through the database for a record with the most number of matches.

Returnes `{record number: number of matches}`. If unknown fields were submitted returnes `{field name: type of data}`
