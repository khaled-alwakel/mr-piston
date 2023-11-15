# mr piston
### video demo: https://www.youtube.com/watch?v=y4GFwNEyVyI
- mr piston is simple web application it's about car maintenance .
- i thought it will be good idea to make app let the users see the company products and enjoy thier services, also they can likes some product and put in in favorites .
- also user can make an appointment . he can choose car brand and the day he want to come to the company to fix his problem it will be nice to make them see thier booking table so he can cancel one if he want.
- i gave user control of his account he can update his username and his password easily. so i worked on that idea and made this simple app .
### mr piston is a simple web app allows you to do the following:
- review the home page  services page , products page , booking page, and settings page here i used aside to navigate the menu links easily . and reach any link from any page of webapp with nice hover effect.
- right side has the special services like outdoor service and emergency and home service . with the coast of it . next to it is the location information to ake it easy for users to find the company . also provided the gmail. and the phone numberd
- sign up and if there any of the inputs blank error will eccoured or the password dont match  also if the name already registred i used database and made users table  and python to manage register route and with jinja to show user the form.
- i made a an apology page let the user know what he did wrong so he can be able to avoid that certain mistake and re signup again correctlty.
- after user successfully registered he will go to login page and enter his data and also i made error checking if any input is blank or wrong name , and apology page will appear if he did something wrong telling him what he has done wrong.so he can avoid it
- once the user in  he will be able to see extra links at aside the cart link and the add to cart link also appointment and his appointments and settings, he can see the homepage . i used grid css to ensure everything working responsivly.
- the products page has several products in it with grid also , and i added a add to cart button so he can add his favorites items to his cart.
- user can go and see what he have choose as fovrites i used a list to append the id of every product and used jinja to show the products and favorites , grapping them from databse .
- also you can make an appointment you can check your appointments table and if you want to delete an appointment it's provided. i used list for the services to show it in appointment page so the user can choose from them . with jinja i can take that list and present it in the page
- i made the chooses like checkboxes so if he want to choose many services instead of radio button . in radio button he will choose one item only, in real life you can make multiple things in your car so it's logical to let the user choose many choces
- i made atable of his appointment so he can review it and if he want to cancel an appointment he can easly press the delete button .
- you can also update  your name if it's only exist in database and if you didnt input error will occure, an apology page will appear in case of error so ther user know what is happening and avoid his mistake
- and also update your password dont accept any missing fields and if the old password isn't match the one in the database for that person an apology page will appear in case of error so ther user know what is happening and avoid his mistake
- it is the same page of an apology but with the help og jinja i send a specefic message to the apology page variable so the page can show it . diffrent apology message in the same page .
- i tried to make it as responsive as i can i used media query in it i used the tablet and mobile width so if user go into the webapp from desktop or laptop or tablet or mobile he will not facing any problems.
- i tried to make it looks good as i could . i did some projects with html and css before
- i used javascript in the mobile screen with the menu button you can shows and dont show the menu
- my data base has users table and appointments table and part table  i use relational databases concept between tables so i can show the right appointment for particular user.

