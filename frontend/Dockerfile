# Use the official Node.js image
FROM node:20 AS build

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json yarn.lock* package-lock.json* ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

ARG VITE_API_BASE_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
# Build the frontend for production
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]