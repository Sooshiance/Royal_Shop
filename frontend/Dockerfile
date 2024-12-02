# Use the official Node.js image with version 20.16
FROM node:20.16

# Set the working directory inside the container
WORKDIR /frontend

COPY package.json yarn.lock ./

# Install dependencies using Yarn
RUN yarn install --frozen-lockfile

COPY . .

# Build the React application for production
RUN yarn build

# Expose port 3000 
EXPOSE 3000

CMD ["yarn", "start"]
