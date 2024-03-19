FROM node:20-alpine
WORKDIR /frontend
COPY package*.json ./
RUN npm install

COPY next.config.mjs ./
COPY next-env.d.ts ./
COPY postcss.config.js ./
COPY tailwind.config.ts ./
COPY tsconfig.json ./

COPY app ./app
COPY components ./components
COPY public ./public
COPY lib ./lib


EXPOSE 3000
CMD npm run dev