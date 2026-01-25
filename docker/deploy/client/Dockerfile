FROM node:22-alpine

WORKDIR /app

ENV NODE_ENV=production

# -----------------------
# Dependencies
# -----------------------
COPY client/package.json client/yarn.lock ./
RUN yarn install --frozen-lockfile --network-timeout 100000

# -----------------------
# Build
# -----------------------
COPY client .
RUN yarn build

# -----------------------
# Runtime
# -----------------------
ENV NITRO_HOST=0.0.0.0
ENV NITRO_PORT=3000

EXPOSE 3000

CMD ["node", ".output/server/index.mjs"]
