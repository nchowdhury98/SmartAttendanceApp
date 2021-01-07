import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)




def get_sheet_name(year ,subject):
    sheet_name_list = ["IT 2nd Year" ,"IT 3rd Year" ,"IT 4th Year"]
    sheet_number_list = {'Algorithm' :'1' ,'Data Structure' :'2' ,'Maths' :'3'}
    return (sheet_name_list[year -2] ,sheet_number_list[subject])


def get_data(sheet,roll=0):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
    client = gspread.authorize(creds)
    if roll == 0:
        data = sheet.get_all_records()
        print(data)

    else:
        data = sheet.row_values(roll +1)
        print(data)




def get_attendance_st(roll ,year ,subject):
    sheet_info = get_sheet_name(year, subject)
    print(sheet_info)
    s_name = sheet_info[0]
    s_number = sheet_info[1]
    print(s_name)
    print(s_number)
    # accessing data base(sheets)
    client = gspread.authorize(creds)
    sheet = client.open(s_name).get_worksheet(int(s_number))
    get_data(sheet)

    data = [{'Roll No.': 1, 'NAME': 'ABHIK BAKSHI', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 2, 'NAME': 'DEBARSHI MITRA', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 3, 'NAME': 'SWETA PANDEY', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 0, '31-01-2023': 0, '31-01-20298': 0}, {'Roll No.': 4, 'NAME': 'KESHAV TIWARI', '31-01-2020': 0, '31-01-2021': 0, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 5, 'NAME': 'AYUSH KUMAR', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 6, 'NAME': 'MD. MUJAHID ALAM', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 7, 'NAME': 'RISHAB KR. MISHRA', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 0, '31-01-2023': 0, '31-01-20298': 0}, {'Roll No.': 8, 'NAME': 'SOUVIK BHOWMICK', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 9, 'NAME': 'BRIHASI DEY', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 10, 'NAME': 'DHIRAJ RAY', '31-01-2020': 0, '31-01-2021': 0, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 11, 'NAME': 'JYOTISKA MAITY', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 0, '31-01-2023': 0, '31-01-20298': 0}, {'Roll No.': 12, 'NAME': 'BIPRADIP GAYEN', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 13, 'NAME': 'DANIYAL AHMAD', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 14, 'NAME': 'MD. ZEESHAN RAZA', '31-01-2020': 0, '31-01-2021': 0, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 15, 'NAME': 'AHSAN ALI', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 16, 'NAME': 'ARBAZUR RAHMAN', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 17, 'NAME': 'RITURAJ DAS', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 18, 'NAME': 'ABHISHEK KUMAR GUPTA', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}, {'Roll No.': 19, 'NAME': 'JAMIR HOSSEN SK.', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 0, '31-01-2023': 0, '31-01-20298': 0}, {'Roll No.': 20, 'NAME': 'ANIKET SINGH', '31-01-2020': 1, '31-01-2021': 1, '31-01-2022': 1, '31-01-2023': 1, '31-01-20298': 1}]
    index = roll -1
    Present = []
    Absent = []
    Total_class = len(data[0]) - 2
    Class_attended = 0
    print(Total_class)
    student_rec = data[index]
    for i in student_rec:
        if i == 'Roll No.':
            o = 0
        else:
            if i == 'NAME':
                o = 0
            else:
                if student_rec[i] == 0:
                    Absent.append(i)
                else:
                    Present.append(i)
                    Class_attended += 1
    print(Present, Absent, Class_attended)
    percentage = (Class_attended / Total_class) * 100
    print(str(percentage) + ' %')


def get_attenddance_tr(year, subject):
    sheet_info = get_sheet_name(year, subject)
    print(sheet_info)
    s_name = sheet_info[0]
    s_number = sheet_info[1]
    print(s_name)
    print(s_number)


print(get_attendance_st(5, 3, 'Algorithm'))
