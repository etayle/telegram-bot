#!/usr/bin/python
import gspread
gc = gspread.service_account(filename= '/root/telegram_bot/Four-species/four-species-325810-093c62e6fccb.json')

sh = gc.open_by_key('1B5kqMI7IIHKCFgcvP2bbIXT03JDloynf_QYOQNphmt4').worksheet('w1')
order = ['city','name','detail','quntity','address','phone_number','cost']
text = "איתי משה לוי"
max_rows = len(sh.get_all_values())
for row_numner in range(1,max_rows+1) :
    values_list = sh.row_values(1)
    print(values_list)
    for cell in sh.row_values(row_numner):
        print(cell)
        if cell == text:
            find_row = sh.row_values(row_numner)
        else:
            continue
        break
if find_row == None:
        print("לא נמצא אדם עם המזהה הנ''ל")
else:
        replay_messege = "עיר: " + find_row[0] +'\n' + 'שם : ' + find_row[1] + '\n' +  ' פרטי הסט ' + find_row[2]+ '\n' + ' כמות: ' + find_row[3] + '\n' + 'כתובת: ' + find_row[4] + '\n' + 'מספר פלאפון: ' + find_row[5]
        print(replay_messege)