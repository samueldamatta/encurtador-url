FROM node:20-alpine AS build

WORKDIR /app

# Seu projeto só tem package.json, então copiamos só ele
COPY package.json ./

RUN npm install

# Copia todo o código-fonte
COPY . .

# Build de produção do Vite
RUN npm run build

# Etapa 2: servir com nginx
FROM nginx:alpine

# Remove conf padrão
RUN rm /etc/nginx/conf.d/default.conf

# Copia o build do Vite
COPY --from=build /app/dist /usr/share/nginx/html

# Copia nossa config de nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]