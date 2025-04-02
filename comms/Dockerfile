From node:18-alpine

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install --production

COPY index.js ./

EXPOSE 3000x    

CMD ["node", "index.js"]



