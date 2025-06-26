# Use the official Node.js image
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the frontend for production
RUN npm run build

# Expose the port your frontend runs on
EXPOSE 3000

# Start the frontend server
CMD ["npm", "start"]