FROM nginx

# Remove the stock configuration 
RUN rm /etc/nginx/conf.d/default.conf

# Copy in our configuration 
COPY nginx.conf /etc/nginx/conf.d
