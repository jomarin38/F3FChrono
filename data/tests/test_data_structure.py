from data.Event import Event

login=input('F3X Vault login : ')
password=input('F3X Vault password : ')

contest_id=1706

event = Event.from_f3x_vault(login, password, contest_id)
