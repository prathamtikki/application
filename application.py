import smtplib
    email = input("Please Enter your email id:")
    pin_code = int(input("Please enter the deseired area pincode:"))
    while True:

        import datetime
        import time
        import requests
        from plyer import notification
       
        time.sleep(15)
        get1 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date=04-05-2021".format(
            pin_code)
        response = requests.get(
            get1)  # api request from govt API Sethu,can be modified with .format string to change pincode
        data = response.json()
        #print(data)
        l = []
        for i in data['centers']:
            d = {}
            for j in i:
                if j in ["name", "fee_type"]:
                    d[j] = i[j]
                if j == 'sessions':
                    d[j] = []
                    for m in i[j]:
                        d1 = {}
                        for k in m:
                            # print(k)
                            if k in ["date", "available_capacity", "min_age_limit", "vaccine"]:
                                d1[k] = m[k]
                        d[j].append(d1)
                    l.append(d)
        #print(l)
        for i in range(len(l)):
            for j in range(len(l[i]['sessions'])):
                if l[i]['sessions'][j]['available_capacity'] > 0:
                    print(l[i]['sessions'][j]['available_capacity'])
                    if len(data["centers"]) == 0:

                        continue
                    #elif l[i]['sessions'][j]['min_age_limit'] == 45:
                        #continue
                    else:
                        while (True):  # only sends notif is 18+
                            available = True
                            notification.notify(
                                # title of the notification,
                                title="COVID19 Vaccine stats on {}".format(datetime.date.today()),
                                # the body of the notification
                                message="VaccineS aVAILABLE AT:\n "
                                        "Name: {name}\nAvailible : {capacity}\nvaccine :{vaccine}\nFee :{fee}\n".format(
                                    name=l[i]["name"],
                                    capacity=l[i]["sessions"][j]["available_capacity"],
                                    vaccine=l[i]["sessions"][j]["vaccine"],
                                    fee=l[i]["fee_type"]),
                                timeout=50
                            )
                            if available == True:
                                conn = smtplib.SMTP('smtp.gmail.com', 587)  # smtp address and port
                                conn.ehlo()  # call this to start the connection
                                conn.starttls()  # starts tls encryption. When we send our password it will be encrypted.
                                conn.login('pratham.tikkisetty@gmail.com', 'Xsw2#edc')  # enter  email and password
                                toAddress = "{}".format(email)
                                conn.sendmail('pratham.tikkisetty@gmail.com', toAddress,
                                              'Subject: Vaccine Available!\n\nAttention!\nVaccines Have been made available\nPlease follow the link \nhttps://www.cowin.gov.in/home')
                                conn.quit()
                                #print('Sent notification e-mails for the recipient\n')
                                break
                            else:
                                '''print('Vaccine Not Available')'''
