import requests

def reqst(payload):
	r = requests.post("http://127.0.0.1:5000/get_form", data=payload)
	print r.text
	return r.json()

if __name__ == "__main__":

	payload = {"date":"12/09/2016","phone":"86-(636)213-3610","email":"sdevilrr@friendfeed.com","text":"protocol"}
	payload1 = {"date":"04/12/2016","phone":"66-(885)648-5373","email":"pschechter0@flickr.com","text":"implementation"}
	payload2 = {"time":"86-(636)213-3610","phone":"sdevilrr@friendfeed.com","email":"qwerty","text":"12/09/2016"}
	payload3 = {"text":"architecture"}
	resp = reqst(payload)
	assert(resp == {"Matches": 4, "Form": "Form 1000"}), 'Not correct responce'
	resp = reqst(payload1)
	assert(resp == {"Matches": 4, "Form": "Form 1"}), 'Not correct responce'
	resp = reqst(payload2)
	assert(resp == {"phone": "email", "text": "date", "email": "text", "time": "phone"}), 'Not correct responce'
	resp = reqst(payload3)
	assert(resp == {"Matches": 1, "Form": "Form 675"}), 'Not correct responce'
	print 'No errors found'