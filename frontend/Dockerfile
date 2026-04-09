# frontend/Dockerfile - multi-stage build
FROM node:20-alpine AS builder


WORKDIR /app


# Build-time env for Next.js (must be set when building the image).
# Next.js embeds these into the server bundle — pass Docker Compose build args, not only runtime env.
ARG NEXT_PUBLIC_API_BASE_URL
ENV NEXT_PUBLIC_API_BASE_URL=$NEXT_PUBLIC_API_BASE_URL

# Flask base URL including /api/v1. In Compose, use the backend service name (see docker-compose build args).
ARG BACKEND_API_URL=http://127.0.0.1:5001/api/v1
ENV BACKEND_API_URL=$BACKEND_API_URL

COPY package.json package-lock.json* ./
RUN npm ci


COPY . .
RUN npm run build


# Production stage
FROM node:20-alpine AS runner


WORKDIR /app


ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1


RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs


COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static


USER nextjs


EXPOSE 3000


ENV PORT=3000
ENV HOSTNAME="0.0.0.0"


CMD ["node", "server.js"]