# Royal Shop

Welcome to ***`Royal online shop`*** platform!

<img src="./preview/Royal Shop.jpg" />

This platform will let users to manage online shopping.

If you wanna add features like `Notification`, `Role base` system & etc. clone the repo create new branch, make changes to the project and finally push your code.

<h2>
Table of contents:
</h2>

<a href="#features">Features</a>  

<a href="#technology stacks">Technology Stack</a>  

<a href="#setup">Setup</a>  

<a href="#backend">Backend Documentation</a>  

<a href="#frontend">Frontend Documentation</a>  

<a href="#contributing">Contributing</a>  

## Features

This platform has these features like:

- Registration via OTP and dynamic **USERNAME_FIELD**
- Authentication using **JWT**
- Cart scenarios
- User's Wishlist
- Full featured Admin Queries
- Payment Integration
- Progress tracking
- Coupon scenarios

## Technology Stacks

We will use these technologies to manage our application:


- **Backend**: Django rest framework

- **Frontend**: React 

- **DevOps**: Docker

- **Database**:PostgreSQL

- **Authentication**: OTP 

- **Cache database**: Redis, Celery


## Setup

We use **Docker** to containerize backend and frontend together.

## Backend

I will use Service-Repository design pattern for **Royal** shop.

We have 5 main Django-applications here:
- ***`user`***: to let users create and manage their accounts.
- ***`store`***: to let users create and manage their carts, orders etc.
- ***`dashboard`***: to let admin see the application status
- ***`club`***: to let customers share their experiences with our app
- ***`payment`***: if any customer wants to buy something, go ahead and allow him/her

The first concept in designing a good backend is ER diagram.

Here is the core functionalities of our ECommerce with ER:

<img src="./preview/ecommerce.png" />

of course this is not the whole Data Base of our api but, It contains the main idea of our ECommerce.

### user app

- **`Authentication`**: In `user` app, I'v customized the the default `User` model of Django. I'v consider `username` as a
`TextField` and so users can send both `email` & `phone`. After users registration, `is_email` get `True` or `is_phone`. Later on we
will use it in `OTP` and since **`OTP**` can be use by his/her owner and yes its an additional layer of security.

- **`OTP`**: In `user` app, I'v added this scenario with security consideration that users need their `otp token` in two places
first in `verify` scenario and than in `password reset`. I'v added this in `password reset` because, If someone grant your
credentials, your whole data is at risk!

### store app

This app has lot of features. I will explain them one by one:

- **`Product`**: I'v added a field named `actualPrice`, its a `GeneratedField` so I use `F`(expression wrapper) to update its value
and this is the first defense against **`Race Condition`** attack.

- **`Gallery & Feature`**: I just make `Gallery` & `Feature` inline with `Product` model to let admin show more about his/her
products

- **`Coupon`**: I'v added this model to let `Admin` create his/her own **`Coupon Type`**, also I'v added a field named 
**`expiration`** field so admin can change it as his/her requirements. The `expiration` field is a **`DurationField`** and will use
to know if users's coupon has been expired or not.

- **`UserCoupon`**: You can integrate your **`History`** model with that model to dispatch `coupon` for your clients as a presents
of buying. I'v added a scenario that check `UserCoupon` expirations and if a coupon was reached to its tres hold, will gets deleted

- **`Cart`**: This model has two fields for storing prices and exactly, I'v placed `products_price` field to calculate the product's
price in the backend with another **`GeneratedField`**. And that is the second defense against `Race Condition`. Also the most
important things about its `CartView` is that instead of using `for loop`, I'v used `map` and `lambda` functions, because, as you
know these are built-in functions of python & in the iterpertering time will not be parse by interpreter(These functions written 
in C language itself) so I use them instead of `for loop` and `yield` keyword.

- **`Order`**: This model will keep `progress tracking` also as you know I'v implemented the `service-repository` design pattern 
and we are going to let users use their `coupons`, right? Now, I'v used service to check user's coupon and consume it to give 
him/her a checkout. Also in its service, I let users to send their `coupon code` to calculate `total_price`. And the last and 
important thing is I used `transaction.atomic` decorator as the third layer of defense against `Race Condition` attack.

- **`OrderItem`**: In the last step, we will add all pieces together, therefor we will redirect user to `payment` gateway.

- **`WishList`**: This model will let users to store their favorite products and buy it later on.

### club app

In this app we will let users send their opinion about anything! Here we have two models:

- **`Rate`**: This model has a field named `vote` to keep grades about a product and also `each_product_rate` function to calculate
the average of votes of each product individually.

