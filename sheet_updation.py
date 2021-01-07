creds = ServiceAccountCredentials.from_json_keyfile_name("cred.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open("demo").sheet1
        print(sheet)
        data = sheet.get_all_records()
        length = len(data[0])
        last_roll = data[-1]['Roll No.']
        # print(last_roll)
        # print(length)
        final_attend = [date]
        for i in range(1, last_roll + 1):
            if i in absent_list:
                final_attend.append('0')
            else:
                final_attend.append('1')
        print(final_attend)
        print(data)
        # updating attendance in sheet

        h = rowcol_to_a1(1, length + 1) + ':' + rowcol_to_a1(last_roll + 1, length + 1)
        # print(h)
        cell_list = sheet.range(h)
        print(cell_list)
        for cell, atend in zip(cell_list, final_attend):
            cell.value = atend
        sheet.update_cells(cell_list)
