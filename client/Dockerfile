# ---------- builder ----------
FROM node:22.20.0-alpine AS builder

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .
RUN yarn build


# ---------- runtime ----------
FROM node:22.20.0-alpine

WORKDIR /app

# 1️⃣ .output
COPY --from=builder /app/.output ./.output

# 2️⃣ node_modules КЛАССИЧЕСКИ
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# 🔥 КЛЮЧ: говорим Node где deps
ENV NODE_PATH=/app/node_modules
ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000
CMD ["node", ".output/server/index.mjs"]
