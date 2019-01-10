FROM php:5.6-fpm
COPY sources.list /etc/apt/sources.list
RUN apt-get update && apt-get install -y libfreetype6-dev libjpeg-dev libpng-dev vim\
&& docker-php-ext-install mysql \
&& docker-php-ext-install pdo pdo_mysql \
&& docker-php-ext-install mysqli \
&& docker-php-ext-configure gd --with-freetype-dir=/usr/include/  --with-png-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
&& docker-php-ext-install gd 
