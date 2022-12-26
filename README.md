# telegram_bot

## Input files

It requires the following three input files,

1. config.json - Please add your telegram bot token in the 'token' field. This token is a secret key to your bot, so make sure to keep it safe.
2. group_details.xlsx - Please enter the channel IDs of all the groups you want to send this post to.
3. post.txt - Please enter the post you have created in this file

## Usage

The following command should be run from cmd window to start the file
python .\telegram_bot.py --configJson ./inputs/config.json
