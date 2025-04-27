FROM node:18

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build  # <--- build production version

EXPOSE 3000

CMD ["npm", "start"]
