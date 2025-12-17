FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=development

# Копируем только файлы зависимостей
COPY client/package.json client/yarn.lock ./

# Устанавливаем зависимости НОРМАЛЬНО
RUN yarn install --frozen-lockfile --network-timeout 100000

# Базовая копия (volume перезапишет в dev)
COPY client/ .

EXPOSE 3000

CMD ["yarn", "dev", "--host", "0.0.0.0"]
