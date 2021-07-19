# Use nginx base image 
FROM nginx 

# Remove the default nginx.conf file that comes with the base nginx image
RUN rm /etc/nginx/conf.d/default.conf

# Copy the created nginx.conf for this app into that directory
COPY nginx.conf /etc/nginx/conf.d/