.. role:: raw-html-m2r(raw)
   :format: html


TradingView webhook
===================

With OctoBot, you can listen to https://www.tradingview.com signals and automate trades.

OctoBot configuration
---------------------

Simply add the Trading-view service into your OctoBot's configuration and setup your `webhook service <Using-a-webhook-with-OctoBot.html>`_.

TradingView account
-------------------


* Create an account at https://www.tradingview.com (join for free button)
* To be able to send signals from tradingview.com, you need a pro account, if you don't have one, you can use the pro trial by clicking on

  .. image:: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-go-pro-trial-button.png
     :width: 200 px
     :target: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-go-pro-trial-button.png
     :alt: start-free-trial-button

* Add your credit card or paypal account to validate your trial account and click on

  .. image:: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-start-trial-button.png
     :width: 400 px
     :target: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-start-trial-button.png
     :alt: start-trial-button

Your account is now ready to be used with OctoBot !

Create an alert
---------------


* Go to the right menu and click on the alert button

  .. image:: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-alert-menu.png
     :width: 300 px
     :target: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-alert-menu.png
     :alt: alert-menu-button

* Create a new alert with

  .. image:: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-add-alert-button.png
     :width: 75 px
     :target: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-add-alert-button.png
     :alt: create-alert-button

* Choose the condition : an indicator cross, a price drop, whatever you want
* Add your OctoBot webhook as the following screenshot.

  .. image:: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-alert-webhook-url.png
     :width: 300 px
     :target: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-alert-webhook-url.png
     :alt: set-webhook-url

  You can find OctoBot's webhook on your OctoBot's configuration page or in OctoBot's starting logs if you activated a webhook requiring tentacle (like trading view signals trading mode). It should be an url like http://XXXXXXXX.ngrok.io/webhook/trading_view.

  .. image:: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/webhook_config.jpg
     :target: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/webhook_config.jpg
     :alt: webhook and tradingview config


  .. image:: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/webhook_log.jpg
     :target: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/webhook_log.jpg
     :alt: webhook log

* Set the alert message to 
  .. code-block::

     EXCHANGE={{exchange}}
     SYMBOL={{ticker}}
     SIGNAL=BUY

  if it's a buy signal

OR

.. code-block::

   EXCHANGE={{exchange}}
   SYMBOL={{ticker}}
   SIGNAL=SELL

if it's a sell signal


.. image:: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-alert-message.png
   :width: 400 px
   :target: https://raw.githubusercontent.com/Drakkar-Software/OctoBot/assets/wiki_resources/tradingview-alert-message.png
   :alt: alert-message


You can also use a token to add a security layer on your webhook using an identification token, this token is randomly generated by your OctoBot and can be found on the configuration interface and in execution logs.

To add your token on the tradingview.com signal: add the following line to the alert message:

.. code-block::

   TOKEN=YOUR_TOKEN
