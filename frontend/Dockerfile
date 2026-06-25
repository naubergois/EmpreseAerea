FROM node:20-alpine

WORKDIR /app

# Instala dependências antes do código-fonte para melhor cache de layers
COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

# Verifica integridade do Vite na build (evita chunks ausentes por node_modules corrompido)
RUN node -e "\
  const fs = require('fs'); \
  const chunks = 'node_modules/vite/dist/node/chunks'; \
  if (!fs.existsSync(chunks)) throw new Error('vite chunks dir missing'); \
  const files = fs.readdirSync(chunks); \
  if (!files.some(f => f.startsWith('dep-') && f.endsWith('.js'))) \
    throw new Error('vite chunk files missing'); \
  "

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
