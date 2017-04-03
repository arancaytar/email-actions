# Table Of Contents

- [email-actions](#email-actions)
- [Why did you make email-actions](#why-did-you-make-email-actions)
- [What are the benefits/differences compared to hosted services like IFTTT](#what-are-the-benefits-differences-compared-to-hosted-services-like-ifttt)
- [Current high level feature list](#current-high-level-feature-list)
- [Installation](#installation)
- [Usage](#usage)
  * [Config file format / Plugin settings](#config-file-format---plugin-settings)
- [Contributing](#contributing)
  * [How to write a plugin](#how-to-write-a-plugin)
  
# email-actions
email-actions is a tiny SMTP server with a rules based engine to trigger any actions (notifications/commands etc) based on the emails sent to this server.
Think of it like [IFTTT](https://ifttt.com) but where input trigger is email and can be set up and run locally as well.

# Why did you make email-actions
Like most of my projects, email-actions is a 'scratch-your-own-itch' project. I bought a NAS (Synology ds216j) which also doubled as a downloader of anime/tv shows etc through RSS using its inbuilt "Download Station" app. I also used Plex to watch them over the network but these needed to be moved to a proper folder and named in a specific format (and some crap deleted and other maintenance done or sometimes some post processing done) to have Plex display/play them properly. I used Filebot and a few custom scripts for this but had to either do this manually or use a fixed time task scheduling (which tended to delay watching). This was semi-irritating. 
I also wanted to know when something had been downloaded so I could binge on that latest episode as soon as it was done :)
Download station had a hack (by changing internal files) to run custom script after a download was completed but it had to be redone after every firmware update and sometimes, after every restart. And finally it stopped working altogether with recent updates.

It did support email notifications though. Thus email-actions was born. So I could push notifications for downloaded items run my custom scripts on the downloaded items.

Since then, I've started using it for many other things as email is pervasive and most of the devices support email based notifications. So I can trap them and carry out other actions.

# What are the benefits/differences compared to hosted services like IFTTT
IFTTT provides email hooks as well. I *think* email-actions may be an alternative (you can decide whether it's better or not) with respect to below:
- IFTTT works as a client once email is received so you still need an available SMTP server to be able to send email. This can be expensive or risky as you'd have to share your server username/pwd to the email sending entity. email-actions is an SMTP server that takes actions before any actual email delivery.
- Can be run locally with minimal dependencies. You don't need to send your data to internet or even have an internet connection
- Tiny footprint
- Can run local commands as well while IFTTT still needs to be integrated with something else if that's what you need
- You are in control of your info
- Free(er), that is, no limitations on hooks/conditions etc

# Current high level feature list
- aiosmtpd based for aync email processing for performance
- The action execution is also asyncio based, so will free up the email sender while processing the action in background
- Easy yaml based configuration
- Global or local variables for full customization/reuse
- Action decision based on "To" email address filtering (Addition of many other filters on the roadmap)
- Plugins supported:
  - [Join](https://joaoapps.com/join/) push notifications (Will add pushbullet if there's a demand or can use custom external script for now)
  - Custom Local commands (Any arguments, any script type, custom environment variables)
  - Email (Can forward the email to custom upstream servers further if needed for more actions or actual email delivery)

# Installation

Pre-requisites: You need Python 3.4+ to be able to run this

- Install using pip (May need to use `pip3` instead of `pip` according to your OS/python installation. May need to use `sudo` prefix before below command if installing system wide)

`pip install email-actions` 

- Install directly

```
git clone git@github.com:shantanugoel/email-actions.git
cd email-actions
python setup.py install
```

# Usage

```
usage: email_actions [-h] [-v] [-H HOSTNAME] [-p PORT] [-l LOG] -c CONFIG

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -H HOSTNAME, --hostname HOSTNAME
                        Host IP or name to bind the server to
  -p PORT, --port PORT  Port number to bind the server to
  -l LOG, --log LOG     Set log level. 0=> Warning, 1=>Info, 2=>Debug

required arguments:
  -c CONFIG, --config CONFIG
                        Specify config file (yaml format) to be used. If it
                        doesn't exist, we'll try to create it

```

Most of the options above are self explanatory. If you don't specify a hostname, it will choose `localhost` by default. If you don't specify a port, it'll choose `8025` by default. 

Specifying a config file is mandatory. If the specified file doesn't exist, we'll generate a dummy one which you can fill. But essentially this is a step that you can't avoid. The config file is explained in more detail below.

## Config file format / Plugin settings

# Contributing
Feel free to fork the repo and send PRs for any changes. If you can't make changes but want to report issues or provide feedback, open an Issue on github or ping me on twitter [@shantanugoel](https://twitter.com/shantanugoel)

You can contribute either to the core or write a plugin for your usecase. The only guiding principle is to keep it as simple/minimal as possible.

## How to write a plugin
Take a look at any plugin in [plugins](https://github.com/shantanugoel/email-actions/tree/master/email_actions/plugins) directory
A minimal plugin needs to do following things:
- Define 'PLUGIN_NAME'. This need not be same as the file name but is preferred to keep that way
- A function that takes these parameters: `filter_name, msg_from, msg_to, msg_subject, msg_content` and doesn't return anything
- Read plugin's configuration (if any) using email_actions.config.read_config_plugin function
  - Ideally the plugin should not need to use any other function from the core
- After writing the plugin, add the plugin's name and entry function in `entry_funcs` dict in [plugins init file](https://github.com/shantanugoel/email-actions/tree/master/email_actions/plugins/__init__.py)
