# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# smtp_login = 'bot.ranepatypography@gmail.com'
# smtp_password = 'qopymbcdeiaosxfo'

# # создаем письмо
# msg = MIMEMultipart()
# msg['From'] = smtp_login
# msg['To'] = email
# msg['Subject'] = f"Оплаченный онлайн-заказ №{count}"

# body = f'Черно-белая печать\n' \
#         f'Количество копий: {user["copies"]}\n' \
#         f'Количество страниц в файле: {user["pages"]}\n' \
#         f'Корпус №{user["corpus"]}'

# msg.attach(MIMEText(body, 'plain'))

# # добавляем файл в письмо
# with open(file_path, 'rb') as f:
#     filename = file_path.split('/')[-1]
#     file_data = f.read()
#     attachment = MIMEApplication(file_data, Name=filename)
#     msg.attach(attachment)


# # отправляем письмо
# server = smtplib.SMTP(smtp_server, smtp_port)
# server.starttls()
# server.login(smtp_login, smtp_password)
# server.sendmail(smtp_login, email, msg.as_string())
# server.quit()
