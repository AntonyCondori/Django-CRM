FROM node:22-slim

# Enable pnpm via corepack
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Install dependencies (layer cached)
COPY package.json pnpm-lock.yaml* ./
ENV CI=true
RUN pnpm config set ignore-scripts false && pnpm install --frozen-lockfile || true

EXPOSE 5173

CMD ["pnpm", "dev", "--host", "0.0.0.0"]
