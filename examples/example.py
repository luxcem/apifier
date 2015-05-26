from apifier import Apifier

api = Apifier(description_file='bieremonde.json')
print(api.load())
