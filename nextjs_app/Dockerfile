# Use an official Node.js runtime as a parent image
FROM node:18.18.2

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install project dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Build the Next.js application
#RUN npm run build

# Expose the port that your app will run on
EXPOSE 3000

# Start the Next.js application
#CMD ["npm", "start"]
