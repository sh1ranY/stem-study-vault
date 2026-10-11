FROM node:22-bookworm-slim AS frontend
WORKDIR /build
COPY package.json package-lock.json ./
RUN npm ci
COPY tsconfig.json vite.config.ts index.html ./
COPY src ./src
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY --from=frontend /build/dist ./dist
RUN useradd --create-home --uid 10001 studio && mkdir -p /var/data/study-studio && chown -R studio:studio /var/data /app
ENV STUDIO_DATA_DIR=/var/data/study-studio
EXPOSE 8765
CMD ["python", "-m", "backend.container_start"]
