FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 5002

# Make sure CMD matches the entry point in package.json
CMD ["node", "app.js"]