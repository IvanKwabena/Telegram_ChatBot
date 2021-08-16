

ENV = 'DEV'

envs = ['PROD', 'DEV']

# #keys
# for i in envs:
#     if i == 'DEV':
#         TELEGRAM_KEY = os.getenv("TELEGRAM_API_KEY")
#         MONGODB_KEY = os.getenv("MONGODB_API_KEY")
        # bot.infinity_polling() 

    # elif i == 'PROD':
    #     import ast
    #     TELEGRAM_KEY = ast.literal_eval(os.getenv("TELEGRAM_API_KEY"))
    #     MONGODB_KEY = ast.literal_eval(os.getenv("MONGODB_API_KEY"))



#server
host = '0.0.0.0'
port = int(os.environ.get("PORT", 5000))
webhook = 'https://bot-date-reminder.herokuapp.com/'

