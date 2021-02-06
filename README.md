# Telegram Shop Bot in Python

Here you can find the work that i've done for a online shopping store that wanted to sell and promote their products via Telegram.
What i've done basically is use their website backend done with wix to extract the data from the database of wix store and make it shareble
via json post that i can obtain by parsing some specific links, for doing that on your Wix website i suggest to you to have a look to their API
and documentation that was very useful in my case. 
What the bot does is splitting the store in two parts, one channel and one bot, on the channel the admin wich can manage the chanell from another
bot can post links and images of the products of the store in the Telegram channel by getting the last product or searching for a specific product. 
The users that navigate on the channels from the product that they like, they can cooy the id of it and after initializing the bot, they can paste the id 
of the product and create an order that asks for different information, 1st print a photo of the product to confirm if the product is what they wanted. 
After that it asks for some information, like size of the product,  name and adress, payment method etc... 
The order will be saved on a csv file contained in google drive, and the admin will be notified for the purchase on the admin bot. 

If you like some more information feel free to add an issue or contact me via email [email](lorenzo.demiri96@gmail.com)