- **`Comment`**: This model will let users send their `suggestion` or `criticism` so you can classify and maintain your app better.

### dashboard app

This app does not contain any models but, I'v added a `queries` module and put some good queries in it

- **`ProductQuery`**: This class have two queries, one for looking for out of stock products, the other for calculate that how many
product is left in stock.

- **`RateQuery`**: This class has one query for now. Let me explain it(it's a little bit tricky):
Unlike what we did in the `Rate` model itself, here we don't have the model as ready to manage, so first we need to use `OuterRef` 
to reach the `product` in the `Product` model(we created a subquery). Than, we create its annotation and calculate the average vote
of each pk from last subquery; in the end, again we use `annotate` to add this `subquery` to the products. (Optionally you can give
them order to better indexing...)

### payment app

I will only add models not views and other staff to it.(because, some may want to write their own logic for payment)

- **`RoyalTransactions`**: We have these fields : two foreign keys, one for `User` and the other for `OrderItem`, `authorized_key` 
to keep payment gateway code, `price` that user want to pay for his products, `card_hash` to keep hash of cards, `tax` tax amount of
gateway, `transaction_id` for Transaction ID.

- **`History`**: After user do his/her transactions in payment gateway, whatever result is, we will store it in the `History` model
And we will need to do some important operations if payment is successful like: change the `progress-tracking` to `Paid` also
update your stock with the quantity of `Cart` models(decrease the `stock_qty` field of each single product object from `quantity`).

### Why you use @staticmethod decorator everywhere?

Let me explain by a very simple calculation:

As you may an expert in Python, you should be familiar with `getsizeof` function. This function will calculate how many bytes taken
by your objects(Object class, Functions, Lists & etc.). So Imagine that I was use normal class object(self keyword) for our design 
pattern and queries, You will reserve at least 3 objects at a time and each object will use 56 bytes from memory `56*3==168bytes` for every request, WOOOW what waste of memory!!!

## Frontend

For Now, I just use `redux` for state management, `axios` for api call & `bootstrap` to style my components.

I will add **`react-query`** package to update backend & frontend simultaneously.

Let's deep dive into most important components and modules.

### apiCall

This module was designed to help us create an `axios object`. This axios object used in everywhere we need to send requests to the
server. In fact, I designed it to uniform calls. If you check `backend.urls`, you will notice that all of our defined urls are like
**`api/v1/...`**, the `api` uses to let us know where those requests go(maybe you need to send requests to somewhere else) and `v1`
is versioning(for now).

### cartSlice

In this module we defined three reducers: `addProduct`, `removeProduct` & `clearCart`. As those names suggest, add & remove will
increase, decrease the chosen product by 1; `clearCart` will remove all products from the cart.

### authService

The `authService` module will do the login logout operations with the backend. In order to login you need `access token` and this
module will do it. The **`Log Out`** flow, just needs to delete the given `JWT` tokens. There is an object named `isAuthenticated`
This will check the `localStorage`, if there is an `access token` available or not.

## authSlice

Like **`cartSlice`**, we will keep state information in here. We have two reducers here: `loginSuccess` & `logoutSuccess`. These
reducers will keep users logged in or logged out. The `isAuthenticated` in 

### CartItem

This module will manage users cart. This module design to let users choose their favorite products and if they would like to
continue, click on `proceed to checkout`.

### Order 

This module was designed to let users use their **`coupons`** and also will show users their chosen `products`, `quantity` of those
products and the `total price` of all the products. If user has coupon, he/she can use it and it will effect in the `final price` in
the **`OrderItem`** model of backend and as soon as user gets there in the `OrderItem` component in the frontend, he can see his 
`final price` that should pay.

### UserCoupon

This component will let users know deadline of their `coupons`. This component use `useReducer` to update `timer`. The `useEffect`
will take the `created_at` field of `UserCoupon` model and create an object from `Date`, get the time of it, `subtract` it from 
the `created_at` and transform the result into a digital clock like object for user.

### Admin 

These components are classified into two parts:

- Showing information:

Admin can see information about everything, `users`, `products` & `advanced search`

- Managing api & database:

Admin can create, modify & delete everything from database.

## Contributing

If you wanna create new features like **Vendor** or **Notification**, follow these steps:

- clone the repository:

        git clone remote_address

- create and switch to your feature branch:

        git checkout -b vendor_feature

- make your changes to the project 

- push your code to remote repository

        git push -u origin vendor_feature

- pull your request to remote repo
