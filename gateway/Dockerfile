# 1. Usa a imagem oficial do Nginx baseada em Alpine (Altamente recomendada em AppSec)
FROM nginx:1.25-alpine

# 2. Remove o arquivo de configuração padrão que vem nativo no Nginx de fábrica
RUN rm /etc/nginx/nginx.conf

# 3. Copia o seu arquivo nginx.conf do VS Code para o diretório interno de configurações do contêiner
COPY nginx.conf /etc/nginx/nginx.conf

# 4. Expõe a porta lógica 80 interna do contêiner
EXPOSE 80

# 5. Inicializa o Nginx em primeiro plano (foreground) para manter o contêiner ativo
CMD ["nginx", "-g", "daemon off;"]
