import os
import slackclient  # import SlackClient


BOT_NAME = 'dice_bot'
BOT_TOKEN = 'xoxb-260663448688-thEsNqu4dUe3tACHWBjnhj2f'

#slack_client = SlackClient(os.environ.get('slack_bot_token'))

dice_bot_slack_client = slackclient.SlackClient(SLACK_BOT_TOKEN)
print(BOT_NAME)
print(BOT_TOKEN)

is_ok = dice_bot_slack_client.api_call("users.list").get('ok')
print(is_ok)

if(is_ok):
    for user in dice_bot_slack_client.api_call("users.list").get('members'):
        if user.get('name') == BOT_NAME:
            print(user.get('id'))

BOT_ID = 'U7NKHD6L8'

# if __name__ == "__main__":
#     api_call = slack_client.api_call("users.list")
#     if api_call.get('ok'):
#         # retrieve all users so we can find our bot
#         users = api_call.get('members')
#         for user in users:
#             if 'name' in user and user.get('name') == BOT_NAME:
#                 print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
#     else:
#         print("could not find bot user with the name " + BOT_NAME)