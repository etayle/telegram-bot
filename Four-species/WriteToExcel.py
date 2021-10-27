from openpyxl import load_workbook
from openpyxl.descriptors.base import String
from openpyxl.workbook import workbook
workbook_name = "/root/telegram_bot/Four-species/Orders.xlsx"
wb = load_workbook(workbook_name)
page = wb.active
new_order = []
new_order.append(input("הכנס שם  "))
new_order.append(input("הכנס פרטי סט "))
new_order.append(input("כתובת "))
new_order.append(input("מספר פלאפון"))
new_order.append(input("מחיר"))
page.append(new_order)
wb.save(filename=workbook_name)

