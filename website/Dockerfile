# syntax=docker/dockerfile:1
ARG NODE_VERSION=20.10.0

# Use node image for base image.
FROM node:${NODE_VERSION}-alpine as build

# Set working directory.
WORKDIR /usr/src/app

# Copy package.json and package-lock.json for installing dependencies.
COPY package*.json ./

# Install production dependencies.
RUN npm ci --omit=dev

# Copy the rest of the source files into the image.
COPY . .

# Run the build script.
RUN npm run build

# Install serve globally to serve the built application.
RUN npm install -g serve

# Expose the port that the serve command listens on.
EXPOSE 3000

# Run the serve command to serve the built application.
CMD ["serve", "-s", "build", "-l", "3000"]