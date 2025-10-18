# frontend/Dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
RUN npm run build

# serve static
FROM node:18-alpine
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/build /app/build
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
